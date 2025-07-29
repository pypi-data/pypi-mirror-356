import torch
import torch.nn as nn
from typing import Dict, List
import json

import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path
from tqdm import tqdm
import os
import hashlib

from transformers import AutoTokenizer, AutoModel
import dspy
from optimas.utils.template import apply_reward_template
from optimas.arch.base import BaseModule
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.collect.utils import get_context_from_traj
try:
    from optimas.utils.llm_lib.get_llm_embeddings import get_llm_embeddings
except ImportError:
    pass


class RewardModel(nn.Module):
    """
    A reward model for evaluating compound agent systems.

    This model formats prompts, tokenizes inputs, and assesses agent performance
    based on provided outputs and contextual information.
    """
    def __init__(
        self,
        model: AutoModel,
        tokenizer: AutoTokenizer,
        pipeline: CompoundAgentPipeline,
        batch_size: int = 2  # Add this parameter
    ):
        """
        Initializes the reward model.

        Args:
            model: The underlying model for computing rewards.
            tokenizer: Tokenizer for processing inputs.
            pipeline: The compound agent pipeline.
            batch_size: Size of batches for batch evaluation (default: 32).
        """
        super().__init__()
        # Initialize tokenizer
        self.model = model
        self.tokenizer = tokenizer
        self.device = model.device
        self.batch_size = batch_size

        self.pipeline = pipeline
        self.module_to_idx = pipeline.optimizable_module_to_idx
        print(f"Module-to-index mapping created: {self.module_to_idx}")

    def _process_prompt(self, module: BaseModule, **kwargs) -> torch.Tensor:
        """
        Tokenize the complete prompt (inputs + outputs).

        Args:
            module (BaseModule): The module containing input_fields, output_fields, etc.
            inputs: Keyword arguments containing input/output values.

        Returns:
            torch.Tensor: The tokenized prompt as a tensor.
        """
        # Separate the inputs and outputs according to the module
        input_dict = {k: v for k, v in kwargs.items() if k in module.input_fields}
        output_dict = {k: v for k, v in kwargs.items() if k in module.output_fields}

        # Fill in the default prompt template
        text = apply_reward_template(
            input_dict=input_dict,
            output_dict=output_dict,
            desc=module.description
        )
        print(text)
        return text

    def evaluate(self, module_name: str, sigmoid=False, **kwargs) -> torch.Tensor:
        """
        Execute the forward pass and post-processing to compute the reward.

        Args:
            module (BaseModule): The module to evaluate.
            inputs: Keyword arguments containing input/output values.

        Returns:
            torch.Tensor: Model outputs after post-processing.
        """
        operator = torch.sigmoid if sigmoid else lambda x: x
        module = self.pipeline.modules[module_name]

        prompt = self._process_prompt(module, **kwargs)
        model_inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model(**model_inputs)

        if output.logits.ndim > 1 and output.logits.shape[1] > 1:
            assert output.logits.numel() == len(self.module_to_idx), "Model output should match the number of modules."
            return operator(output.logits[0, self.module_to_idx[module_name]]).item()

        assert output.logits.numel() == 1, "Model output should be a single value."
        return operator(output.logits).item()

    def batch_evaluate(self, module_name: str, batch_pool: list, sigmoid=False) -> list:
        """
        Evaluate multiple instances in batches.

        Args:
            module_name (str): The name of the module to evaluate.
            batch_pool (list): List of dictionaries containing kwargs for each instance.
            sigmoid (bool): Whether to apply sigmoid activation to the output.

        Returns:
            list: List of scores for each instance in the batch_pool.
        """
        operator = torch.sigmoid if sigmoid else lambda x: x
        module = self.pipeline.modules[module_name]

        scores = []

        # Process in batches
        for batch_start in range(0, len(batch_pool), self.batch_size):
            batch_end = min(batch_start + self.batch_size, len(batch_pool))
            batch = batch_pool[batch_start:batch_end]

            # Process prompts for this batch
            prompts = []
            for kwargs in batch:
                prompt = self._process_prompt(module, **kwargs)
                prompts.append(prompt)

            # Tokenize all prompts in the batch together
            model_inputs = self.tokenizer(
                prompts,
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.device)

            with torch.no_grad():
                output = self.model(**model_inputs)

            # Process outputs based on the model's output shape
            if output.logits.ndim > 1 and output.logits.shape[1] > 1:
                # Multi-module output case
                assert output.logits.shape[1] == len(self.module_to_idx), \
                    "Model output should match the number of modules."

                # Extract scores for the specific module for each instance in batch
                module_idx = self.module_to_idx[module_name]
                batch_scores = operator(output.logits[:, module_idx]).tolist()

            else:
                # Single output case
                assert output.logits.shape[1] == 1, "Model output should be a single value."
                batch_scores = operator(output.logits.squeeze(-1)).tolist()

            scores.extend(batch_scores)

        return scores


class EmbeddingSimilarityRewardModel(nn.Module):
    """
    Reward = weighted cosine-similarity in a frozen embedding space between
    (candidate output) and (preferred output) *for the same input*.

    The similarity is weighted by the score_chosen value from the dataset.

    Preferred-output embeddings are pre-computed once per module and
    cached to disk, so repeated runs don't rebuild them.
    """

    def __init__(
        self,
        dataset_name: str,
        pipeline: CompoundAgentPipeline,
        reward_dataset: "RewardDataset",
        embedding_model: str = "text-embedding-3-small",
        batch_size: int = 32,
        cache_dir: str = "/dfs/project/kgrlm/multiagent_reward/trl/reward_emb/embedding_cache",
    ):
        super().__init__()
        self.pipeline = pipeline
        self.embed_model = embedding_model
        self.batch_size = batch_size
        self.hash_fn = lambda x: hashlib.sha256(
            json.dumps(x, sort_keys=True).encode("utf-8")
        ).hexdigest()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        cache_dir = Path(cache_dir)
        cache_dir = cache_dir / dataset_name
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Store both embeddings and weights
        self.gt_embs: Dict[str, Dict[int, torch.Tensor]] = {
            m: {} for m in pipeline.modules
        }
        self.gt_weights: Dict[str, Dict[int, float]] = {m: {} for m in pipeline.modules}

        batch_sz = 128

        for m in reward_dataset.module_name_lst:
            emb_cache_file = (
                cache_dir / f"{m}_{embedding_model.replace('/', '_')}_embs.pt"
            )
            weight_cache_file = (
                cache_dir / f"{m}_{embedding_model.replace('/', '_')}_weights.pt"
            )

            if emb_cache_file.exists() and weight_cache_file.exists():
                self.gt_embs[m] = {
                    k: v.to(self.device)
                    for k, v in torch.load(
                        emb_cache_file, map_location=self.device
                    ).items()
                }
                self.gt_weights[m] = torch.load(
                    weight_cache_file, map_location=self.device
                )
                continue

            desc = pipeline.modules[m].description
            tmp_embs: Dict[int, torch.Tensor] = {}
            tmp_weights: Dict[int, float] = {}
            all_hashes: List[int] = []
            all_texts: List[str] = []
            all_scores: List[float] = []

            # 1) gather hashes + texts + scores
            print(
                f"[{m}] collecting GT texts, total {len(reward_dataset.dataset[m])} examples"
            )
            for eg in tqdm(
                reward_dataset.dataset[m],
                desc=f"[{m}] collecting GT texts",
                leave=False,
                total=len(reward_dataset.dataset[m]),
            ):
                # Get score (default to 1.0 if not present)
                score = float(eg["score_chosen"])

                ctx = get_context_from_traj(json.loads(eg["context"]))
                try:
                    inp = {k: ctx[k] for k in pipeline.modules[m].input_fields}
                except KeyError:
                    context = json.loads(eg["context"])
                    print(f"{context=}")
                    print(
                        f"KeyError: {ctx.keys()} vs {pipeline.modules[m].input_fields}"
                    )
                    print(f"{ctx=}")
                    inp = {k: ctx[k] for k in pipeline.modules[m].input_fields}

                h = self.hash_fn(inp)
                # If we already have this input hash but with a higher score, skip
                if h in tmp_weights and tmp_weights[h] > score:
                    continue

                chosen = json.loads(eg["response_chosen"])
                all_hashes.append(h)
                all_texts.append(apply_reward_template(inp, chosen, desc=desc))
                all_scores.append(score)

            # 2) embed in mini-batches
            batch_iter = range(0, len(all_texts), batch_sz)
            for start in tqdm(
                batch_iter,
                desc=f"[{m}] embedding GT texts",
                leave=False,
                total=len(batch_iter),
            ):
                end = min(start + batch_sz, len(all_texts))
                chunk_texts = all_texts[start:end]
                chunk_hashes = all_hashes[start:end]
                chunk_scores = all_scores[start:end]

                with torch.no_grad():
                    chunk_emb = get_llm_embeddings(chunk_texts, model=self.embed_model)

                for h, e, s in zip(chunk_hashes, chunk_emb, chunk_scores):
                    tmp_embs[h] = e.to(self.device)
                    tmp_weights[h] = s

            torch.save(tmp_embs, emb_cache_file)
            torch.save(tmp_weights, weight_cache_file)
            self.gt_embs[m] = tmp_embs
            self.gt_weights[m] = tmp_weights
            print(
                f"[{m}] saved {len(tmp_embs)} GT embeddings and weights to {emb_cache_file} and {weight_cache_file}"
            )

        self.eval()

    def evaluate(self, module_name: str, sigmoid: bool = False, **kwargs) -> float:
        """
        Evaluate a single instance.

        Args:
            module_name (str): The name of the module to evaluate.
            sigmoid (bool): Whether to apply sigmoid activation to the output.
            **kwargs: Dictionary containing input/output values.

        Returns:
            float: Weighted similarity score.
        """
        mod = self.pipeline.modules[module_name]

        inp = {k: v for k, v in kwargs.items() if k in mod.input_fields}
        out = {k: v for k, v in kwargs.items() if k in mod.output_fields}

        key = self.hash_fn(inp)
        if key not in self.gt_embs[module_name]:
            print('warning: unseen input, skipping')
            return 0.0  # unseen input → neutral reward

        text_pred = apply_reward_template(inp, out, desc=mod.description)
        try:
            emb_pred = get_llm_embeddings(text_pred, model=self.embed_model)[0].to(
                self.device
            )
            emb_gt = self.gt_embs[module_name][key]
            weight = self.gt_weights[module_name][key]

            # Calculate cosine similarity
            similarity = F.cosine_similarity(emb_pred, emb_gt, dim=0)

            # Weight the similarity by the score_chosen
            weighted_score = similarity * weight

        except Exception as e:
            print(f"Error in embedding similarity: {e}")
            return 0.0

        return (
            torch.sigmoid(weighted_score).item() if sigmoid else weighted_score.item()
        )

    def batch_evaluate(self, module_name: str, batch_pool: list, sigmoid=False) -> list:
        """
        Evaluate multiple instances in batches.

        Args:
            module_name (str): The name of the module to evaluate.
            batch_pool (list): List of dictionaries containing kwargs for each instance.
            sigmoid (bool): Whether to apply sigmoid activation to the output.

        Returns:
            list: List of weighted similarity scores for each instance in the batch_pool.
        """
        operator = torch.sigmoid if sigmoid else lambda x: x
        mod = self.pipeline.modules[module_name]

        scores = []

        # Process in batches
        for batch_start in range(0, len(batch_pool), self.batch_size):
            batch_end = min(batch_start + self.batch_size, len(batch_pool))
            batch = batch_pool[batch_start:batch_end]

            batch_texts = []
            batch_keys = []
            batch_has_gt = []
            batch_weights = []

            # Prepare data for this batch
            for kwargs in batch:
                inp = {k: v for k, v in kwargs.items() if k in mod.input_fields}
                out = {k: v for k, v in kwargs.items() if k in mod.output_fields}

                key = self.hash_fn(inp)
                has_gt = key in self.gt_embs[module_name]

                text_pred = apply_reward_template(inp, out, desc=mod.description)

                batch_texts.append(text_pred)
                batch_keys.append(key)
                batch_has_gt.append(has_gt)

                if has_gt:
                    batch_weights.append(self.gt_weights[module_name][key])
                else:
                    batch_weights.append(0.0)

            # Get embeddings for all texts in the batch
            try:
                with torch.no_grad():
                    batch_embs = get_llm_embeddings(batch_texts, model=self.embed_model)
                    batch_embs = [emb.to(self.device) for emb in batch_embs]
            except Exception as e:
                print(f"Error in batch embedding: {e}")
                # Fall back to zero scores for the entire batch
                scores.extend([0.0] * len(batch))
                continue

            # Calculate weighted similarity scores
            batch_scores = []
            for emb_pred, key, has_gt, weight in zip(
                batch_embs, batch_keys, batch_has_gt, batch_weights
            ):
                if not has_gt:
                    batch_scores.append(0.0)  # unseen input → neutral reward
                    continue

                emb_gt = self.gt_embs[module_name][key]
                try:
                    # Calculate cosine similarity
                    similarity = F.cosine_similarity(emb_pred, emb_gt, dim=0)

                    # Weight the similarity by the score_chosen
                    weighted_score = similarity * weight

                    batch_scores.append(operator(weighted_score).item())
                except Exception as e:
                    print(f"Error in embedding similarity: {e}")
                    batch_scores.append(0.0)

            scores.extend(batch_scores)

        return scores


if __name__ == '__main__':

    from transformers import BitsAndBytesConfig
    from optimas.utils.load import load_model_and_tokenizer
    from transformers import AutoModelForSequenceClassification

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=False,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    from peft import LoraConfig
    peft_config = LoraConfig(
        r=32,
        lora_alpha=16,
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
        init_lora_weights="gaussian",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"]
    )
    model, tokenizer = load_model_and_tokenizer("meta-llama/Llama-3.1-8B-Instruct",
                                                # max_new_tokens=2048,
                                                peft_config=peft_config,
                                                bnb_config=bnb_config,
                                                model_class=AutoModelForSequenceClassification,
                                                num_labels=4)
    print(model)

    rm = RewardModel(model, tokenizer)
    module = BaseModule("Test module", ["input1", "input2"], ["output1", "output2"])
    reward = rm.evaluate(module, input1="value1", input2="value2", output1="value1", output2="value2")
    print(reward)
