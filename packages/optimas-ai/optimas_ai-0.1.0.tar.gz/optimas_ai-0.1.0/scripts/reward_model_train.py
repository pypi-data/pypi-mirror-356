
import os
import wandb
import warnings
import sys
import torch
from transformers import (
    AutoModelForSequenceClassification, AutoTokenizer, HfArgumentParser, BitsAndBytesConfig, EarlyStoppingCallback
)
import copy
from dataclasses import dataclass, field
from datasets import load_dataset
from peft import LoraConfig
from typing import List, Optional
import os.path as osp
import json

sys.path.append(".")
from optimas.external import RewardConfig, RewardTrainer
from optimas.utils.load import load_model_and_tokenizer
from optimas.reward.dataset import RewardDataset
from optimas.utils.save import save_model_and_tokenizer
from optimas.reward.finetune import run_finetune
from examples.pipelines import registered_pipeline
from optimas.reward.callback import PerModuleSaveEvalCallback
from examples.datasets import registered_dataset
from optimas.utils.logging import setup_logger

# Define script arguments
@dataclass
class ScriptArgs:
    base_model_name: str = "meta-llama/Llama-3.1-8B-Instruct"
    hf_repo_or_local_dir: str = ""
    pipeline_name: str = ""
    dataset: str = ""
    train_multi_head: bool = True
    dataset_format: str = ""
    output_dir: str = ""
    logging_dir: str = ""
    wandb_entity: str = ""
    wandb_project: str = ""
    wandb_run_name: str = ""
    per_device_train_batch_size: int = 8
    per_device_eval_batch_size: int = 4
    gradient_accumulation_steps: int = 1
    torch_empty_cache_steps: int = 1
    max_steps: int = -1
    learning_rate: float = 5e-5
    early_stopping_patience: int = 512
    num_train_epochs: int = 20
    max_length: int = 2048
    logging_steps: int = 10
    eval_steps: int = 10
    save_steps: int = 10
    eval_strategy: str = "steps"
    metric_for_best_model: str = "eval_loss"
    lora_r: int = 16
    lora_alpha: int = 8
    lora_dropout: float = 0.05
    eval_ratio: float = 0.1
    report_to: str = "wandb"
    save_total_limit: int = 3
    warmup_steps: int = 0
    weight_decay: float = 0.0
    state_dict_path: str = None
    add_margin: bool = False
    push_to_hub: bool = True
    load_in_4bit: bool = False
    load_in_8bit: bool = False
    module_name_lst: List[str] = None
    load_best_model_at_end: bool = True
    use_score_scaling: bool = False
    use_score_norm: bool = False
    use_lora: bool = False
    static_rollouts_path: Optional[str] = None
    static_rollouts_cache_path: str = None
    save_model_per_module: bool = True
    test_best_model_only: bool = True
    test_static_rollouts_per_module: bool = False

    def __post_init__(self):
        # Convert all attributes with value "None" (string) to actual None
        for field_name, field_value in self.__dict__.items():
            if field_value == "None":
                setattr(self, field_name, None)


def main():
    parser = HfArgumentParser(ScriptArgs)
    args = parser.parse_args_into_dataclasses()[0]
    logger = setup_logger(__name__, log_file=osp.join(args.output_dir, "output.log"))

    if os.environ.get('LOCAL_RANK', '0') == '0':
        wandb.init(
            project=args.wandb_project,
            entity=args.wandb_entity,
            name=args.wandb_run_name,
            config=args,
            save_code=True
        )

    if args.load_in_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=False,
            bnb_4bit_compute_dtype=torch.bfloat16
        )
    elif args.load_in_8bit:
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_quant_type="nf8",
            bnb_8bit_use_double_quant=False,
            bnb_8bit_compute_dtype=torch.bfloat16
        )
    else:
        bnb_config = None

    if args.use_lora:
        peft_config = LoraConfig(
            r=args.lora_r,
            lora_alpha=args.lora_alpha,
            lora_dropout=args.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM",
            init_lora_weights="gaussian",
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                            "gate_proj", "up_proj", "down_proj"]
        )
    else:
        peft_config = None

    # Configure training
    training_args = RewardConfig(
        do_train=True,
        output_dir=args.output_dir,
        logging_dir=args.logging_dir,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        num_train_epochs=args.num_train_epochs,
        max_length=args.max_length,
        logging_steps=args.logging_steps,
        eval_steps=args.eval_steps,
        save_steps=args.save_steps,
        eval_strategy=args.eval_strategy,
        push_to_hub=args.push_to_hub,
        report_to=args.report_to,
        torch_empty_cache_steps=args.torch_empty_cache_steps,
        max_steps=args.max_steps,
        save_total_limit=args.save_total_limit,
        warmup_steps=args.warmup_steps,
        weight_decay=args.weight_decay,
        metric_for_best_model=args.metric_for_best_model,
        load_best_model_at_end=args.load_best_model_at_end,
        use_score_scaling=args.use_score_scaling,
        use_score_norm=args.use_score_norm,
        ddp_find_unused_parameters=False,
    )

    pipeline = registered_pipeline[args.pipeline_name]()
    trainset, valset, testset = registered_dataset[args.dataset](**vars(args))

    reward_dataset = RewardDataset(
        args.hf_repo_or_local_dir, pipeline,
        original_trainset=trainset + valset
        )
    ds = reward_dataset.to_format(
        eval_ratio=args.eval_ratio,
        format=args.dataset_format,
        add_margin=args.add_margin
    )

    num_labels = len(pipeline.optimizable_modules) if args.train_multi_head else 1
    logger.info(f"[reward_model_train] Setting the number of output dims to {num_labels}")

    model, tokenizer = load_model_and_tokenizer(
        args.base_model_name,
        peft_config=peft_config,
        bnb_config=bnb_config,
        model_class=AutoModelForSequenceClassification,
        state_dict_path=args.state_dict_path,
        num_labels=num_labels
    )

    ############ Callback ############
    if args.static_rollouts_path is not None:
        train_ds, val_ds, test_ds = registered_dataset[args.dataset](**vars(args))
        with open(args.static_rollouts_path, 'r') as f:
            static_rollouts_dict = json.load(f)
            static_rollouts_dict = {int(k): v for k, v in static_rollouts_dict.items()}
            test_ds = [example for idx, example in enumerate(test_ds) if idx in static_rollouts_dict]
            static_rollouts = list(static_rollouts_dict.values())
    else:
        test_ds, static_rollouts = None, None

    eval_callback = PerModuleSaveEvalCallback(
        tokenizer=tokenizer,
        pipeline=pipeline,
        test_ds=test_ds,
        repo_name=args.hf_repo_or_local_dir,
        push_to_hub=args.push_to_hub,
        static_rollouts=static_rollouts,
        metric_for_best_model=args.metric_for_best_model,
        save_model_per_module=args.save_model_per_module,
        test_best_model_only=args.test_best_model_only,
        test_static_rollouts_per_module=args.test_static_rollouts_per_module,
        static_rollouts_cache_path=args.static_rollouts_cache_path,
    )
    early_stopping_callback = EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience)
    
    ############ Train model ############
    logger.info(f"[reward_model_train] {pipeline.optimizable_modules=}")

    trainer = run_finetune(
        ds, model, tokenizer, training_args,
        train_last_layer=True, 
        callbacks=[eval_callback, early_stopping_callback], format=args.dataset_format,
        module_to_idx=pipeline.optimizable_module_to_idx
    )

    ############ SAVING ############
    if training_args.eval_strategy != "no":
        metrics = trainer.evaluate()
        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)

    wandb.finish()

if __name__ == "__main__":
    main()
