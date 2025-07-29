
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading
from typing import List, Dict, Any
import numpy as np
import wikipedia
import os
import os.path as osp
import joblib
import argparse
from datetime import datetime
from dotenv import load_dotenv
import time
import sys
sys.path.append('.')
from examples.datasets import registered_dataset
from examples.pipelines import registered_pipeline
from optimas.arch.adapt import create_module_from_signature
from optimas.arch.base import BaseModule
from optimas.collect import generate_reward_model_trainset
from optimas.optim.optimizer import CompoundAgentOptimizer


if __name__ == "__main__":

    # args run_name name
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--method', type=str, default='preference_model_prior',
            choices=[
                'abs_value_llm_judge',
                'abs_value_naive_sample',
                'preference_modular_model_prior',
                'preference_scorer',
                ]
        )

        parser.add_argument('--dataset', type=str, default='hotpotqa')
        parser.add_argument('--pipeline', type=str, default="hotpotqa_two_agents")

        parser.add_argument('--train_size', type=int, default=1000)
        parser.add_argument('--judge_model', type=str, default='openai/gpt-4o')
        parser.add_argument('--sample_temperature', type=float, default=None)
        parser.add_argument('--push_to_hub', action='store_true', help='push to hub')
        parser.add_argument('--max_workers', type=int, default=8)

        parser.add_argument('--num_forward_estimate', type=int, default=3)
        parser.add_argument('--num_repeat_samples', type=int, default=3)
        parser.add_argument('--num_per_instance', type=int, default=1)

        parser.add_argument('--cache_root', type=str, default="/dfs/project/kgrlm/multiagent_reward/trl/cache")
        parser.add_argument('--output_dir', type=str, default="/dfs/project/kgrlm/multiagent_reward/trl/dataset")

        # stark
        parser.add_argument('--emb_model', type=str, default="text-embedding-ada-002")
        parser.add_argument('--emb_dir', type=str, default="/dfs/project/kgrlm/multiagent_reward/emb")
        return parser.parse_args()

    args = parse_args()
    dotenv_path = osp.expanduser('/dfs/project/kgrlm/common/.env')
    load_dotenv(dotenv_path)

    ##############################################
    #           Define the pipeline              #
    ##############################################
    pipeline = registered_pipeline[args.pipeline](
        max_sample_workers=args.max_workers, 
        max_eval_workers=args.max_workers
    )
    trainset, valset, _ = registered_dataset[args.dataset](**vars(args))

    trainset = trainset[:args.train_size]
    begin_time = datetime.now()
    dataset = generate_reward_model_trainset(
        args.method, pipeline, trainset,
        judge_model=args.judge_model,
        sample_temperature=args.sample_temperature,
        max_workers=args.max_workers,
        cache_dir=osp.join(args.cache_root, args.pipeline),
        num_forward_estimate=args.num_forward_estimate,
        num_repeat_samples=args.num_repeat_samples,
        num_per_instance=args.num_per_instance,
    )
    end_time = datetime.now()

    os.makedirs(args.output_dir, exist_ok=True)
    try:
        dataset.save_to_disk(osp.join(args.output_dir, f"{args.pipeline}-{args.method}"))
    except:
        dataset.save_to_disk(f"{args.pipeline}-{args.method}")

    if args.push_to_hub:
        dataset.push_to_hub(f'snap-stanford/{args.pipeline}-{args.method}', private=True)

    print(f"Time taken: {end_time - begin_time}")
