import copy
import os
import re
import json
import wandb
import shutil
import numpy as np
import torch
import importlib.util
from pathlib import Path
from typing import List, Optional, Callable
from transformers import TrainerCallback

from optimas.utils.save import save_model_and_tokenizer
from optimas.utils.logging import setup_logger
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.reward.eval import eval_pipeline, PerModuleEvaluator
from optimas.reward.model import RewardModel
import time

logger = setup_logger(__name__)

PREFIX_STATE_DICT_DIR = "full"
PREFIX_CHECKPOINT_DIR = "checkpoint"


# Integration functions:
def is_wandb_available():
    # any value of WANDB_DISABLED disables wandb
    ENV_VARS_TRUE_VALUES = {"1", "ON", "YES", "TRUE"}
    if os.getenv("WANDB_DISABLED", "").upper() in ENV_VARS_TRUE_VALUES:
        logger.warning(
            "Using the `WANDB_DISABLED` environment variable is deprecated and will be removed in v5. Use the "
            "--report_to flag to control the integrations used for logging result (for instance --report_to none)."
        )
        return False
    return importlib.util.find_spec("wandb") is not None


class PerModuleSaveEvalCallback(TrainerCallback):
    """
    A TrainerCallback that saves model checkpoints, manages full model backups, and tracks the best model 
    based on evaluation metrics.
    """
    def __init__(
        self,
        tokenizer,
        repo_name: str,
        metric_for_best_model: str,
        pipeline: CompoundAgentPipeline = None,
        test_ds: str = None,
        static_rollouts: List = None,
        push_to_hub: bool = False,
        criteria: Optional[Callable[[str], bool]] = None,
        static_rollouts_cache_path: str = None,
        save_model_per_module: bool = True,
        test_best_model_only: bool = True,
        test_static_rollouts_per_module: bool = True,
    ):
        """
        Initializes the callback.
        Args:
            tokenizer: Tokenizer to save along with the model.
            repo_name (str): Repository name for pushing to the hub.
            push_to_hub (bool, optional): Whether to push model checkpoints to the hub. Default is False.
            criteria (callable, optional): Function to filter which model parameters to save.
                                           Defaults to saving LoRA weights and 'score.weight'.
        """
        self.tokenizer = tokenizer
        self.repo_name = repo_name

        self.pipeline = pipeline
        self.module_names = [m for m in pipeline.modules if pipeline.modules[m].optimizable] if pipeline else []

        self.test_ds = test_ds
        self.static_rollouts = static_rollouts
        self.test_static_rollouts_per_module = test_static_rollouts_per_module
        self.static_rollouts_cache_path = static_rollouts_cache_path
        
        if self.test_ds is not None:
            self.num_splits = torch.cuda.device_count()
            per_device_eval_size = len(test_ds) // self.num_splits
            self.device_idx_mapping = {
                gpu_id: range(i * per_device_eval_size, (i + 1) * per_device_eval_size) 
                for i, gpu_id in enumerate(range(self.num_splits - 1))
            }
            self.device_idx_mapping[self.num_splits - 1] = range(
                (self.num_splits - 1) * per_device_eval_size, len(test_ds)
            )
            
        self.metric_for_best_model = metric_for_best_model
        self.save_model_per_module = save_model_per_module
        self.criteria = criteria or (lambda x: "score.weight" in x.lower() or "lora" in x.lower())
        
        self.push_to_hub = push_to_hub
        self.test_best_model_only = test_best_model_only
    
    def on_evaluate(self, args, state, control, model, metrics=None, **kwargs):
        """
        Evaluates the model during training, with both overall pipeline evaluation
        and per-module evaluation.
        """
        best_step = self._get_best_step_from_log_history(
            state.log_history, 
            self.metric_for_best_model, 
            higher_is_better=not "loss" in self.metric_for_best_model
        )
        print(metrics)

        if (
            is_wandb_available() 
            and self.test_ds 
            and metrics 
            and "completion" in metrics
            and (
                not self.test_best_model_only
                or best_step == state.global_step
            )
        ):
            indices = self.device_idx_mapping[args.process_index]
            world_size = torch.distributed.get_world_size()

            test_ds = [d for i, d in enumerate(self.test_ds) if i in indices]
            test_ds_dict = {i: d for i, d in enumerate(self.test_ds) if i in indices}
            static_rollouts = [r for i, r in enumerate(self.static_rollouts) if i in indices]
            static_rollouts_dict = {i: r for i, r in enumerate(self.static_rollouts) if i in indices}

            logger.info(f"Process {args.process_index} evaluating {len(indices)} examples on device {model.device}")            

            metrics = self._test_static_rollout(model, test_ds, static_rollouts)
            metrics_tensor = torch.tensor([metrics]).cuda() 
            gathered_metrics = [torch.zeros_like(metrics_tensor) for _ in range(world_size)]
            torch.distributed.all_gather(gathered_metrics, metrics_tensor)
            all_metrics = torch.cat(gathered_metrics, dim=0).cpu().numpy()

            if self.test_static_rollouts_per_module:
                per_module_metrics, hit_res, _ = self._test_static_rollout_per_module(model, test_ds_dict, static_rollouts_dict)

                per_module_values = [per_module_metrics[name] for name in self.module_names]
                per_module_tensor = torch.tensor(per_module_values).cuda()
                hit_res_values = [hit_res[name] for name in self.module_names]
                hit_res_tensor = torch.tensor(hit_res_values).cuda()

                gathered_per_module = [torch.zeros_like(per_module_tensor) for _ in range(world_size)]
                gathered_hit_res = [torch.zeros_like(hit_res_tensor) for _ in range(world_size)]
                
                torch.distributed.all_gather(gathered_per_module, per_module_tensor)
                torch.distributed.all_gather(gathered_hit_res, hit_res_tensor)

                all_per_module = torch.cat(gathered_per_module, dim=0).cpu().numpy()
                all_hit_res = torch.cat(gathered_hit_res, dim=0).cpu().numpy()

            # Log the aggregated metrics if needed
            if state.is_world_process_zero:
                wandb.log({"test/static_rollouts": all_metrics.mean().item()})

                if self.test_static_rollouts_per_module:
                    all_per_module = all_per_module.reshape(world_size, len(self.module_names))
                    per_module_means = all_per_module.mean(axis=0)
                    per_module_dict = {f"test/static_rollouts_{name}": value for name, value in zip(self.module_names, per_module_means)}
                    wandb.log(per_module_dict)

                    all_hit_res = all_hit_res.reshape(world_size, len(self.module_names))
                    hit_res_means = all_hit_res.mean(axis=0)
                    hit_res_dict = {f"test/hit_res_{name}": value for name, value in zip(self.module_names, hit_res_means)}
                    wandb.log(hit_res_dict)

    def on_train_begin(self, args, state, control, model, **kwargs):
        """
        Initializes the callback.
        """
        if not state.is_world_process_zero:
            return

        # Save the initial model and tokenizer
        self.init_model_path = os.path.join(args.output_dir, f"{PREFIX_STATE_DICT_DIR}-init")
        save_model_and_tokenizer(
            model, self.tokenizer, self.init_model_path,
            repo_name=self.repo_name, push_to_hub=self.push_to_hub, criteria=self.criteria
        )

    def on_train_end(self, args, state, control, model, **kwargs):
        """
        Saves the final full model and renames the best checkpoint based on evaluation metrics.
        This method runs only on the primary process (LOCAL_RANK=0).
        """
        self.on_evaluate(args, state, control, model, **kwargs)

        if not state.is_world_process_zero:
            return
        
        last_checkpoint = os.path.join(args.output_dir, f"{PREFIX_STATE_DICT_DIR}-last")
        save_model_and_tokenizer(
            model, self.tokenizer, last_checkpoint, 
            repo_name=self.repo_name, push_to_hub=self.push_to_hub, criteria=self.criteria
        )
        if state.best_model_checkpoint:
            # Rename best model checkpoint
            best_checkpoint_name = os.path.basename(state.best_model_checkpoint).replace(PREFIX_CHECKPOINT_DIR, PREFIX_STATE_DICT_DIR)
            best_model_checkpoint = os.path.join(args.output_dir, best_checkpoint_name)
            
            model_info = {}
            if best_model_checkpoint:
                model_info.update({
                    "best_metric": state.best_metric,
                    "best_model_step": int(best_model_checkpoint.split("-")[-1])
                })
                best_model_path = os.path.join(args.output_dir, f"{PREFIX_STATE_DICT_DIR}-best")
                os.rename(best_model_checkpoint, best_model_path)

            if self.save_model_per_module:
                for m in self.module_names:
                    if self.best_step_per_module[m]:
                        per_module_step_checkpoint = os.path.join(args.output_dir, f"{PREFIX_STATE_DICT_DIR}-{m}-{self.best_step_per_module[m]}")
                        per_module_best_checkpoint = os.path.join(args.output_dir, f"{PREFIX_STATE_DICT_DIR}-{m}-best")
                        os.rename(per_module_step_checkpoint, per_module_best_checkpoint)
                        model_info.update({f"best_{m}_step": self.best_step_per_module[m]})
        else:
            os.rename(self.init_model_path, os.path.join(args.output_dir, f"{PREFIX_STATE_DICT_DIR}-best"))
            model_info = {"best_metric": None, "best_model_step": 0}

        if is_wandb_available():
            table = wandb.Table(columns=["Metric", "Value"])
            for key, value in model_info.items():
                table.add_data(key, value)
                
            wandb.log({"model_results": table})

        with open(os.path.join(args.output_dir, "model_info.json"), "w") as f:
            json.dump(model_info, f, indent=4)

    def _get_best_step_from_log_history(self, log_history, metric_key, higher_is_better=True) -> int:
        """
        Retrieves the best model checkpoint step based on the evaluation metrics.

        Args:
            log_history (list): List of evaluation metrics.
            metric_key (str): Key to retrieve the metric from the log history.

        Returns:
            int: Step of the best model checkpoint.
        """
        best_metric = None
        best_step = None
        for log in log_history:
            if metric_key in log:
                metric = log[metric_key]
                if best_metric is None or (higher_is_better and metric > best_metric) or (not higher_is_better and metric < best_metric):
                    best_metric = metric
                    best_step = log["step"]
        return best_step

    def on_save(self, args, state, control, model, **kwargs):
        """
        Saves a model checkpoint at the current training step and manages checkpoint rotation.
        This method runs only on the primary process (LOCAL_RANK=0).
        """
        if not state.is_world_process_zero:
            return

        step_checkpoint = os.path.join(args.output_dir, f"{PREFIX_STATE_DICT_DIR}-{state.global_step}")
        save_model_and_tokenizer(
            model, self.tokenizer, step_checkpoint,
            repo_name=f"{self.repo_name}-{state.global_step}", push_to_hub=self.push_to_hub,
            criteria=self.criteria
        )
        # Identify best model checkpoint
        if state.best_model_checkpoint:
            best_checkpoint_name = os.path.basename(state.best_model_checkpoint).replace(PREFIX_CHECKPOINT_DIR, PREFIX_STATE_DICT_DIR)
            best_model_checkpoint = os.path.join(args.output_dir, best_checkpoint_name)
        else:
            best_model_checkpoint = None
        self._rotate_checkpoints(args, state, best_model_checkpoint=best_model_checkpoint, prefix=PREFIX_STATE_DICT_DIR)
        
        if self.save_model_per_module:
            self.best_step_per_module = {
                m: self._get_best_step_from_log_history(
                    state.log_history, 
                    self.metric_for_best_model.replace("eval_", f"eval_{m}_"),
                    higher_is_better=not "loss" in self.metric_for_best_model
                ) for m in self.module_names
            }

            for m in self.module_names:
                if self.best_step_per_module[m] == state.global_step:
                    per_module_step_checkpoint = os.path.join(args.output_dir, f"{PREFIX_STATE_DICT_DIR}-{m}-{state.global_step}")

                    save_model_and_tokenizer(
                        model, self.tokenizer, per_module_step_checkpoint,
                        repo_name=f"{self.repo_name}-{m}-{state.global_step}", push_to_hub=self.push_to_hub,
                        criteria=self.criteria
                    )
                    self._rotate_checkpoints(args, state, best_model_checkpoint=best_model_checkpoint, prefix=f"{PREFIX_STATE_DICT_DIR}-{m}")

    def _test_static_rollout(self, model, test_ds, static_rollouts) -> float:
        """
        Evaluates the static rollout pipeline on the evaluation dataset.
        """
        rm = RewardModel(model, self.tokenizer, pipeline=self.pipeline)
        self.pipeline.register_rm(rm, modules_to_apply=['all'])
        metrics, _ = eval_pipeline(self.pipeline, test_ds, static_rollouts)
        return metrics

    def _rotate_checkpoints(self, args, state, best_model_checkpoint, prefix=PREFIX_STATE_DICT_DIR) -> None:
        """
        Rotates checkpoints to maintain a maximum number of checkpoints.

        Args:
            args: Trainer arguments.
            state: Trainer state.
            best_model_checkpoint (str): Best model checkpoint path.
            prefix (str): Prefix for the checkpoint directory.            
        """
        if not args.save_total_limit or args.save_total_limit <= 0:
            return

        full_checkpoints_sorted = self._sorted_full_checkpoints(
            args.output_dir, state, 
            best_model_checkpoint=best_model_checkpoint, 
            prefix=prefix
        )
        if len(full_checkpoints_sorted) <= args.save_total_limit:
            return
        # Adjust limit to prevent deleting the best checkpoint
        save_limit = args.save_total_limit
        if best_model_checkpoint and save_limit == 1 and full_checkpoints_sorted[-1] != best_model_checkpoint:
            save_limit = 2
        # Delete excess checkpoints
        to_delete = full_checkpoints_sorted[:max(0, len(full_checkpoints_sorted) - save_limit)]
        for checkpoint in to_delete:
            print(f"Deleting outdated checkpoint: {checkpoint}")
            shutil.rmtree(checkpoint, ignore_errors=True)

    def _sorted_full_checkpoints(self, output_dir, state, best_model_checkpoint: str, prefix: str) -> tuple[Optional[str], List[str]]:
        """
        Returns the sorted full model checkpoints and the best model checkpoint if available.

        Args:
            state: Trainer state containing the best model checkpoint.
            best_model_checkpoint (str): Best model checkpoint path.
            prefix (str): Prefix for the checkpoint directory.

        Returns:
            tuple: Sorted full model checkpoints.
        """

        full_checkpoints = [str(x) for x in Path(output_dir).glob(f"{prefix}-*") if x.is_dir()]
        sorted_checkpoints = sorted(
            (int(re.search(rf"{prefix}-(\d+)", path).group(1)), path)
            for path in full_checkpoints if re.search(rf"{prefix}-(\d+)", path)
        )

        sorted_checkpoints = [path for _, path in sorted_checkpoints]

        # Ensure best checkpoint is not deleted
        if best_model_checkpoint in sorted_checkpoints:
            sorted_checkpoints.append(sorted_checkpoints.pop(sorted_checkpoints.index(best_model_checkpoint)))

        return sorted_checkpoints
    
    def _test_static_rollout_per_module(self, model, test_ds, static_rollouts):
        """
        Evaluates each module separately in the static rollout pipeline.
        Evaluation is done per example.
        
        Args:
            model: The reward model to use for evaluation
            test_ds: The evaluation dataset
            static_rollouts: The static rollouts dataset
            
        Returns:
            per_module_metrics: Dictionary mapping module names to evaluation metrics
        """
        evaluator = PerModuleEvaluator(
            pipeline=self.pipeline,
            test_ds=test_ds,
            static_rollouts=static_rollouts,
            tokenizer=self.tokenizer,
            static_rollouts_cache_path=self.static_rollouts_cache_path
        )
        
        return evaluator.evaluate_model(model, score_type='avg_score')
