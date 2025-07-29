import copy
import torch
from typing import Any, Dict, List
from datasets import DatasetDict
from optimas.optim.args import OptimasArguments
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.reward.model import RewardModel
from optimas.utils.logging import setup_logger
from optimas.utils.parallel import run_parallel_tasks
from optimas.utils.prediction import Prediction
from optimas.optim.opro import OPRO
from optimas.optim.ppo import train_ppo, build_prompt
from optimas.utils.example import Example
from optimas.utils.lora import *
import json
import dspy
import itertools
import os

logger = setup_logger(__name__)

class CompoundAgentOptimizer:
    """
    An optimizer class to optimize the variables (e.g., prompts and parameters) of a CompoundAgentPipeline.
    """

    def __init__(
        self,
        args: OptimasArguments,
        pipeline: CompoundAgentPipeline,
        reward_model: RewardModel,
        train_dataset: DatasetDict,
        original_trainset: DatasetDict,
        val_dataset: DatasetDict | None = None,
        val_metrics_path: str | None = None,
    ):
        """
        Initialize the Optimizer.

        Args:
            pipeline (CompoundAgentPipeline): The pipeline to optimize.
            train_dataset (list): A dataset of input-output pairs for training or evaluation.
            args (OptimasArguments): Configuration arguments for the optimization process.
        """
        self.args = args
        self.pipeline = pipeline
        assert self.pipeline.rm is None or self.pipeline.sample_size == 1, "Pipeline already has a reward model. If sample size > 1, it would affect the optimization "

        self.train_dataset = train_dataset
        self.val_dataset = val_dataset
        self.val_metrics_path = val_metrics_path
        self.hyper_param_train_dataset = original_trainset[:self.args.per_module_search_size]
        # Load the reward model and tokenizer
        self.reward_model = reward_model

        optimizable_modules = [
            module_name for module_name, module in pipeline.modules.items()
            if module.optimizable
        ]
        visible_modules = list(pipeline.modules.keys()) if "all" in args.modules_to_apply else args.modules_to_apply
        self.modules_to_apply = list(set(visible_modules) & set(optimizable_modules))

    def optimize(self) -> Any:
        """
        Optimize the CompoundAgentPipeline.

        Returns:
            CompoundAgentPipeline: The optimized pipeline with updated variables.
        """
        for name, module in self.pipeline.modules.items():
            if not name in self.modules_to_apply:
                logger.info(f"Module {name} is not in the modules to apply. Skipping...")
                continue

            print(f'{self.args.ppo_epochs=}')
            if module.variable == 'local_lm' and int(self.args.ppo_epochs) > 0:
                print(f"Optimizing weights for module {name}...")
                self._optimize_weights(name)

            if isinstance(module.variable, str) and module.variable != 'local_lm':
                print(f"Optimizing prompt for module {name}...")
                self._optimize_prompts(name)

            if isinstance(module.variable, dict) and self.args.global_hyper_param_search:
                print(f"Optimizing hyperparameters for module {name}...")
                self._optimize_hyperparameters(name)

        return self.pipeline

    def _optimize_weights(self, module_name: str) -> None:
        """
        Run PPO on the local LLM that backs `module_name` and
        drop the resulting LoRA adapter inside
        {args.output_dir}/ppo/{module_name}

        Then update the module to use the new adapter.
        """
        logger.info(f"[PPO] optimising weights for module «{module_name}»")
        module = self.pipeline.modules[module_name]

        # -------- paths ------------
        out_dir = os.path.join(self.args.output_dir, "ppo", module_name)
        os.makedirs(out_dir, exist_ok=True)

        # -------- reward-dataset → prompts for PPO ------------------------
        ds_inputs = self.train_dataset[module_name]

        def to_prompt(example):
            inp = example["input"]
            prompt = build_prompt(module_name, inp)
            return {"prompt": prompt, "orig": inp}

        if self.args.emb_sim_reward:
            reward_ds_for_ppo = ds_inputs.map(to_prompt, remove_columns=ds_inputs.column_names)
            reward_ds_for_ppo = reward_ds_for_ppo.select(range(min(self.args.per_module_train_size, len(reward_ds_for_ppo))))
        else:
            reward_ds_for_ppo = None

        val_ds_for_ppo = None
        if self.val_dataset is not None and module_name in self.val_dataset:
            val_ds_for_ppo = (self.val_dataset[module_name]
                            .map(to_prompt, remove_columns=self.val_dataset[module_name].column_names))

        # -------- call PPO trainer -------
        adapter_dir = train_ppo(
            module_name = module_name,
            base_model = self.args.ppo_base_model_name,
            reward_model = self.reward_model,
            output_dir = out_dir,
            batch_size = getattr(self.args, "ppo_batch_size", 2),
            ppo_epochs = getattr(self.args, "ppo_epochs", 1),
            train_steps = getattr(self.args, "ppo_train_steps", 800),
            learning_rate = getattr(self.args, "ppo_learning_rate", 1e-4),
            resume_adapter = getattr(self.args, "ppo_resume_adapter", None),
            save_every = getattr(self.args, "ppo_save_every", 0),
            save_epoch_ratio = getattr(self.args, "ppo_save_epoch_ratio", 0.25),
            reward_trainset = reward_ds_for_ppo,
            val_dataset = val_ds_for_ppo,
            val_metrics_path= self.val_metrics_path,
            val_every_ratio = self.args.val_every_ppo_ratio,
            args = self.args,
        )
        logger.info(f"[PPO] adapter ready at {adapter_dir}")

        # -------- update the pipeline to use the new adapter -----------------------------------

        # Find the best adapter
        best_adapter_path = get_adapter_from_ppo_output(out_dir, module_name)

        if best_adapter_path:
            adapter_id = f"{module_name}_optimized"

            host = os.getenv("VLLM_HOST", "localhost")
            port = int(os.getenv("VLLM_PORT", "8001"))

            success = load_lora_adapter(adapter_id, best_adapter_path, host, port)

            if success:
                if hasattr(module, 'set_adapter_path'):
                    module.set_adapter_path(best_adapter_path, adapter_id)
                else:
                    module.model_id = adapter_id
                    module._current_adapter_path = best_adapter_path

                logger.info(f"[PPO] Module {module_name} now using adapter {adapter_id} from {best_adapter_path}")
            else:
                logger.error(f"[PPO] Failed to load adapter {best_adapter_path} into vLLM")
        else:
            logger.warning(f"[PPO] No adapter found in PPO output directory")

    def _evaluate_hyperparameter(self, module_name, hyperparameter: dict, trainset: List, metric) -> float:
        """
        Evaluate the candidate prompt using the provided metric on the trainset.
        The `metric` expects (example, pred) or something similar.
        """
        cur_config = {module_name: {'variable': hyperparameter}}
        module = self.pipeline.modules[module_name]

        total_score = 0.0
        assert isinstance(module.variable, dict), "Module variable should be a dict."

        def process_single_example(module, example):
            """Process a single example through the module"""
            pred = module(**example.inputs())
            pred = Prediction(**pred)
            return pred

        # Prepare the task arguments
        task_args = [(module, example) for example in trainset]

        # Run in parallel

        with self.pipeline.context(cur_config):
            predictions = run_parallel_tasks(
                task_func=process_single_example,
                task_args=task_args,
                max_workers=self.args.max_sample_workers,  # Adjust based on your system capabilities
                use_tqdm=True,
                task_desc=f"Evaluate hp {hyperparameter}"
            )

        # Filter out None results (from errors) if needed
        predictions = [pred for pred in predictions if pred is not None]

        avg_score = metric(trainset, predictions)
        return avg_score

    def _optimize_hyperparameters(self, module_name):
        """
        Implement grid search on hyperparameters
        """

        module = self.pipeline.modules[module_name]
        old_variable = copy.deepcopy(module.variable)

        best_score = float('-inf')
        best_params = None

        param_keys = list(module.variable_search_space.keys())
        param_values = list(module.variable_search_space.values())
        param_combinations = list(itertools.product(*param_values))

        def metric_from_rm_or_global_metric(example, pred, trace=None):
            """
            Calculate metric for single instance or average for multiple instances.

            Args:
                example: Single example (dict/object) or list of examples
                pred: Single prediction (dict/object) or list of predictions
                trace: Optional trace information
                return_all: If True and input is list, return all scores instead of average

            Returns:
                float or list: Single score, average score, or list of all scores
            """

            # Ensure both are lists for uniform processing
            is_single = not (isinstance(example, list) or isinstance(pred, list))

            examples = [example] if not isinstance(example, list) else example
            preds = [pred] if not isinstance(pred, list) else pred

            # Validate same length
            if len(examples) == 1 and len(preds) > 1:
                examples = examples * len(preds)
            elif len(preds) == 1 and len(examples) > 1:
                preds = preds * len(examples)
            elif len(examples) != len(preds):
                raise ValueError(f"Length mismatch: {len(examples)} examples vs {len(preds)} predictions")

            # Check if using pipeline evaluation
            use_pipeline = all(
                all(field in p for field in self.pipeline.final_output_fields)
                for p in preds
            )

            if use_pipeline:
                scores = self.pipeline.evaluate_multiple(examples, preds)
            else:
                batch_pool = [{**{key: getattr(ex, key) for key in module.input_fields},
                              **{key: getattr(pr, key) for key in module.output_fields}} for ex, pr in zip(examples, preds)]

                # Evaluate
                scores = self.reward_model.batch_evaluate(module_name, batch_pool, sigmoid=True)
                logger.info(f'Reward values from reward model (batch): {scores}')

            return scores[0] if is_single else sum(scores) / len(scores)

        trainset_per_module = [
            Example(**example['input']).with_inputs(*module.input_fields) \
            for example in self.train_dataset[module_name]][:self.args.per_module_train_size]

        for i, param_combo in enumerate(param_combinations):
            params = dict(zip(param_keys, param_combo))
            avg_score = self._evaluate_hyperparameter(
                module_name,
                params,
                trainset_per_module,
                metric_from_rm_or_global_metric
            )

            if avg_score > best_score:
                best_score = avg_score
                best_params = params

            logger.info(
                f"Grid {i+1}/{len(param_combinations)} avg={avg_score:.4f} best={best_score:.4f}"
            )

            logger.info(f"Tried {i+1}/{len(param_combinations)} combinations. Current best: {best_score:.4f}")

        logger.info('FINISH PARAMETER SEARCH')
        logger.info(f'best score: {best_score:.4f}')
        logger.info(f'best parameters: {best_params}')
        logger.info(f"Old variable: {old_variable}")
        self.pipeline.modules[module_name].update(best_params)

    def _optimize_hyperparameters_full(self, module_name):
        """
        Implement grid search on hyperparameters
        """

        module = self.pipeline.modules[module_name]
        old_variable = copy.deepcopy(module.variable)

        best_score = float('-inf')
        best_params = None

        param_keys = list(module.variable_search_space.keys())
        param_values = list(module.variable_search_space.values())
        param_combinations = list(itertools.product(*param_values))

        for i, param_combo in enumerate(param_combinations):
            params = dict(zip(param_keys, param_combo))
            cur_config = {module_name: {'variable': params}}

            logger.info(f'{cur_config=}')
            with self.pipeline.context(cur_config):
                scores = self.pipeline.evaluate_multiple(self.hyper_param_train_dataset)
                avg_score = sum(scores) / len(scores)

            if avg_score > best_score:
                best_score = avg_score
                best_params = params

            logger.info(
                f"Grid {i+1}/{len(param_combinations)} avg={avg_score:.4f} best={best_score:.4f}"
            )

            logger.info(f"Tried {i+1}/{len(param_combinations)} combinations. Current best: {best_score:.4f}")

        logger.info('FINISH PARAMETER SEARCH')
        logger.info(f'best score: {best_score:.4f}')
        logger.info(f'best parameters: {best_params}')
        logger.info(f"Old variable: {old_variable}")
        self.pipeline.modules[module_name].update(best_params)

    def _optimize_prompts(self, module_name):
        """
        Optimize the prompts of the modules in the pipeline.
        """

        module = self.pipeline.modules[module_name]
        old_variable = copy.deepcopy(module.variable)

        def metric_from_rm_or_global_metric(example, pred, trace=None):
            """
            Calculate metric for single instance or average for multiple instances.

            Args:
                example: Single example (dict/object) or list of examples
                pred: Single prediction (dict/object) or list of predictions
                trace: Optional trace information
                return_all: If True and input is list, return all scores instead of average

            Returns:
                float or list: Single score, average score, or list of all scores
            """

            # Ensure both are lists for uniform processing
            is_single = not (isinstance(example, list) or isinstance(pred, list))

            examples = [example] if not isinstance(example, list) else example
            preds = [pred] if not isinstance(pred, list) else pred

            # Validate same length
            if len(examples) == 1 and len(preds) > 1:
                examples = examples * len(preds)
            elif len(preds) == 1 and len(examples) > 1:
                preds = preds * len(examples)
            elif len(examples) != len(preds):
                raise ValueError(f"Length mismatch: {len(examples)} examples vs {len(preds)} predictions")

            # Check if using pipeline evaluation
            use_pipeline = all(
                all(field in p for field in self.pipeline.final_output_fields)
                for p in preds
            )

            if use_pipeline:
                scores = self.pipeline.evaluate_multiple(examples, preds)
            else:
                batch_pool = [{**{key: getattr(ex, key) for key in module.input_fields},
                              **{key: getattr(pr, key) for key in module.output_fields}} for ex, pr in zip(examples, preds)]

                # Evaluate
                scores = self.reward_model.batch_evaluate(module_name, batch_pool, sigmoid=True)
                logger.info(f'Reward values from reward model (batch): {scores}')

            return scores[0] if is_single else sum(scores) / len(scores)

        trainset_per_module = [
            Example(**example['input']).with_inputs(*module.input_fields) \
            for example in self.train_dataset[module_name]][:self.args.per_module_train_size]
        if self.args.prompt_optimizer == "opro":
            logger.info(f"Running OPRO for module {module_name} ...")

            # Construct the OPRO instance
            opro_optimizer = OPRO(
                llm_model="gpt-4o-mini",
                temperature=0.7,
                max_new_tokens=512,
                metric=metric_from_rm_or_global_metric,
                num_prompt_candidates=self.args.num_prompt_candidates,
                max_sample_workers=self.args.max_sample_workers,
                meta_prompt_preamble=(
                    f"This module is meant to handle the task:\n{module.description}\n"
                    "We want to improve its prompt based on prior attempts.\n"
                ),
            )
            # Now variable only contains the system prompt
            initial_prompt_str = module.variable

            new_variable, prompt_score_pairs = opro_optimizer.compile(
                module=module,
                initial_prompt=initial_prompt_str,
                trainset=trainset_per_module
            )

            print(f"New variable: {new_variable}")

            # Debug prints
            logger.info(f"All prompt score pairs: {json.dumps(prompt_score_pairs, indent=2)}")
            logger.info(f"Old prompt: {old_variable}")
            logger.info(f"New prompt from OPRO: {new_variable}")

            # Update module with the new prompt
            module.update(new_variable)

        elif self.args.prompt_optimizer == "mipro":
            from dspy.teleprompt import MIPROv2

            logger.info(f'train size: {len(trainset_per_module)}')
            tp = MIPROv2(
                metric=metric_from_rm_or_global_metric,
                auto=self.args.auto,
                verbose=self.args.verbose,
                num_candidates=self.args.num_prompt_candidates,
                num_threads=4
            )
            old_signature_cls = module.signature_cls.with_instructions(module.variable)

            new_signature = tp.compile(
                dspy.Predict(old_signature_cls),
                trainset=trainset_per_module,
                requires_permission_to_run=self.args.requires_permission_to_run
            ).signature

            new_variable = new_signature.instructions

        elif self.args.prompt_optimizer == "copro":
            from dspy.teleprompt import COPRO

            eval_kwargs = dict(num_threads=1, display_progress=True)
            tp = COPRO(
                metric=metric_from_rm_or_global_metric,
                breadth=self.args.num_prompt_candidates,
                depth=self.args.copro_depth,
                verbose=self.args.verbose
            )
            old_signature_cls = module.signature_cls.with_instructions(module.variable)
            new_signature = tp.compile(
                dspy.Predict(old_signature_cls),
                trainset=trainset_per_module,
                eval_kwargs=eval_kwargs
            ).signature
            new_variable = new_signature.instructions
        else:
            raise ValueError(f"Invalid prompt optimizer: {self.args.prompt_optimizer}")

        if self.args.verbose:
            logger.info(f"Old prompt for module '{module_name}': {old_variable}")
            logger.info(f"Optimized prompt for module '{module_name}': {new_variable}")

        self.pipeline.modules[module_name].update(new_variable)
