import numpy as np
import json
import os
import dspy
from tqdm import tqdm
from typing import Dict, List
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.reward.model import RewardModel
from optimas.utils.logging import setup_logger
from optimas.utils.example import Example


logger = setup_logger(__name__)


def eval_pipeline(
    pipeline: CompoundAgentPipeline,
    testset: List[Example],
    static_rollouts: List = None,
    num_repeat: int = 1
) -> List:
    """
    Evaluate a compound agent pipeline on a test set.

    Args:
        pipeline: The compound agent pipeline to evaluate
        testset: List of test examples
        static_rollouts: Optional pre-generated rollouts to use
        num_repeat: Number of times to repeat evaluation

    Returns:
        Tuple of (predictions, metrics)
    """
    assert not (static_rollouts is not None) or len(testset) == len(static_rollouts), \
        "testset and static_rollouts must have the same length"

    metrics = {}
    static_ref_dicts = []
    for i in range(num_repeat):
        if static_rollouts:
            preds, scores = [], []
            for example, static_rollout in tqdm(zip(testset, static_rollouts), total=len(testset)):
                pred = pipeline(
                    **example,
                    static_rollout=static_rollout
                )

                if i == 0:
                    static_ref_dicts.append(pipeline.static_reference(
                        **example,
                        static_rollout=static_rollout
                    ))

                score = pipeline.evaluate(example, pred, return_pred=False)
                scores.append(score)
                preds.append(pred)

            if i == 0:
                static_ref_dicts = {k: [d[k] for d in static_ref_dicts] for k in static_ref_dicts[0]}
                static_ref_dicts = {k: {"mean": np.mean(v), "std": np.std(v)} for k, v in static_ref_dicts.items()}
        else:
            results = pipeline.evaluate_multiple(testset, return_pred=True)
            original_results_num = len(results)
            results = [result for result in results if result is not None]
            filtered_results_num = len(results)
            if original_results_num != filtered_results_num:
                print(f"Original results num: {original_results_num}")
                print(f"Filtered results num: {filtered_results_num}")
                print(f"Filtered {original_results_num - filtered_results_num} NONE results")
                none_idx = [i for i, result in enumerate(results) if result is None]
                print(f"NONE results at {none_idx}")
            scores = []
            preds = []
            for result in results:
                if isinstance(result, tuple):
                    scores.append(result[0])
                    preds.append(result[1])
                else:
                    scores.append(result)
                    print(f"float result: {result}")
                    preds.append(None)
            # if isinstance(results[0], float):
            #     scores = results
            #     preds = []
            # else:
            #     scores = [result[0] for result in results]
            #     preds = [result[1] for result in results]
            static_ref_dicts = {}

        metrics.update({
            f"trial_{i}": np.mean(scores)
        })

    metrics.update({
        "mean": np.mean([metrics[f"trial_{i}"] for i in range(num_repeat)]),
        "std": np.std([metrics[f"trial_{i}"] for i in range(num_repeat)]),
        "static_ref": static_ref_dicts
    })

    return metrics, preds


class PerModuleEvaluator:
    """
    Class to evaluate reward models for each module in a pipeline independently.
    Utilizes standard deviation to select the most promising branches for evaluation.
    """

    def __init__(
        self,
        pipeline,
        testset,
        static_rollouts,
        tokenizer=None,
        max_candidates=20,
        static_rollouts_cache_path=None
    ):
        """
        Initialize the evaluator.

        Args:
            pipeline: The pipeline to evaluate
            testset: Evaluation dataset
            static_rollouts: Static rollouts dataset (preprocessed with scores)
            tokenizer: Tokenizer for the reward model
            max_candidates: Maximum number of candidates to consider per module per example
        """
        self.pipeline = pipeline
        self.testset = testset
        self.static_rollouts = static_rollouts
        self.tokenizer = tokenizer
        self.max_candidates = max_candidates
        self.static_rollouts_cache_path = static_rollouts_cache_path

        if static_rollouts_cache_path:
            os.makedirs(os.path.dirname(static_rollouts_cache_path), exist_ok=True)

    def _filter_candidates(self, candidates, module_name=None, score_type='avg_score'):
        """
        Filters candidates to a manageable number for evaluation:
        1. If more than max_candidates candidates, reduces to max_candidates
        2. Uses a deterministic selection based on preprocessed scores

        Args:
            candidates: List of candidate dictionaries
            module_name: Name of the module (for logging)
            score_type: Type of score to use ('max_score', 'avg_score', 'std_score')

        Returns:
            List of filtered candidates
        """
        if not candidates or not isinstance(candidates, list):
            return []

        if len(candidates) <= self.max_candidates:
            return candidates

        candidates = candidates.copy()

        candidates_with_idx = [(i, c) for i, c in enumerate(candidates)]

        def get_candidate_score(idx_cand_tuple):
            idx, cand = idx_cand_tuple
            if isinstance(cand, dict) and score_type in cand:
                return (cand[score_type], idx)
            elif isinstance(cand, dict) and 'score' in cand:
                return (cand['score'], idx)
            return (0, idx)

        candidates_with_idx.sort(key=get_candidate_score, reverse=True)

        return [c for _, c in candidates_with_idx[:self.max_candidates]]

    def _collect_high_std_candidates(self, static_rollouts):
        """
        Collects candidates by following branches with highest standard deviation.
        For the last module, collects all leaf nodes from the selected branch.

        Args:
            static_rollouts: Dictionary of static rollout trees

        Returns:
            Dictionary mapping each module to a nested dictionary:
            {module_name: {example_id: [(candidates, inputs), ...], ...}, ...}
        """
        module_candidates = {module_name: defaultdict(list) for module_name in self.pipeline.modules}

        for example_id, rollout in static_rollouts.items():
            example = self.testset[example_id]

            # Process example through the pipeline, following highest std paths
            self._collect_best_std_path(
                example_id,
                example,
                rollout,
                0,
                {},
                module_candidates
            )

        return module_candidates

    def _collect_best_std_path(self, example_id, example, candidates, module_idx, context, module_candidates):
        """
        Collects candidates by following the branch with highest standard deviation.
        For the last module, collects all leaf nodes in the current branch.

        Args:
            example_id: ID of the current example
            example: The example data
            candidates: Current list of candidates
            module_idx: Index of the current module in execution_order
            context: Context containing outputs from previous modules
            module_candidates: Dictionary to collect candidates for each module
        """
        if module_idx >= len(self.pipeline.execution_order):
            return

        module_name = self.pipeline.execution_order[module_idx]
        module = self.pipeline.modules[module_name]

        if not candidates or not isinstance(candidates, list):
            return

        module_inputs = {
            key: context.get(key, example.get(key))
            for key in module.input_fields if key in context or key in example
        }

        module_candidates[module_name][example_id].append((candidates, module_inputs))

        if module_idx == len(self.pipeline.execution_order) - 1:
            return

        is_second_to_last = (module_idx == len(self.pipeline.execution_order) - 2)
        next_module = self.pipeline.execution_order[module_idx + 1]

        if is_second_to_last:
            best_candidate = None
            best_std = -1
            best_fallback = -1

            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue

                if next_module not in candidate or not candidate[next_module]:
                    continue

                if 'std_score' in candidate and candidate['std_score'] > best_std:
                    best_std = candidate['std_score']
                    best_candidate = candidate
                elif best_std < 0 and 'max_score' in candidate and candidate['max_score'] > best_fallback:
                    best_fallback = candidate['max_score']
                    best_candidate = candidate
                elif best_std < 0 and best_fallback < 0 and 'avg_score' in candidate:
                    best_fallback = candidate['avg_score']
                    best_candidate = candidate

            if best_candidate and next_module in best_candidate:
                new_context = context.copy()
                new_context.update(best_candidate)

                last_module_candidates = best_candidate[next_module]

                last_module_name = self.pipeline.execution_order[-1]
                last_module = self.pipeline.modules[last_module_name]

                last_module_inputs = {
                    key: new_context.get(key, example.get(key))
                    for key in last_module.input_fields if key in new_context or key in example
                }

                # Add all leaf nodes to the collection for the last module (no more exploring)
                module_candidates[last_module_name][example_id].append((last_module_candidates, last_module_inputs))
        else:
            best_candidate = None
            best_std = -1
            best_fallback = -1

            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue

                if next_module not in candidate or not candidate[next_module]:
                    continue

                if 'std_score' in candidate and candidate['std_score'] > best_std:
                    best_std = candidate['std_score']
                    best_candidate = candidate
                elif best_std < 0 and 'max_score' in candidate and candidate['max_score'] > best_fallback:
                    best_fallback = candidate['max_score']
                    best_candidate = candidate
                elif best_std < 0 and best_fallback < 0 and 'avg_score' in candidate:
                    best_fallback = candidate['avg_score']
                    best_candidate = candidate

            if best_candidate:
                new_context = context.copy()
                new_context.update(best_candidate)

                self._collect_best_std_path(
                    example_id,
                    example,
                    best_candidate[next_module],
                    module_idx + 1,
                    new_context,
                    module_candidates
                )

    def evaluate_model(self, model, score_type='max_score'):
        """
        Evaluates a reward model on each module independently,
        focusing on paths with highest standard deviation.

        Args:
            model: The reward model to evaluate
            score_type: Which score to use for candidate filtering ('max_score' or 'avg_score')

        Returns:
            Dictionary mapping module names to evaluation scores
        """
        rm = RewardModel(model, self.tokenizer, self.pipeline)
        reward_log = {module_name: {} for module_name in self.pipeline.modules}

        if self.static_rollouts_cache_path is not None and os.path.exists(self.static_rollouts_cache_path):
            logger.info(f"Loading module candidates from {self.static_rollouts_cache_path}")
            with open(self.static_rollouts_cache_path, 'r') as f:
                module_candidates = json.load(f)
        else:
            # Collect candidates by following highest std paths
            module_candidates = self._collect_high_std_candidates(self.static_rollouts)

            # save module_candidates
            with open(self.static_rollouts_cache_path, 'w') as f:
                json.dump(module_candidates, f, indent=4)
            logger.info(f"Saved module_candidates to {self.static_rollouts_cache_path}")

        per_module_scores = {module_name: [] for module_name in self.pipeline.modules}
        hit_res = {}

        for module_name in self.pipeline.execution_order:
            # logger.info(f'Evaluating {module_name}...')
            module = self.pipeline.modules[module_name]

            no_eval = 0
            hit_list = []
            for example_id, example_candidates in module_candidates[module_name].items():
                example_highest_score = float('-inf')
                gd_highest_score = 0
                any_evaluated = False

                # Currently we only have one branch (subtree) in example_candidates, as we narrowed down to the best std path
                for branch in example_candidates:
                    # the input of candidates under same branch should be the same
                    candidates, inputs = branch[0], branch[1]

                    filtered_candidates = candidates
                    if len(filtered_candidates) <= 1:
                        continue

                    scores = []
                    for candidate in filtered_candidates:
                        full_input = {**inputs, **candidate}
                        score = rm.evaluate(module_name, **full_input, sigmoid=False)
                        scores.append(score)

                    assert len(scores) == len(filtered_candidates), "Score length mismatch"

                    # Update the highest score for this example
                    if module_name == self.pipeline.execution_order[-1]:
                        gd_scores = [c['score'] for c in filtered_candidates]
                    else:
                        gd_scores = [c[score_type] for c in filtered_candidates]
                    gd_max_score_idx = np.argmax(gd_scores)

                    any_evaluated = True
                    max_score_idx = np.argmax(scores)

                    # still do the checking in case we wanna add more branches. (Always happens when branch num = 1)
                    if scores[max_score_idx] > example_highest_score:
                        example_highest_score = scores[max_score_idx]
                        # Get ground truth score (either direct score or preprocessed score)
                        if module_name == self.pipeline.execution_order[-1]:
                            gd_highest_score = filtered_candidates[max_score_idx]['score']
                        else:
                            gd_highest_score = filtered_candidates[max_score_idx][score_type]

                        reward_log[module_name][example_id] = {
                            'pred': int(max_score_idx),
                            'gold': int(gd_max_score_idx),
                            'scores': scores,
                            'gd_scores': gd_scores
                        }
                        hit_list.append(max_score_idx == gd_max_score_idx)

                # Record the result for this example
                if any_evaluated:
                    per_module_scores[module_name].append(gd_highest_score)
                else:
                    no_eval += 1


            hit_rate = sum(hit_list) / len(hit_list) if hit_list else 0
            hit_res[module_name] = hit_rate

            logger.info(f"{module_name} skip {no_eval}/{len(module_candidates[module_name])} examples")
            logger.info(f"Hit rate for {module_name} across {len(module_candidates[module_name])} candidates: {hit_rate}")

        # Calculate average performance for each module
        result = {module: sum(scores) / len(scores) if scores else 0
                for module, scores in per_module_scores.items()}

        return result, hit_res, reward_log
