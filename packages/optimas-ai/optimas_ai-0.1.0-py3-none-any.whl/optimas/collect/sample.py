import dspy
import copy
from typing import Any, Dict, List, Optional, Tuple
from optimas.arch.pipeline import CompoundAgentPipeline
from concurrent.futures import ThreadPoolExecutor

from optimas.collect.process import process_dataset_parallel
from optimas.utils.example import Example
from optimas.utils.prediction import Prediction
from optimas.utils.operation import unique_objects
from optimas.collect.utils import get_context_from_traj
from tqdm import tqdm


def generate_samples(
    pipeline: CompoundAgentPipeline,
    example: Example,
    modules_to_perturb: List[str],
    traj: Dict,
    num_samples: int = 3,
    max_workers: int = 8
) -> List[Any]:
    """
    Generates candidate states by perturbing outputs from specified modules.

    Args:
        pipeline (CompoundAgentPipeline): The pipeline used to run sub-pipelines.
        modules_to_perturb (List[str]): Names of modules to perturb.
        traj (Dict): The trajectory dictionary used to reference the original states.
        num_samples (int, optional): Number of samples to generate.
        max_workers (int, optional): Number of workers for parallel sampling.

    Returns:
        List[Any]: A list of unique samples (each sample's structure depends on your pipeline).
                   If no unique samples can be generated, an empty list might be returned.
    """
    module_names = list(pipeline.modules.keys())
    modules_to_perturb_idx = [module_names.index(m) for m in modules_to_perturb]
    earliest_midx, latest_midx = min(modules_to_perturb_idx), max(modules_to_perturb_idx)
    latest_module_name = module_names[latest_midx]
    
    # Build the original trajectory subset
    original_traj = {m: traj[m] for m in module_names[:latest_midx + 1]}

    # Flatten the context from all modules before earliest_midx
    context = {
        **{k: getattr(example, k) for k in pipeline.required_input_fields},
        **{
            k: v 
            for m in module_names[:earliest_midx] 
            for k, v in traj[m]['input'].items()
        },
        **{
            k: v 
            for m in module_names[:earliest_midx] 
            for k, v in traj[m]['output'].items()
        },
    }
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        perturbed_samples = list(
            executor.map(
                lambda _: pipeline.run_subpipeline(
                    start_module=earliest_midx,
                    end_module=latest_midx,
                    **context
                ),
                range(num_samples)
            )
        )
    # Append the original traj for uniqueness checking
    perturbed_trajs = [{**original_traj, **s.traj} for s in perturbed_samples]
    perturbed_trajs.append(original_traj)

    # Identify unique outputs from the latest module's 'output'
    _, unique_indices = unique_objects(
        [t[latest_module_name]['output'] for t in perturbed_trajs],
        return_idx=True
    )
    unique_samples = [perturbed_trajs[i] for i in unique_indices]

    return unique_samples


def evaluate_samples(
    pipeline,
    examples: List[Example],
    trajs: List[Dict],
    forward_to_module: str = None,
    process_reward_func: callable = None,
    max_workers: int = 8,
    num_forward_estimate: int = 3,
) -> List[Tuple[Any, Dict]]:
    """
    Evaluate multiple (example, traj) pairs in parallel using ThreadPoolExecutor.
    Args:
        pipeline: The pipeline or CompoundAgentPipeline used for sub-pipeline runs/evaluation.
        examples: A list of Example objects, each representing inputs to evaluate.
        trajs: A corresponding list of partial trajectories (dict), one per example.
        forward_to_module: (Optional) Module name at which to stop if not running to the end.
        process_reward_func: (Optional) Custom function for computing final score if we stop before the last module.
        max_workers: Number of parallel threads to use (default=8).

    Returns:
        A list of (score_list, final_output_list) tuples for each (example, pred) pair.
    """

    # Ensure that examples and trajs align
    if len(examples) != len(trajs):
        raise ValueError("Number of examples must match number of trajs.")

    module_names = list(pipeline.modules.keys())

    if forward_to_module is None:
        forward_to_module = module_names[-1]

    def single_eval(example_and_traj: Tuple[Example, Dict]) -> Tuple[Any, dict]:
        example, traj = example_and_traj

        # Copy the trajectory to avoid mutating the original
        local_traj = copy.copy(traj)

        # Identify completed modules
        existing_module_names = list(local_traj.keys())
        if not existing_module_names:
            raise ValueError("Trajectory is empty—no modules in `traj`.")

        # Convert each existing module name to its index and pick the max
        existing_module_indices = [module_names.index(m) for m in existing_module_names]
        last_completed_idx = max(existing_module_indices)

        # Build the context from current trajectory
        context = get_context_from_traj(local_traj)

        # Always add fields required by the pipeline
        context.update({k: getattr(example, k) for k in pipeline.required_input_fields})
        
        scores, preds = [], []
        for _ in range(num_forward_estimate):
            if last_completed_idx + 1 < len(module_names):
                # Run sub-pipeline from the module AFTER the last completed to the scorer module
                pred = pipeline.run_subpipeline(
                    start_module=last_completed_idx + 1,
                    end_module=forward_to_module,
                    **context
                )
            else:
                pred = Prediction(**context, traj=local_traj)

            # If we ended on the last module, evaluate directly
            if forward_to_module == module_names[-1]:
                score = pipeline.evaluate(example, pred)
            else:
                # Use the custom reward function for scoring
                if process_reward_func is None:
                    raise ValueError(
                        "Must provide process_reward_func if not running to the final module."
                    )
                score = process_reward_func(pipeline, example, pred)
            scores.append(score)
            preds.append(pred)

        avg_score = sum(scores) / len(scores)
        additional_info = [{"traj": p.traj, "score": s} for p, s in zip(preds, scores)]
        return avg_score, additional_info

    # Parallelize the evaluation over all (example, traj) pairs
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = executor.map(single_eval, zip(examples, trajs))
        results = list(
            tqdm(futures, total=len(examples), desc="Evaluating Samples")
        )
    return results