import os
import os.path as osp
from dataclasses import dataclass, field
from typing import List, Optional
import requests, time

import dspy
import sys
import json
sys.path.append(".")

import torch
from dotenv import load_dotenv
from peft import LoraConfig
from transformers import HfArgumentParser

from examples.pipelines import registered_pipeline
from examples.datasets import registered_dataset
from optimas.utils.load import load_model_and_tokenizer
from optimas.reward.model import RewardModel, EmbeddingSimilarityRewardModel
from optimas.optim.optimizer import CompoundAgentOptimizer
from optimas.reward.dataset import RewardDataset
from optimas.optim.args import OptimasArguments
from optimas.utils.logging import setup_logger
from optimas.reward.eval import eval_pipeline
from optimas.utils.lora import *

@dataclass
class ScriptArgs:
    """
    Comprehensive configuration class for script arguments with default values.
    """
    # Model and Pipeline Configuration
    run_name: str = "default"
    base_model_name: str = "meta-llama/Llama-3.1-8B-Instruct"
    hf_repo_or_local_dir: str = "snap-stanford/hotpotqa_four_agents_pipeline-preference_scorer"

    dataset: str = "hotpotqa"
    pipeline_name: str = "hotpotqa_four_agents_pipeline"

    # Paths and Directories
    state_dict_path : str = None
    state_dict_path_for_sampling: str = None
    pipeline_state_dict_path: str = None
    output_dir: str = "/dfs/project/kgrlm/multiagent_reward/trl/optim"
    dotenv_path: str = "/dfs/project/kgrlm/common/.env"
    modules_to_apply: List[str] = field(default_factory=lambda: ['all'])
    mode: str ='test' # 'val' or 'val+test'
    val_name: str = "val"

    # Hyper-parameter search
    global_hyper_param_search: bool = True

    # Optimas
    per_module_train_size: int = 50
    per_module_search_size: int = 20
    num_prompt_candidates: int = 10
    num_iterations: int = 2

    # rollout
    sample_size: int = 3

    # LoRA Configuration
    lora_r: int = 32
    lora_alpha: int = 16
    lora_dropout: float = 0.0
    lora_bias: str = "none"
    lora_target_modules: List[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ])

    # Optimization Configuration
    optimize_prompts: bool = True
    prompt_optimizer: str = "mipro"
    requires_permission_to_run: bool = False

    verbose: bool = True
    reward_model_for_optimization: bool = False
    reward_model_for_rollout: bool = False
    num_repeat: int = 3
    max_sample_workers: int = 4
    max_eval_workers: int = 4
    val_every_prompt_iter: int = 3
    val_every_ppo_ratio: float = 0.25

    # ─── PPO hyper-params ──────────────────────────────────────────────
    weight_optimizer: str = "none"
    ppo_train_steps: int = 800
    ppo_epochs: int = 4
    ppo_batch_size: int = 2
    ppo_learning_rate: float = 1e-4
    ppo_save_every: int = 0
    ppo_save_epoch_ratio: float = 0.5
    ppo_resume_adapter: Optional[str] = None
    ppo_base_model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"

    # ---- LoRA adapters for session and profiler ----
    session_adapter: str | None = None
    session_adapter_path: str | None = None
    profiler_adapter: str | None = None
    profiler_adapter_path: str | None = None

    # ---- SFT with embedding similarity reward model ----
    emb_sim_reward: bool = False
    emb_dir: str = "/dfs/project/kgrlm/multiagent_reward/trl/reward_emb_submit/embedding_cache"
    embedding_model: str = "text-embedding-3-small"
    margin_threshold:  float = 0.5

    # ---- GPU --------
    reward_device: str = "cuda:0"
    policy_device: str = "cuda:0"

    def post_init(self):
        """
        Post-initialization method to handle any necessary conversions.
        """
        # Convert any string "None" to actual None if needed
        for field_name, field_value in vars(self).items():
            if field_value == "None":
                setattr(self, field_name, None)


def optimize_pipeline(pipeline, reward_model, args):

    logger = setup_logger(__name__)

    trainset, valset, testset = registered_dataset[args.dataset](**vars(args))

    # Prepare dataset
    train_dataset = RewardDataset(
        hf_repo_or_local_dir=args.hf_repo_or_local_dir,
        pipeline=pipeline,
        original_trainset=trainset+valset+testset,
    ).to_inputs_only_dataset()

    # Prepare optimization arguments
    optimas_args = OptimasArguments(
        optimize_prompts=args.optimize_prompts,
        prompt_optimizer=args.prompt_optimizer,
        per_module_train_size=args.per_module_train_size,
        per_module_search_size=args.per_module_search_size,
        num_prompt_candidates=args.num_prompt_candidates,
        requires_permission_to_run=args.requires_permission_to_run,
        global_hyper_param_search=args.global_hyper_param_search,
        verbose=args.verbose,
        output_dir=args.output_dir,
        weight_optimizer=args.weight_optimizer,
        modules_to_apply=args.modules_to_apply,
        ppo_train_steps=args.ppo_train_steps,
        ppo_epochs=args.ppo_epochs,
        ppo_batch_size=args.ppo_batch_size,
        ppo_learning_rate=args.ppo_learning_rate,
        ppo_save_every=args.ppo_save_every,
        ppo_save_epoch_ratio=args.ppo_save_epoch_ratio,
        ppo_resume_adapter=args.ppo_resume_adapter,
        ppo_base_model_name=args.ppo_base_model_name,
        val_every_prompt_iter=args.val_every_prompt_iter,
        val_every_ppo_ratio=args.val_every_ppo_ratio,
        policy_device=args.policy_device,
    )

    # Initialize and run optimizer
    optimizer = CompoundAgentOptimizer(
        args=optimas_args,
        pipeline=pipeline,
        reward_model=reward_model,
        train_dataset=train_dataset, # reward dataset
        original_trainset=trainset, # original dataset
        val_dataset=valset,
        val_metrics_path=args.val_metrics_path,
    )

    # Optimize the pipeline
    optimized_pipeline = optimizer.optimize()

    # Print and potentially further process the optimized pipeline
    logger.info(f"Optimized Pipeline: {optimized_pipeline}", )
    logger.info(f"Optimized State Dict: {optimized_pipeline.state_dict()}")
    torch.save(optimized_pipeline.state_dict(), osp.join(args.output_dir, "pipeline_state_dict.pth"))

    return optimized_pipeline


def load_reward_model(pipeline, args):
    # Create LoRA configuration
    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias=args.lora_bias,
        task_type="CAUSAL_LM",
        init_lora_weights="gaussian",
        target_modules=args.lora_target_modules
    )
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(
        args.base_model_name,
        peft_config=peft_config,
        bnb_config=None,
        state_dict_path=args.state_dict_path
    )

    # Create reward model
    reward_model = RewardModel(model, tokenizer, pipeline)
    return reward_model

def load_reward_model_for_sampling(pipeline, state_dict_path_for_sampling):
    # Create LoRA configuration
    peft_config = LoraConfig(
        r=32,
        lora_alpha=16,
        lora_dropout=0.0,
        bias="none",
        task_type="CAUSAL_LM",
        init_lora_weights="gaussian",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"]
    )
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(
        "meta-llama/Llama-3.1-8B-Instruct",
        peft_config=peft_config,
        bnb_config=None,
        state_dict_path=state_dict_path_for_sampling
    )

    # Create reward model
    reward_model = RewardModel(model, tokenizer, pipeline)
    return reward_model


if __name__ == "__main__":
    # Create script arguments instance
    parser = HfArgumentParser(ScriptArgs)
    args = parser.parse_args_into_dataclasses()[0]
    print(args)

    # Load environment variables
    load_dotenv(args.dotenv_path)

    args.output_dir = osp.join(args.output_dir, args.dataset, args.pipeline_name, args.run_name)
    os.makedirs(args.output_dir, exist_ok=True)

    args.val_metrics_path = osp.join(args.output_dir, "val_metrics.json")

    logger = setup_logger(__name__, log_file=osp.join(args.output_dir, "output.log"))

    try:

        host = os.getenv("VLLM_HOST", "localhost")
        port = int(os.getenv("VLLM_PORT", "8001"))

        # HOT‑LOAD adapters
        if args.session_adapter and args.session_adapter_path:
            load_lora_adapter(args.session_adapter, args.session_adapter_path, host, port)
        if args.profiler_adapter and args.profiler_adapter_path:
            load_lora_adapter(args.profiler_adapter, args.profiler_adapter_path, host, port)

        # Get the pipeline
        print(f'{args.pipeline_name=}')
        if args.pipeline_name == 'amazon_next_item_selection_local_pipeline':
            print(f'{args.session_adapter=}, {args.profiler_adapter=}')
            pipeline = registered_pipeline[args.pipeline_name](
                session_adapter=args.session_adapter,
                profiler_adapter=args.profiler_adapter,
                log_dir=args.output_dir,
                max_sample_workers=args.max_sample_workers,
                max_eval_workers=args.max_eval_workers
            )
        else:
            pipeline = registered_pipeline[args.pipeline_name](
                log_dir=args.output_dir,
                max_sample_workers=args.max_sample_workers,
                max_eval_workers=args.max_eval_workers
                )
        cur_pipeline_state_dict = pipeline.state_dict()

        logger.info(f"Pipeline: {pipeline}", )
        logger.info(f"Current State Dict: {cur_pipeline_state_dict}")
        torch.save(cur_pipeline_state_dict, osp.join(args.output_dir, "pipeline_state_dict.pth.bak"))

        # Evaluate the optimized pipeline
        trainset, valset, testset = registered_dataset[args.dataset](**vars(args))

        if args.emb_sim_reward:
            rd = RewardDataset(
                hf_repo_or_local_dir=args.hf_repo_or_local_dir,
                pipeline=pipeline,
                original_trainset=trainset + valset + testset,
            )
            reward_model = EmbeddingSimilarityRewardModel(
                dataset_name=args.dataset,
                        pipeline=pipeline,
                        reward_dataset=rd,
                        embedding_model=args.embedding_model,
                        cache_dir=args.emb_dir)
        else:
            if args.state_dict_path:
                pipeline.max_eval_workers = 1
                logger.info(f"Load reward model from {args.state_dict_path}")
                reward_model = load_reward_model(pipeline, args)
            else:
                reward_model = None

        # switch device
        if args.reward_model_for_optimization:
            device_idx = int(args.reward_device.split(":")[-1])
            reward_model.to(f"cuda:{device_idx}")

        print(f'{args.reward_model_for_optimization}')
        if args.reward_model_for_optimization:
            # Run the optimization function
            pipeline = optimize_pipeline(pipeline, reward_model, args)
            args.pipeline_state_dict_path = osp.join(args.output_dir, "pipeline_state_dict.pth")
            logger.info(f"Pipeline saved to {args.pipeline_state_dict_path}")

        if args.pipeline_state_dict_path:
            logger.info(f"Loading pipeline from {args.pipeline_state_dict_path}")
            pipeline_state_dict = torch.load(args.pipeline_state_dict_path)

            pipeline.load_state_dict(pipeline_state_dict)
            logger.info(f"State dict: {json.dumps(pipeline_state_dict, indent=2)}")

        if args.reward_model_for_rollout:
            kwargs = {
                "sample_size": args.sample_size,
                "modules_to_apply": args.modules_to_apply
            }
        else:
            kwargs = {"sample_size": 1, "modules_to_apply": ["all"]}

        if args.state_dict_path_for_sampling:

            reward_model_for_sampling = load_reward_model_for_sampling(pipeline, args.state_dict_path_for_sampling)
            if "context_model_selector" in pipeline.modules:
                if hasattr(pipeline.modules["context_model_selector"], "set_reward_model"):
                    pipeline.modules["context_model_selector"].set_reward_model(reward_model_for_sampling)
                    # logger.info("Attached reward model to context_model_selector")
            if "solver_model_selector" in pipeline.modules:
                if hasattr(pipeline.modules["solver_model_selector"], "set_reward_model"):
                    pipeline.modules["solver_model_selector"].set_reward_model(reward_model_for_sampling)

        pipeline.register_rm(rm=reward_model, **kwargs)
        # with pipeline.context({module_name: {"randomize_search_variable": args.randomize_search_variable} for module_name in pipeline.modules()}):
        if 'val' in args.mode:
            metrics, preds = eval_pipeline(
                pipeline=pipeline,
                testset=valset,
                num_repeat=args.num_repeat,

            )
            with open(os.path.join(args.output_dir, f"val_metrics_{args.val_name}.json"), "w") as f:
                json.dump(metrics, f, sort_keys=True, indent=2)
        if 'test' in args.mode:
            metrics, preds = eval_pipeline(
                pipeline=pipeline,
                testset=testset,
                num_repeat=args.num_repeat
            )
            if args.val_name == 'val':
                with open(
                    os.path.join(args.output_dir, f"test_metrics.json"), "w"
                ) as f:
                    json.dump(metrics, f, sort_keys=True, indent=2)
            else:
                with open(
                    os.path.join(args.output_dir, f"test_metrics_{args.val_name}.json"), "w"
                ) as f:
                    json.dump(metrics, f, sort_keys=True, indent=2)
        print(metrics)
    finally:
        if args.session_adapter:
            unload_lora_adapter(args.session_adapter, host, port)
        if args.profiler_adapter:
            unload_lora_adapter(args.profiler_adapter, host, port)
