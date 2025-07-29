import sys
sys.path.append(".")
sys.path.append("..")
import os
import os.path as osp
import numpy as np
import logging
import torch
import copy
import random
import json
import datetime
from tqdm import tqdm
import dspy
from datasets import DatasetDict
from collections import defaultdict, deque
from transformers import AutoModelForSequenceClassification
from datasets import Dataset
from optimas.reward.model import RewardModel
from optimas.collect import generate_trainset_preference_scorer
from optimas.reward.eval import eval_pipeline
from optimas.utils.logging import setup_logger
from optimas.optim.optimizer import CompoundAgentOptimizer
from optimas.optim.args import OptimasArguments
from optimas.reward.dataset import RewardDataset
from optimas.utils.lora import *
import wandb

class OnPolicyOptimizer:
    def __init__(
        self,
        pipeline,
        train_dataset,
        val_dataset,
        full_val_dataset,
        test_dataset,
        preference_dataset=None,  # Added parameter for existing preference dataset
        reward_model=None,
        per_iteration_rm_train_size=-1,
        tokenizer=None,
        iterations=5,
        per_iteration_input_size=20,
        base_model_name="meta-llama/Llama-3.1-8B-Instruct",
        output_dir="./optimas_on_policy",
        cooldown_period=1,  # Number of iterations before a module can be optimized again
        optimas_args=None,  # Add OptimasArguments
        vllm_host="localhost",
        vllm_port=8001,
        replay_buffer_size=200,
        use_replay_buffer=False
    ):
        self.pipeline = pipeline
        self.train_dataset = train_dataset
        self.val_dataset = val_dataset
        self.full_val_dataset = full_val_dataset
        self.test_dataset = test_dataset
        self.preference_dataset = preference_dataset
        self.reward_model = reward_model
        self.per_iteration_rm_train_size = per_iteration_rm_train_size
        self.iterations = iterations
        self.per_iteration_input_size = per_iteration_input_size
        self.module_performance_history = defaultdict(list)
        self.logger = setup_logger("on_policy_optimizer")
        self.base_model_name = base_model_name
        self.output_dir = output_dir
        self.tokenizer = tokenizer
        self.cooldown_period = cooldown_period
        self.optimas_args = optimas_args  # Store the optimas arguments
        self.vllm_host = vllm_host
        self.vllm_port = vllm_port
        self.use_replay_buffer = use_replay_buffer
        self.replay_buffer = deque(maxlen=replay_buffer_size) if use_replay_buffer else None

        # Track recently optimized modules
        self.recently_optimized = {}  # Module name -> iteration when last optimized

        # Track previous reward models for selector modules
        self.previous_reward_models = {
            "context_model_selector": None,
            "solver_model_selector": None,
        }

        # Track current adapter paths for local_lm modules
        self.current_adapters = {}  # module_name -> adapter_path

        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)

    def select_module_to_optimize(self, preference_dataset, current_iteration):
        """
        Select a module to optimize based on the score gaps in preference data.
        Uses softmax to probabilistically select modules with higher average gaps.
        Args:
            preference_dataset: DatasetDict containing preference pairs for each module
            current_iteration: The current optimization iteration
        Returns:
            String: The selected module name, or None if no eligible modules
        """
        if not preference_dataset:
            self.logger.warning("No preference data available")
            return None

        # Calculate average score gap for each module
        module_gaps = {}
        for module_name, dataset in preference_dataset.items():
            # Skip modules that were recently optimized (still in cooldown)
            if (
                module_name in self.recently_optimized
                and current_iteration - self.recently_optimized[module_name]
                < self.cooldown_period
            ):
                self.logger.info(
                    f"Module {module_name} is in cooldown period, skipping"
                )
                continue

            # Calculate average gap between chosen and rejected scores
            score_chosen = dataset["score_chosen"]
            score_rejected = dataset["score_rejected"]
            if len(score_chosen) == 0:
                continue

            avg_gap = sum(c - r for c, r in zip(score_chosen, score_rejected)) / len(
                score_chosen
            )
            module_gaps[module_name] = avg_gap
            self.logger.info(f"Module {module_name} average score gap: {avg_gap:.4f}")

        if not module_gaps:
            self.logger.warning(
                "No eligible modules found (all in cooldown or no data)"
            )
            return None

        # Apply softmax to create probability distribution
        module_names = list(module_gaps.keys())
        gap_values = [module_gaps[name] for name in module_names]

        # Convert to torch tensor and apply softmax
        gaps_tensor = torch.tensor(gap_values)
        probs = torch.nn.functional.softmax(gaps_tensor, dim=0).numpy()

        # Sample a module based on probabilities
        selected_idx = np.random.choice(len(module_names), p=probs)

        # log each module's probability
        wandb.log(
            {"iteration": current_iteration,
             **{f"prob_{module_name}": prob for module_name, prob in zip(module_names, probs)}}
        )

        selected_module = module_names[selected_idx]
        self.logger.info(
            f"Selected module {selected_module} for optimization with probability {probs[selected_idx]:.4f}"
        )

        # Log all module probabilities for transparency
        for i, name in enumerate(module_names):
            self.logger.info(
                f"Module {name}: gap={gap_values[i]:.4f}, probability={probs[i]:.4f}"
            )

        return selected_module

    def _is_local_lm_module(self, module_name):
        """Check if a module uses local LLM (has variable='local_lm')"""
        module = self.pipeline.modules[module_name]
        return hasattr(module, 'variable') and module.variable == 'local_lm'

    def _update_pipeline_with_adapter(self, module_name, adapter_path):
        """Update pipeline to use the new adapter for a local LLM module"""
        if not self._is_local_lm_module(module_name):
            return

        # Store the adapter path
        self.current_adapters[module_name] = adapter_path

        # Update the module's model_id to use the new adapter
        module = self.pipeline.modules[module_name]
        if hasattr(module, 'model_id'):
            # Generate a unique model ID for this adapter
            model_id = f"{module_name}_lora"

            # Load the adapter into vLLM using the enhanced safe function
            success = load_adapter_safe(model_id, adapter_path, self.vllm_host, self.vllm_port)

            if success:
                module.model_id = model_id
                module._current_adapter_path = adapter_path
                self.logger.info(f"Loaded adapter {adapter_path} as {model_id} into vLLM")
            else:
                self.logger.error(f"Failed to load adapter into vLLM: {adapter_path}")
                raise RuntimeError(f"Failed to load adapter {adapter_path}")

    def _get_current_adapter_state(self):
        """Get the current state of all adapters for saving/loading"""
        return copy.deepcopy(self.current_adapters)

    def _restore_adapter_state(self, adapter_state):
        """Restore adapter state and update pipeline accordingly"""
        for module_name, adapter_path in adapter_state.items():
            if adapter_path and self._is_local_lm_module(module_name):
                self._update_pipeline_with_adapter(module_name, adapter_path)
        self.current_adapters = copy.deepcopy(adapter_state)

    def optimize_module(self, module_name, hf_repo_or_local_dir):
        """
        Optimize a specific module using techniques from the existing framework.
        For local LLM modules, this includes PPO training.
        """
        self.logger.info(f"Optimizing module: {module_name}")

        # Handle special module types differently
        if module_name in ["context_model_selector", "solver_model_selector"]:
            self.logger.info(
                f"Setting reward model for {module_name} instead of optimizing"
            )
            # Store the current reward model for this module before changing it
            if hasattr(self.pipeline.modules[module_name], "reward_model"):
                self.previous_reward_models[module_name] = self.pipeline.modules[
                    module_name
                ].reward_model

            # Create a reward model from the trained model
            reward_model_for_sampling = RewardModel(
                self.reward_model, self.tokenizer, self.pipeline
            )

            # Set the reward model on the module
            self.pipeline.modules[module_name].set_reward_model(
                reward_model_for_sampling
            )
            return self.pipeline

        self.reward_model.eval()
        reward_model = RewardModel(self.reward_model, self.tokenizer, self.pipeline)

        # Prepare dataset specific to this module
        train_dataset = RewardDataset(
            pipeline=self.pipeline,
            hf_repo_or_local_dir=hf_repo_or_local_dir,
            original_trainset=self.train_dataset + self.full_val_dataset + self.test_dataset,
        ).to_inputs_only_dataset()

        self.logger.info(f'Training dataset size: {len(train_dataset[module_name]["input"])}')

        # Clone and modify optimas_args for this specific module
        module_optimas_args = copy.deepcopy(self.optimas_args)

        # Override with module-specific settings
        module_optimas_args.modules_to_apply = [
            module_name
        ]  # Focus only on this module
        module_optimas_args.per_module_train_size = min(
            len(train_dataset[module_name]["input"]), module_optimas_args.per_module_train_size
        )

        # Create module-specific output dir
        module_output_dir = os.path.join(self.output_dir, f"optim_{module_name}")
        os.makedirs(module_output_dir, exist_ok=True)
        module_optimas_args.output_dir = module_output_dir

        self.logger.info(
            f"Configured OptimasArguments for {module_name}: {vars(module_optimas_args)}"
        )

        # Initialize and run optimizer with the args from command line
        optimizer = CompoundAgentOptimizer(
            args=module_optimas_args,
            pipeline=self.pipeline,
            reward_model=reward_model,
            train_dataset=train_dataset,
            original_trainset=self.train_dataset,
            val_dataset=self.val_dataset,
            val_metrics_path=os.path.join(module_output_dir, "val_metrics.json"),
        )

        # Optimize just this module
        optimized_pipeline = optimizer.optimize()

        # For local LLM modules, check if PPO training produced new adapters
        if self._is_local_lm_module(module_name):
            # Look for PPO output directory
            ppo_output_dir = os.path.join(module_output_dir, "ppo", module_name)
            if os.path.exists(ppo_output_dir):
                # Find the best adapter using the enhanced function
                new_adapter_path = get_adapter_from_ppo_output(module_output_dir, module_name)

                if new_adapter_path:
                    self.logger.info(f"Found new adapter for {module_name}: {new_adapter_path}")

                    # Update the pipeline to use the new adapter
                    self._update_pipeline_with_adapter(module_name, new_adapter_path)
                else:
                    self.logger.warning(f"No valid adapter found in PPO output directory: {ppo_output_dir}")
            else:
                self.logger.info(f"No PPO output directory found: {ppo_output_dir}")

        return optimized_pipeline

    def train_reward_model(self, module_name, hf_repo_or_local_dir, per_iteration_rm_train_size=-1):
        """
        Train a reward model on the collected preference data for the specified module.
        Args:
            module_name: Name of the module to train the reward model for
            hf_repo_or_local_dir: Path to the preference dataset
        Returns:
            Trained reward model
        """
        self.logger.info(f"Training reward model for module: {module_name}")

        # Setup reward model training configuration
        from peft import LoraConfig
        from transformers import BitsAndBytesConfig
        from optimas.external import RewardConfig
        from optimas.reward.finetune import run_finetune
        from optimas.reward.dataset import RewardDataset

        # Create module-specific output directory
        module_output_dir = os.path.join(self.output_dir, f"reward_model_{module_name}")
        os.makedirs(module_output_dir, exist_ok=True)

        # Configure LoRA for efficient fine-tuning
        peft_config = LoraConfig(
            r=16,  # LoRA attention dimension
            lora_alpha=8,  # LoRA alpha parameter
            lora_dropout=0.05,  # Dropout probability for LoRA
            bias="none",  # Bias type
            task_type="CAUSAL_LM",  # Task type for LoRA
            init_lora_weights="gaussian",
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ],
        )

        # Configure quantization if needed (8-bit training)
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_quant_type="nf8",
            bnb_8bit_use_double_quant=False,
            bnb_8bit_compute_dtype=torch.bfloat16,
        )

        # Training configuration
        training_args = RewardConfig(
            do_train=True,
            output_dir=module_output_dir,
            logging_dir=module_output_dir,
            per_device_train_batch_size=2,
            per_device_eval_batch_size=2,
            gradient_accumulation_steps=8,
            learning_rate=5e-5,
            num_train_epochs=1,
            max_length=2048,
            logging_steps=10,
            eval_steps=50,
            save_steps=50,
            eval_strategy="no",
            metric_for_best_model="eval_loss",
            load_best_model_at_end=False,
            use_score_scaling=False,
            use_score_norm=False,
            ddp_find_unused_parameters=False,
        )

        # Load dataset
        reward_dataset = RewardDataset(hf_repo_or_local_dir, self.pipeline)

        # Format the dataset
        ds = reward_dataset.to_format(
            eval_ratio=0, format="implicit_preference", add_margin=False
        )

        if per_iteration_rm_train_size != -1:
            # shuffle and take the first per_iteration_rm_train_size samples
            import random
            random.seed(42)
            train_list = ds["train"].to_list()
            random.shuffle(train_list)
            train_list = train_list[:per_iteration_rm_train_size]
            ds["train"] = Dataset.from_list(train_list)
        # Otherwise use the full reward dataset

        # Train the reward model
        trainer = run_finetune(
            ds,
            self.reward_model,
            self.tokenizer,
            training_args,
            format="implicit_preference",  # Training on preference pairs
            train_last_layer=True,
            module_to_idx={module_name: self.pipeline.optimizable_module_to_idx[module_name]}
        )

        return trainer.model

    def evaluate_pipeline(self, pipeline, eval_set):
        """
        Evaluate the pipeline on the test dataset and return average score
        """
        metrics, _ = eval_pipeline(pipeline=pipeline, testset=eval_set, num_repeat=1)
        if "mean" in metrics:
            return metrics["mean"]
        elif "avg_score" in metrics:
            return metrics["avg_score"]
        else:
            return (
                sum(metrics["scores"]) / len(metrics["scores"])
                if metrics["scores"]
                else 0
            )

    def optimize(self):
        """
        Main optimization loop using the existing preference dataset to select modules.
        """
        # Store initial pipeline state dict for comparison
        original_state_dict = self.pipeline.state_dict()
        original_adapter_state = self._get_current_adapter_state()

        # Optimization history
        history = {"iterations": [], "overall_performance": []}

        # Set reward_model at the beginning
        local_hyper_param_search = any([module.variable_search_space for module in self.pipeline.modules.values()])
        if not args.global_hyper_param_search and local_hyper_param_search:
            self.pipeline.register_rm(
                RewardModel(self.reward_model, self.tokenizer, self.pipeline), sample_size=1
            )
            # => sample_size=1 causes no effect to modules without variable_search_space

        # Evaluate initial performance
        try:
            initial_score = self.evaluate_pipeline(self.pipeline, self.val_dataset)
            self.logger.info(f"Initial score: {initial_score:.4f}")
        except Exception as e:
            self.logger.warning(
                f"Error evaluating initial pipeline: {e}. Setting initial score to 0."
            )
            initial_score = 0

        history["overall_performance"].append(initial_score)

        # Best score and pipeline state so far
        best_score = initial_score
        best_state_dict = original_state_dict
        best_adapter_state = original_adapter_state
        current_best_iteration = 0

        wandb.log(
            {
                "iteration": 0,
                "eval/score": best_score,
                "eval/best_score": best_score
            }
        )

        # get env variable skip online training
        skip_online_datagen = os.getenv("SKIP_ONLINE_DATAGEN", "false").lower() == "true"

        # Check if preference dataset exists
        if self.preference_dataset is None:
            self.logger.error("No preference dataset provided. Cannot continue.")
            return self.pipeline, history

        # Log preference dataset stats
        self.logger.info("Using provided preference dataset:")
        for module_name, dataset in self.preference_dataset.items():
            self.logger.info(f"  {module_name}: {len(dataset)} preference pairs")

        enable_data_gen = True # SHIRWU CHANGE 1

        # Main optimization loop
        self.logger.info("Starting optimization iterations...")
        for iteration in range(self.iterations):
            self.logger.info(f"Starting iteration {iteration+1}/{self.iterations}")

            # Select a module to optimize based on preference data
            module_to_optimize = self.select_module_to_optimize(
                self.preference_dataset, iteration
            )

            if not module_to_optimize:
                self.logger.warning(
                    "No suitable module to optimize, ending optimization"
                )
                break

            self.logger.info(f"Selected module to optimize: {module_to_optimize}")

            if skip_online_datagen or not enable_data_gen:
                print("!" * 50, "FRESH TRAINING SKIPPED", "!" * 50)
                fresh_preference_dataset = [module_to_optimize]
            else:
                subset_size = min(len(self.train_dataset), self.per_iteration_input_size)
                dataset_subset = random.sample(self.train_dataset, subset_size)
                fresh_preference_dataset = generate_trainset_preference_scorer(
                    pipeline=self.pipeline,
                    dataset=dataset_subset,
                    module_names=[module_to_optimize],
                    num_forward_estimate=3,
                    num_repeat_samples=5,
                    max_workers=4,
                    num_per_instance=3
                )

            # ------------------------------------------------------------------
            # Build training dataset for reward-model update
            # ------------------------------------------------------------------
            if module_to_optimize in fresh_preference_dataset:
                dataset = fresh_preference_dataset[module_to_optimize]

                # ---------- branch: replay-buffer ON ----------
                if self.use_replay_buffer:
                    # 1) push new pairs into buffer
                    for i in range(len(dataset)):
                        sample = {
                            "context": dataset["context"][i],
                            "response_chosen": dataset["response_chosen"][i],
                            "response_rejected": dataset["response_rejected"][i],
                            "score_chosen": dataset["score_chosen"][i],
                            "score_rejected": dataset["score_rejected"][i],
                        }
                        if "margin" in dataset.column_names:
                            sample["margin"] = dataset["margin"][i]
                        self.replay_buffer.append(sample)

                    self.logger.info(
                        f"Added {len(dataset)} samples to buffer. "
                        f"Buffer size = {len(self.replay_buffer)}/{self.replay_buffer.maxlen}"
                    )

                    # 2) convert entire buffer back to Dataset
                    buffer_data = {
                        "context": [s["context"] for s in self.replay_buffer],
                        "response_chosen": [s["response_chosen"] for s in self.replay_buffer],
                        "response_rejected": [s["response_rejected"] for s in self.replay_buffer],
                        "score_chosen": [s["score_chosen"] for s in self.replay_buffer],
                        "score_rejected": [s["score_rejected"] for s in self.replay_buffer],
                    }
                    if any("margin" in s for s in self.replay_buffer):
                        buffer_data["margin"] = [s.get("margin", 0.0) for s in self.replay_buffer]

                    training_dataset = DatasetDict(
                        {module_to_optimize: Dataset.from_dict(buffer_data)}
                    )

                    dataset_path = os.path.join(
                        self.output_dir,
                        f"buffer_preference_dataset_{iteration}_{module_to_optimize}",
                    )
                    training_dataset.save_to_disk(dataset_path)

                # ---------- branch: replay-buffer OFF ----------
                else:
                    if not enable_data_gen or skip_online_datagen:
                        dataset_path = os.path.join(
                            self.output_dir,
                            f"preference_dataset_{iteration}_{module_to_optimize}",
                        )
                        selected_data = {
                            module_to_optimize: self.preference_dataset[module_to_optimize]
                        }
                        DatasetDict(selected_data).save_to_disk(dataset_path)
                    else:
                        dataset_path = os.path.join(
                            self.output_dir,
                            f"fresh_preference_dataset_{iteration}_{module_to_optimize}",
                        )
                        fresh_preference_dataset.save_to_disk(dataset_path)

                    # when buffer is OFF train on whatever is in dataset_path
                    training_dataset = None  # not used, but keep name defined

                # -------- reward-model fine-tune on dataset_path --------
                trained_model = self.train_reward_model(
                    module_to_optimize, dataset_path, self.per_iteration_rm_train_size
                )
                self.reward_model = trained_model


            # # Save preference dataset to disk (just the selected module's data)
            # if module_to_optimize in fresh_preference_dataset:
            #     dataset_path = os.path.join(
            #         self.output_dir,
            #         f"preference_dataset_{iteration}_{module_to_optimize}",
            #     )

            #     if not enable_data_gen or skip_online_datagen: # SHIRWU CHANGE 2
            #         selected_data = {
            #             module_to_optimize: self.preference_dataset[module_to_optimize]
            #         }
            #         DatasetDict(selected_data).save_to_disk(dataset_path)
            #     else:
            #         dataset_path = os.path.join(self.output_dir, f"fresh_preference_dataset_{iteration}_{module_to_optimize}")
            #         fresh_preference_dataset.save_to_disk(dataset_path)

            #         # Train reward model on this module's data
            #         trained_model = self.train_reward_model(
            #             module_to_optimize, dataset_path, self.per_iteration_rm_train_size
            #         )
            #         self.reward_model = trained_model  # Update the reward model

                # Save the current pipeline state before optimization
                current_state_dict = self.pipeline.state_dict()
                current_adapter_state = self._get_current_adapter_state()

                # Optimize the module
                optimized_pipeline = self.optimize_module(
                    module_to_optimize, dataset_path
                )

                if not args.global_hyper_param_search and local_hyper_param_search:
                    self.pipeline.register_rm(
                        RewardModel(self.reward_model, self.tokenizer, self.pipeline), sample_size=1
                    )

                # Evaluate optimized pipeline
                try:
                    new_score = self.evaluate_pipeline(
                        optimized_pipeline, self.val_dataset
                    )
                    self.logger.info(
                        f"After optimizing {module_to_optimize}, score: {new_score:.4f} (previous: {best_score:.4f})"
                    )

                    # Record this successful optimization
                    history["iterations"].append(
                        {
                            "iteration": iteration + 1,
                            "current_best_iteration": current_best_iteration,
                            "module_optimized": module_to_optimize,
                            "score_before": best_score,
                            "score_after": new_score,
                            "improvement": new_score - best_score,
                            "gap_data": {
                                "num_pairs": len(
                                    self.preference_dataset[module_to_optimize]
                                ),
                                "avg_gap": sum(
                                    self.preference_dataset[module_to_optimize][
                                        "score_chosen"
                                    ]
                                )
                                / len(self.preference_dataset[module_to_optimize])
                                - sum(
                                    self.preference_dataset[module_to_optimize][
                                        "score_rejected"
                                    ]
                                )
                                / len(self.preference_dataset[module_to_optimize]),
                            },
                        }
                    )

                    wandb.log(
                        {
                            "iteration": iteration + 1,
                            "module_idx": self.pipeline.optimizable_module_to_idx[module_to_optimize],
                            "eval/score": new_score,
                            "eval/best_score": best_score
                        }
                    )

                    # Check if there's improvement
                    if new_score > best_score:
                        enable_data_gen = True # SHIRWU CHANGE 3
                        self.logger.info(
                            f"Performance improved from {best_score:.4f} to {new_score:.4f}"
                        )
                        best_score = new_score
                        best_state_dict = optimized_pipeline.state_dict()
                        best_adapter_state = self._get_current_adapter_state()
                        current_best_iteration = iteration + 1

                        # Save the improved pipeline state
                        torch.save(
                            best_state_dict,
                            os.path.join(
                                self.output_dir,
                                f"pipeline_state_iteration_{iteration+1}_{module_to_optimize}.pth",
                            ),
                        )

                        # Save adapter state
                        with open(
                            os.path.join(
                                self.output_dir,
                                f"adapter_state_iteration_{iteration+1}_{module_to_optimize}.json",
                            ), "w"
                        ) as f:
                            json.dump(best_adapter_state, f, indent=2)

                        # Mark this module as recently optimized
                        self.recently_optimized[module_to_optimize] = iteration
                    else:
                        self.logger.info(
                            f"No improvement from optimizing {module_to_optimize}, reverting"
                        )
                        # Revert the pipeline state
                        self.pipeline.load_state_dict(current_state_dict)
                        self._restore_adapter_state(current_adapter_state)

                        # If this was a selector module, restore its previous reward model
                        if module_to_optimize in [
                            "context_model_selector",
                            "solver_model_selector",
                        ]:
                            if (
                                self.previous_reward_models[module_to_optimize]
                                is not None
                            ):
                                self.pipeline.modules[
                                    module_to_optimize
                                ].set_reward_model(
                                    self.previous_reward_models[module_to_optimize]
                                )
                            else:
                                # Reset to None if there was no previous reward model
                                self.pipeline.modules[
                                    module_to_optimize
                                ].reward_model = None

                except Exception as e:
                    self.logger.error(
                        f"Error evaluating optimized pipeline: {e}. Reverting."
                    )
                    # Revert the pipeline state
                    self.pipeline.load_state_dict(current_state_dict)
                    self._restore_adapter_state(current_adapter_state)
            else:
                self.logger.warning(
                    f"No preference data available for module {module_to_optimize}"
                )

            # Update to best state so far for next iteration
            self.pipeline.load_state_dict(best_state_dict)
            self._restore_adapter_state(best_adapter_state)

            # Update performance history
            history["overall_performance"].append(best_score)

        # Final improvement calculation
        improvement = best_score - initial_score
        self.logger.info(
            f"Overall improvement: {improvement:.4f} ({initial_score:.4f} to {best_score:.4f})"
        )
        history["overall_improvement"] = improvement

        # Ensure we return the pipeline with the best state
        self.pipeline.load_state_dict(best_state_dict)
        self._restore_adapter_state(best_adapter_state)

        return self.pipeline, history


if __name__ == "__main__":
    import argparse
    import datetime
    from dotenv import load_dotenv
    from examples.pipelines import registered_pipeline
    from examples.datasets import registered_dataset
    from optimas.utils.load import load_model_and_tokenizer
    from datasets import load_from_disk, load_dataset
    from optimas.optim.args import OptimasArguments

    parser = argparse.ArgumentParser(description="On-Policy Pipeline Optimization")

    # ========================= Dataset & Pipeline Configuration =========================
    data_group = parser.add_argument_group("Dataset and Pipeline Configuration")
    # [KEY] need to specify dataset to load
    data_group.add_argument(
        "--dataset", type=str, default="pubmed", help="Dataset to use"
    )
    # [KEY] need to specify pipeline to load
    data_group.add_argument(
        "--pipeline", type=str, default="pubmed_pipeline", help="Pipeline to optimize"
    )
    data_group.add_argument(
        "--val_size", type=int, default=10, help="Validation set size"
    )
    data_group.add_argument(
        "--num_repeat", type=int, default=1, help="Number of times to repeat evaluation"
    )
    data_group.add_argument(
        "--max_sample_workers", type=int, default=4, help="Maximum parallel workers"
    )
    data_group.add_argument(
        "--dotenv_path",
        type=str,
        default="/dfs/project/kgrlm/common/.env",
        help="Path to .env file",
    )
    data_group.add_argument(
        "--run_name",
        type=str,
        default="run",
        help="Name of the current",
    )

    # ========================= vLLM Configuration =========================
    vllm_group = parser.add_argument_group("vLLM Configuration")
    vllm_group.add_argument(
        "--vllm_host",
        type=str,
        default="localhost",
        help="vLLM server host",
    )
    vllm_group.add_argument(
        "--vllm_port",
        type=int,
        default=8001,
        help="vLLM server port",
    )

    # ========================= Optimization Settings =========================
    optim_group = parser.add_argument_group("Optimization Settings")
    optim_group.add_argument(
        "--iterations", type=int, default=5, help="Number of optimization iterations"
    )
    optim_group.add_argument(
        "--per_iteration_input_size", type=int, default=10, help="Samples per iteration"
    )
    optim_group.add_argument(
        "--cooldown",
        type=int,
        default=1,
        help="Cooldown period before reoptimizing a module",
    )
    optim_group.add_argument(
        "--global_hyper_param_search", action="store_true", help="Enable hyperparameter search"
    )
    optim_group.add_argument(
        "--modules_to_apply",
        nargs="+",
        default=["all"],
        help="Modules to apply optimization to",
    )
    optim_group.add_argument(
        "--use_replay_buffer",
        action="store_true",
        default=False,
        help="Turn on the sliding replay buffer; otherwise every iteration trains only on the fresh batch",
    )
    optim_group.add_argument(
        "--replay_buffer_size",
        type=int,
        default=200,
        help="Maximum number of preference pairs kept in the replay buffer",
    )

    # ========================= Reward model Settings =========================
    reward_group = parser.add_argument_group("Reward Model Settings")
    reward_group.add_argument(
        "--per_iteration_rm_train_size", type=int, default=-1, help="Size of training set for reward model"
    )

    # ========================= OptimasArguments Settings =========================
    optimas_group = parser.add_argument_group("Optimas Optimization Settings")
    optimas_group.add_argument(
        "--optimize_prompts", action="store_true", default=True, help="Optimize prompts"
    )
    optimas_group.add_argument(
        "--no_prompts_opt",
        action="store_false",
        dest="optimize_prompts",
        help="Disable prompt optimization",
    )
    optimas_group.add_argument(
        "--prompt_optimizer",
        type=str,
        default="opro",
        choices=["opro", "mipro", "copro"],
        help="Prompt optimization method",
    )
    # [Key] Only applicable to reward dataset!
    optimas_group.add_argument(
        "--per_module_train_size",
        type=int,
        default=20,
        help="Training examples per module",
    )
    optimas_group.add_argument(
        "--per_module_search_size",
        type=int,
        default=20,
        help="Search examples per module",
    )
    optimas_group.add_argument(
        "--num_prompt_candidates",
        type=int,
        default=3,
        help="Number of candidates to generate",
    )
    optimas_group.add_argument(
        "--requires_permission_to_run",
        action="store_true",
        help="Require permission to run",
    )
    optimas_group.add_argument(
        "--verbose", action="store_true", default=True, help="Show verbose output"
    )
    optimas_group.add_argument(
        "--quiet", action="store_false", dest="verbose",
        help="Disable verbose output"
    )
    optimas_group.add_argument(
        "--auto",
        action="store_true",
        help="Automatically determine parameters for MIPRO",
    )
    optimas_group.add_argument(
        "--validate",
        action="store_true",
        default=True,
        help="Validate during optimization",
    )
    optimas_group.add_argument(
        "--no_validate",
        action="store_false",
        dest="validate",
        help="Disable validation during optimization",
    )
    optimas_group.add_argument(
        "--val_every_prompt_iter",
        type=int,
        default=3,
        help="Validate every N prompt iterations",
    )
    optimas_group.add_argument(
        "--val_every_ppo_ratio",
        type=float,
        default=0.25,
        help="Validation ratio for PPO",
    )
    optimas_group.add_argument(
        "--val_every_grid_ratio",
        type=float,
        default=0.25,
        help="Validation ratio for grid search",
    )

    # ========================= Model & Data Paths =========================
    path_group = parser.add_argument_group("Model and Data Paths")
    path_group.add_argument(
        "--output_dir", type=str, default="./on_policy_optim", help="Output directory"
    )
    path_group.add_argument(
        "--base_model",
        type=str,
        default="meta-llama/Llama-3.1-8B-Instruct",
        help="Base model for reward model",
    )
    path_group.add_argument(
        "--state_dict_path",
        type=str,
        default=None,
        help="Path to a pre-trained reward model state dict",
    )
    path_group.add_argument(
        "--preference_dataset",
        type=str,
        required=True,
        help="Path to pre-generated preference dataset",
    )
    path_group.add_argument(
        "--pipeline_state_dict_path",
        type=str,
        default=None,
        help="Path to pipeline state dict",
    )
    path_group.add_argument(
        "--load_in_4bit", action="store_true", help="Load model in 4-bit precision"
    )
    path_group.add_argument(
        "--load_in_8bit", action="store_true", help="Load model in 8-bit precision"
    )
    path_group.add_argument(
        "--train_multi_head",
        action="store_true",
        default=True,
        help="Train multi-head reward model",
    )

    # ========================= PPO-Related Options =========================
    ppo_group = parser.add_argument_group("PPO Options")
    # [KEY] need to specify ppo to turn on PPO
    ppo_group.add_argument(
        "--weight_optimizer",
        type=str,
        default="none",
        choices=["none", "ppo"],
        help="Weight optimizer method",
    )
    # [KEY] max steps, can cut off epochs
    ppo_group.add_argument(
        "--ppo_train_steps", type=int, default=800, help="Number of PPO training steps"
    )
    # [KEY] need to be >0 to turn on PPO
    ppo_group.add_argument(
        "--ppo_epochs", type=int, default=0, help="Number of PPO epochs, default no PPO"
    )
    ppo_group.add_argument(
        "--ppo_batch_size", type=int, default=2, help="PPO batch size"
    )
    ppo_group.add_argument(
        "--ppo_learning_rate", type=float, default=1e-4, help="PPO learning rate"
    )
    ppo_group.add_argument(
        "--ppo_save_every",
        type=int,
        default=0,
        help="Save PPO model every N steps (0 to disable)",
    )
    ppo_group.add_argument(
        "--ppo_save_epoch_ratio",
        type=float,
        default=0.25,
        help="Save PPO model at this ratio of each epoch",
    )
    ppo_group.add_argument(
        "--ppo_resume_adapter",
        type=str,
        default=None,
        help="Path to resume PPO adapter from",
    )
    ppo_group.add_argument(
        "--ppo_base_model_name",
        type=str,
        default="Qwen/Qwen2.5-1.5B-Instruct",
        help="Base model for PPO",
    )

    # ========================= Amazon Pipeline Specific Options =========================
    amazon_group = parser.add_argument_group("Amazon Pipeline Specific Options")
    amazon_group.add_argument(
        "--session_adapter",
        type=str,
        default=None,
        help="PPO session analyzer LoRA adapter",
    )
    amazon_group.add_argument(
        "--profiler_adapter",
        type=str,
        default=None,
        help="PPO candidate profiler LoRA adapter",
    )

    # ========================= Embedding Similarity Options =========================
    emb_group = parser.add_argument_group("Embedding Similarity Options")
    # [KEY] need to add this to use embedding similarity reward model
    emb_group.add_argument(
        "--emb_sim_reward",
        action="store_true",
        help="Use embedding similarity reward model",
    )
    emb_group.add_argument(
        "--emb_dir",
        type=str,
        default="/dfs/project/kgrlm/multiagent_reward/trl/reward_emb/embedding_cache",
        help="Directory for embedding cache",
    )
    emb_group.add_argument(
        "--embedding_model",
        type=str,
        default="text-embedding-3-small",
        help="Embedding model name",
    )
    emb_group.add_argument(
        "--margin_threshold",
        type=float,
        default=0.5,
        help="Margin threshold for embedding similarity",
    )

    lora_group = parser.add_argument_group("LoRA Options")
    lora_group.add_argument(
        "--lora_r", type=int, default=32, help="LoRA rank"
    )
    lora_group.add_argument(
        "--lora_alpha", type=int, default=16, help="LoRA alpha"
    )
    lora_group.add_argument(
        "--lora_dropout", type=float, default=0.0, help="LoRA dropout"
    )

    args = parser.parse_args()

    wandb.init(
        project="optimas",
        entity="dsp-team",
        name=f"{args.run_name}_{args.dataset}",
        config=args,
        save_code=True
    )

    # Customize output dir with timestamp
    args.output_dir = osp.join(args.output_dir, args.dataset, args.pipeline, args.run_name)
    os.makedirs(args.output_dir, exist_ok=True)

    # Set up logging
    logger = setup_logger(
        __name__, log_file=os.path.join(args.output_dir, "output.log")
    )
    logger.info(f"Arguments: {args}")

    # Load environment variables
    load_dotenv(args.dotenv_path)

    # Initialize pipeline with appropriate parameters based on pipeline type
    if args.pipeline == "amazon_next_item_selection_local_pipeline":
        logger.info(
            f"Using Amazon pipeline with adapters: {args.session_adapter=}, {args.profiler_adapter=}"
        )
        pipeline = registered_pipeline[args.pipeline](
            session_adapter=args.session_adapter,
            profiler_adapter=args.profiler_adapter,
            log_dir=args.output_dir,
            max_sample_workers=args.max_sample_workers
        )
    else:
        pipeline = registered_pipeline[args.pipeline](
            log_dir=args.output_dir, max_sample_workers=args.max_sample_workers
        )

    # Load dataset
    logger.info(f"Loading dataset: {args.dataset}")
    trainset, valset, testset = registered_dataset[args.dataset]()
    full_valset = copy.deepcopy(valset)

    # Configure validation set
    val_size = min(args.val_size, len(trainset)) if hasattr(args, "val_size") else 10
    if valset is None or len(valset) == 0:
        logger.info(
            f"No validation set provided, using {val_size} samples from trainset"
        )
        valset = trainset[:val_size]
    else:
        valset = valset[:val_size]

    logger.info(
        f"Dataset sizes - Train: {len(trainset)}, Val: {len(valset)}, Test: {len(testset) if testset else 'N/A'}"
    )

    # Load preference dataset
    logger.info(f"Loading preference dataset from {args.preference_dataset}")
    preference_dataset = load_dataset(args.preference_dataset)

    # Load initial pipeline state if provided
    if args.pipeline_state_dict_path:
        logger.info(f"Loading pipeline state from {args.pipeline_state_dict_path}")
        pipeline_state_dict = torch.load(args.pipeline_state_dict_path)
        pipeline.load_state_dict(pipeline_state_dict)

    # Create OptimasArguments from command-line arguments
    optimas_args = OptimasArguments(
        optimize_prompts=args.optimize_prompts,
        prompt_optimizer=args.prompt_optimizer,
        per_module_train_size=args.per_module_train_size,
        per_module_search_size=args.per_module_search_size,
        num_prompt_candidates=args.num_prompt_candidates,
        requires_permission_to_run=args.requires_permission_to_run,
        verbose=args.verbose,
        output_dir=args.output_dir,
        weight_optimizer=args.weight_optimizer,
        global_hyper_param_search=args.global_hyper_param_search,
        modules_to_apply=args.modules_to_apply,
        ppo_train_steps=args.ppo_train_steps,
        ppo_epochs=args.ppo_epochs, # we take min(epoch, steps) in PPO training
        ppo_batch_size=args.ppo_batch_size,
        ppo_learning_rate=args.ppo_learning_rate,
        ppo_save_every=args.ppo_save_every,
        ppo_save_epoch_ratio=args.ppo_save_epoch_ratio,
        ppo_base_model_name=args.ppo_base_model_name,
        val_every_prompt_iter=args.val_every_prompt_iter,
        val_every_ppo_ratio=args.val_every_ppo_ratio,
        emb_sim_reward=args.emb_sim_reward,
        max_sample_workers=args.max_sample_workers,
        policy_device=f"cuda:{torch.cuda.current_device()}",  # Set policy device
    )

    # Initialize reward model
    if args.emb_sim_reward:
        from optimas.reward.model import EmbeddingSimilarityRewardModel
        from optimas.reward.dataset import RewardDataset
        logger.info(
            f"Using embedding similarity reward model with {args.embedding_model}"
        )
        rd = RewardDataset(
            hf_repo_or_local_dir=args.preference_dataset,
            pipeline=pipeline,
            original_trainset=trainset + full_valset + testset,
        )
        reward_model = EmbeddingSimilarityRewardModel(
            pipeline=pipeline,
            reward_dataset=rd,
            embedding_model=args.embedding_model,
            margin_threshold=args.margin_threshold,
            cache_dir=args.emb_dir,
        )
        tokenizer = None
    else:
        # Configure LoRA for the reward model
        from peft import LoraConfig
        from transformers import BitsAndBytesConfig
        logger.info(f"Initializing LoRA-based reward model with {args.base_model}")

        peft_config = LoraConfig(
            r=args.lora_r,
            lora_alpha=args.lora_alpha,
            lora_dropout=args.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
            init_lora_weights="gaussian",
            target_modules=[
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ],
        )

        # Configure quantization if needed
        bnb_config = None
        if args.load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=False,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
        elif args.load_in_8bit:
            bnb_config = BitsAndBytesConfig(
                load_in_8bit=True,
                bnb_8bit_quant_type="nf8",
                bnb_8bit_use_double_quant=False,
                bnb_8bit_compute_dtype=torch.bfloat16,
            )

        # Load initial model for reward training
        model, tokenizer = load_model_and_tokenizer(
            args.base_model,
            peft_config=peft_config,
            bnb_config=bnb_config,
            model_class=AutoModelForSequenceClassification,
            num_labels=(
                len(pipeline.optimizable_modules) if args.train_multi_head else 1
            ),
            state_dict_path=args.state_dict_path,
        )
        reward_model = model

    # Create optimizer
    logger.info("Initializing On-Policy Optimizer")
    optimizer = OnPolicyOptimizer(
        iterations=args.iterations,
        per_iteration_input_size=args.per_iteration_input_size,
        per_iteration_rm_train_size=args.per_iteration_rm_train_size,
        pipeline=pipeline,
        train_dataset=trainset,
        val_dataset=valset,
        full_val_dataset=full_valset,
        test_dataset=testset,
        preference_dataset=preference_dataset,
        reward_model=reward_model,
        tokenizer=tokenizer,
        base_model_name=args.base_model,
        output_dir=args.output_dir,
        cooldown_period=args.cooldown,
        optimas_args=optimas_args,  # Pass the OptimasArguments to the optimizer
        vllm_host=args.vllm_host,
        vllm_port=args.vllm_port,
        replay_buffer_size=args.replay_buffer_size,
        use_replay_buffer=args.use_replay_buffer,  
    )

    # Run optimization
    logger.info("Starting optimization process")
    optimized_pipeline, history = optimizer.optimize()

    # Save optimization history
    history_path = os.path.join(args.output_dir, "optimization_history.json")
    logger.info(f"Saving optimization history to {history_path}")
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    # Evaluate final pipeline on test set if available
    if testset and len(testset) > 0:
        logger.info("Evaluating optimized pipeline on test set")
        try:
            metrics, preds = eval_pipeline(
                pipeline=optimized_pipeline, testset=testset, num_repeat=args.num_repeat
            )
            metrics_path = os.path.join(args.output_dir, "eval_metrics.json")
            logger.info(f"Saving evaluation metrics to {metrics_path}")
            with open(metrics_path, "w") as f:
                json.dump(metrics, f, sort_keys=True, indent=2)

            wandb.log(
                {   "iteration": args.iterations,
                    "test/score": metrics["mean"],
                    "test/std": metrics["std"],
                }
            )
        except Exception as e:
            logger.error(f"Error evaluating optimized pipeline: {e}")

    # Save final optimized pipeline
    final_pipeline_path = os.path.join(args.output_dir, "final_optimized_pipeline.pth")
    logger.info(f"Saving final optimized pipeline to {final_pipeline_path}")
    torch.save(optimized_pipeline.state_dict(), final_pipeline_path)

    # Save final adapter state
    final_adapter_state = optimizer._get_current_adapter_state()
    with open(os.path.join(args.output_dir, "final_adapter_state.json"), "w") as f:
        json.dump(final_adapter_state, f, indent=2)

    # Log improvement summary
    if "overall_improvement" in history:
        improvement = history["overall_improvement"]
        logger.info(f"Final improvement: {improvement:.4f}")

        # Create a summary file with key metrics
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "pipeline": args.pipeline,
            "dataset": args.dataset,
            "iterations": args.iterations,
            "initial_score": history["overall_performance"][0],
            "final_score": history["overall_performance"][-1],
            "improvement": improvement,
            "modules_optimized": (
                [it["module_optimized"] for it in history["iterations"]]
                if "iterations" in history
                else []
            ),
            "final_adapter_state": final_adapter_state,
        }

        with open(os.path.join(args.output_dir, "optimization_summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

    print(f"Optimization complete. Final pipeline saved to {final_pipeline_path}")
    print(f"Overall improvement: {history.get('overall_improvement', 'N/A')}")
    print(f"Final adapter state: {final_adapter_state}")
