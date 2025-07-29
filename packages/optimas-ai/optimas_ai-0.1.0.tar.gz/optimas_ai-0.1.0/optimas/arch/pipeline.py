import dspy
import random
import inspect
import concurrent.futures
from typing import Any, Dict, List, Optional, Union, Tuple, Callable
import warnings
import os
import pandas as pd
import datetime
from contextlib import contextmanager, nullcontext
from itertools import product
from optimas.utils.operation import unique_objects
from optimas.utils.example import Example
from optimas.utils.prediction import Prediction


import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

import dspy
from optimas.arch.base import BaseModule
from optimas.utils.parallel import run_parallel_tasks
from optimas.utils.logging import setup_logger
from optimas.utils.lora import load_lora_adapter

logger = setup_logger()

MODELS_LIST = [
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "openai/gpt-3.5-turbo-0125",
    "openai/gpt-4-turbo",
    "anthropic/claude-3-5-haiku-20241022",
    "anthropic/claude-3-5-sonnet-20241022",
    "anthropic/claude-3-7-sonnet-20250219",
]

class ModuleExecutor(dspy.Module):
    def __init__(self, modules: Dict[str, BaseModule], execution_order: List[str], randomize_model: bool = False):
        self.input_keys = {}
        self.output_keys = {}

        for name, module in modules.items():
            if hasattr(module, "dspy_module"):
                setattr(self, name, module.dspy_module)
            else:
                setattr(self, name, module)
            self.input_keys[name] = module.input_fields
            self.output_keys[name] = module.output_fields

        self.execution_order = execution_order
        self.all_results = {}
        self.randomize_model = randomize_model

        self.lm = dspy.settings.lm

    def forward(self, **initial_inputs: Any) -> Prediction:
        current_call_data = dict(initial_inputs)  # Local accumulator for this specific call
        last_module_name_in_loop = None

        for i, name in enumerate(self.execution_order):
            last_module_name_in_loop = name
            module_instance = getattr(self, name)  # The actual dspy.Module (e.g., dspy.Predict, dspy.Retrieve)

            current_module_output_dict = None

            try:
                if isinstance(module_instance, dspy.Retrieve):
                    # Prepare positional arguments for the retriever
                    positional_args = tuple(current_call_data[k] for k in self.input_keys[name])
                    retrieved_data = module_instance(*positional_args)  # This is a Prediction

                    # Shape the output as defined by self.output_keys
                    output_field_name = self.output_keys[name][0]  # Assuming one output field
                    current_module_output_dict = {output_field_name: "\\n".join(retrieved_data.passages)}
                else:
                    # Prepare keyword arguments for other dspy.Modules
                    kwargs_for_module = {
                        key: current_call_data[key]
                        for key in self.input_keys[name]
                        if key in current_call_data
                    }

                    if self.randomize_model:
                        self.lm = dspy.LM(model=random.choice(MODELS_LIST), max_tokens=1024, temperature=0.6, cache=False)

                    with dspy.context(lm=self.lm):
                        prediction_result = module_instance(**kwargs_for_module) # This is a Prediction

                    # Convert Prediction to a dictionary, removing 'reasoning' if present
                    if hasattr(prediction_result, "_store"):
                        current_module_output_dict = {
                            k: v for k, v in prediction_result._store.items() if k != "reasoning"
                        }
                    elif isinstance(prediction_result, dict): # If it already returned a dict
                        current_module_output_dict = {
                            k: v for k, v in prediction_result.items() if k != "reasoning"
                        }
                    else:
                        # Attempt to treat as dict-like if not a standard Prediction or dict
                        # This mirrors the original logic's fallback
                        current_module_output_dict = {
                            k: v for k, v in prediction_result.items() if k != "reasoning"
                        }

                # Update the local accumulator with the outputs of the current module
                if current_module_output_dict is not None:
                    current_call_data.update(current_module_output_dict)
                else:
                    logger.warning(f"Module {name} produced no processable output to update context.")

            except Exception as e:
                logger.error(f"Exception in module '{name}'. Current data: {current_call_data}. Error: {e}")
                # The original code printed `result` (which is current_module_output_dict here)
                # print(current_module_output_dict)
                raise e

        if last_module_name_in_loop is None:
            # This case should not happen if execution_order is not empty
            return Prediction()

        # Construct the final Prediction object.
        # It should contain the output fields of the *last* module, sourced from current_call_data.
        final_output_keys_for_prediction = self.output_keys[last_module_name_in_loop]

        prediction_content = {
            key: current_call_data[key]
            for key in final_output_keys_for_prediction
            if key in current_call_data
        }
        return Prediction(**prediction_content)


class CompoundAgentPipeline:
    """
    A pipeline that can operate in two modes:
      LLM-based mode: Accepts dynamic inputs, calls modules that internally
         query an LLM (optionally re-sampling and filtering with an RM).

    Usage: To use LLM-based mode, provide the usual arguments (e.g., default_model, etc.)
    """

    def __init__(self,
                 max_sample_workers: Optional[int] = 4, # for generating rollouts
                 max_eval_workers: Optional[int] = 4, # for evaluate_multiple
                 log_dir: Optional[str] = None):
        """
        Args:
            max_sample_workers: If provided, the number of threads for parallel RM scoring.
        """
        self.modules: Dict[str, BaseModule] = {}
        self.execution_order: List[str] = []
        self.final_output_fields: List[str] = []
        self.max_sample_workers = max_sample_workers
        self.max_eval_workers = max_eval_workers

        self.rm = None
        self.sample_size = None
        self.modules_to_apply = []

        self.log_dir = log_dir
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            self.log_file = os.path.join(log_dir, f"rollouts_{timestamp}.csv")
            self.log_df = pd.DataFrame(columns=["module_name", "module_inputs", "scores", "outputs"])
        else:
            self.log_file = self.log_df = None

    def state_dict(self) -> Dict[str, Any]:
        """
        Save the pipeline state. In LLM-mode, we might track each module's variable state.
        In static-mode, typically there's no relevant internal state to store.
        """
        state = {}
        # for name, module in self.modules.items():
        #     state[name] = module.variable
        for name, module in self.modules.items():
            if hasattr(module, 'variable') and module.variable == 'local_lm':
                # For local LLM modules, save the current adapter path if available
                if hasattr(module, 'model_id') and module.model_id:
                    state[name] = {
                        'variable': 'local_lm',
                        'adapter_id': module.model_id,
                        'adapter_path': getattr(module, '_current_adapter_path', None)
                    }
                else:
                    state[name] = {'variable': 'local_lm'}
            else:
                state[name] = module.variable
        return state

    def load_state_dict(self, state: Dict[str, Any]) -> None:
        """
        Load a pipeline state. Only relevant in LLM-mode. Static mode ignores it.
        """
        # for name, variable in state.items():
        #     if name in self.modules:
        #         self.modules[name].update(variable)
        #     else:
        #         logger.info(f"[load_state_dict] Module '{name}' not found in the pipeline.")
        for name, variable_info in state.items():
            if name in self.modules:
                if isinstance(variable_info, dict) and 'variable' in variable_info:
                    if variable_info['variable'] == 'local_lm':
                        module = self.modules[name]

                        # Set the adapter if provided
                        if 'adapter_id' in variable_info and 'adapter_path' in variable_info:
                            adapter_id = variable_info['adapter_id']
                            adapter_path = variable_info['adapter_path']

                            if adapter_path and os.path.exists(adapter_path):
                                try:
                                    # Load the adapter into vLLM
                                    host = os.getenv("VLLM_HOST", "localhost")
                                    port = int(os.getenv("VLLM_PORT", "8001"))
                                    load_lora_adapter(adapter_id, adapter_path, host, port)

                                    # Update module properties
                                    module.model_id = adapter_id
                                    module._current_adapter_path = adapter_path

                                    logger.info(f"Loaded adapter {adapter_path} as {adapter_id} for module {name}")
                                except Exception as e:
                                    logger.error(f"Failed to load adapter for module {name}: {e}")
                                    # Keep the module with base model
                                    module.model_id = None
                                    module._current_adapter_path = None
                            else:
                                # No adapter or invalid path, use base model
                                logger.warning(f"No valid adapter path provided for module {name}. Using base model.")
                                module.model_id = None
                                module._current_adapter_path = None
                        else:
                            # No adapter info, use base model
                            logger.warning(f"No adapter info provided for module {name}. Using base model.")
                            module.model_id = None
                            module._current_adapter_path = None
                    else:
                        self.modules[name].update(variable_info['variable'])
                else:
                    self.modules[name].update(variable_info)
            else:
                logger.info(f"[load_state_dict] Module '{name}' not found in the pipeline.")

    def register_module(self, name: str, module: BaseModule):
        """
        Register a single module by name.
        """
        if name in self.modules:
            raise ValueError(f"Module with name '{name}' is already registered.")
        self.modules[name] = module

    def register_modules(self, modules: Dict[str, BaseModule]):
        """
        Register multiple modules at once.
        """
        for name, module in modules.items():
            self.register_module(name, module)

    def construct_pipeline(self, module_order: List[str],
                           final_output_fields: List[str],
                           ground_fields: List[str],
                           eval_func: Any = None, *args, **kwargs):
        """
        Defines the execution order of modules and sets the desired final output keys.
        """
        self.execution_order = module_order
        self.final_output_fields = final_output_fields
        self.ground_fields = ground_fields
        self.eval_func = eval_func
        self.external = kwargs

        input_fields, output_fields = set(), set()
        for name in self.modules:
            input_fields.update(self.modules[name].input_fields)
            output_fields.update(self.modules[name].output_fields)
        self.required_input_fields = list(input_fields - output_fields)

        self.optimizable_modules = [name for name in self.modules if self.modules[name].optimizable]
        self.optimizable_module_to_idx = {module_name: idx for idx, module_name in enumerate(self.optimizable_modules)}

        assert all(name in self.modules for name in self.execution_order), \
            f"Invalid module names in execution_order: {self.execution_order}"

    # --- Reward model arguments ---
    def register_rm(
        self,
        rm: Union[Any, Dict[str, Any]],
        modules_to_apply: list = ['all'],
        sample_temperature: float = None,
        sample_size: Optional[int] = 1,
    ):
        """
        Register a reward model for filtering.
        """
        self.rm = rm
        self.sample_temperature = sample_temperature
        self.sample_size = sample_size

        self.modules_to_apply = modules_to_apply or []

        if 'all' in self.modules_to_apply:
            assert len(self.modules_to_apply) == 1, "Cannot mix 'all' with specific module names."
            self.modules_to_apply = set(self.optimizable_modules)

        assert set(self.modules_to_apply).issubset(set(self.optimizable_modules)), \
            f"Invalid module names in modules_to_apply: {self.modules_to_apply}"
        logger.info(f"[register_rm] Applying RM filtering to modules: {self.modules_to_apply}")

    @property
    def predecessor_map(self) -> Dict[str, List[str]]:
        """
        Returns a map of module names to their immediate predecessors.
        """

        predecessor_map = {}

        # Determine which modules depend on others
        for module_idx, module_name in enumerate(self.modules):
            predecessor_map[module_name] = []
            for input_field in self.modules[module_name].input_fields:
                for prev_module_idx in range(module_idx, -1, -1):
                    prev_module_name = self.execution_order[prev_module_idx]
                    if input_field in self.modules[prev_module_name].output_fields:
                        predecessor_map[module_name].append(prev_module_name)
        return predecessor_map

    @property
    def successor_map(self) -> Dict[str, List[str]]:
        """
        Returns a map of module names to their immediate successors.
        """
        successor_map = {}
        for module_name, dependencies in self.predecessor_map.items():
            for dependency in dependencies:
                if dependency not in successor_map:
                    successor_map[dependency] = []
                successor_map[dependency].append(module_name)
        return successor_map

    @property
    def desc(self) -> Dict[str, str]:
        """
        Returns the descriptions of all registered modules.
        """
        return {name: module.description for name, module in self.modules.items()}

    @contextmanager
    def context(self, module_configs=None):
        """
        Pipeline-level context manager that allows temporarily modifying multiple modules at once.

        Args:
            module_configs (Dict[str, Dict]): Dictionary mapping module names to their configuration
                Each module configuration is itself a dictionary with:
                    - 'variable': Optional new variable value
                    - Other kwargs: Will be passed to the module's context() method as config parameters

        Yields:
            The pipeline itself for method chaining

        Example:
            >>> with pipeline.context({
            >>>     'wikipedia_retriever': {'variable': {'k': 25}},
            >>>     'question_rewriter': {'model': 'openai/gpt-4o'}
            >>> }):
            >>>     scores = pipeline.evaluate_multiple(testset)
        """
        if module_configs is None:
            module_configs = {}

        # Store the context managers and entered contexts
        managed_contexts = []
        try:
            # Create and enter all contexts
            for module_name, config in module_configs.items():
                if module_name not in self.modules:
                    raise ValueError(f"Module '{module_name}' not found in pipeline")

                # Extract variable and config kwargs
                variable_config = config.pop('variable', None)
                assert not (variable_config and config.get("randomize_search_variable", None)), \
                    f"Cannot set both variable and randomize_search_variable for {module_name} at the same time."

                # Create and enter the context manager
                context_mgr = self.modules[module_name].context(variable=variable_config, **config)
                managed_contexts.append((context_mgr, module_name))
                context_mgr.__enter__()

                # Restore the config dict for proper cleanup later
                if variable_config is not None:
                    config['variable'] = variable_config

            # Yield the pipeline itself for method chaining
            yield self

        finally:
            # Exit all contexts in reverse order (LIFO)
            # Use a separate try/except for each context to ensure all are properly exited
            exceptions = []
            for ctx_mgr, module_name in reversed(managed_contexts):
                try:
                    ctx_mgr.__exit__(None, None, None)
                except Exception as e:
                    logger.error(f"Error exiting context for module '{module_name}': {e}")
                    exceptions.append(e)

            # If any exceptions occurred during cleanup, raise the first one
            if exceptions:
                raise exceptions[0]

    # ------------------------------------------------------------------------
    #                          Public Execution API
    # ------------------------------------------------------------------------
    def __call__(self, *args, **kwargs) -> Prediction:
        """
        Top-level invocation of the pipeline. Dispatches to either LLM-mode or static-mode.

        For LLM mode, typical usage: pipeline(input1=..., input2=...)
        For static mode, usage: pipeline(example_id=..., some_other_input=...)
        """
        static_mode = kwargs.get("static_rollout") is not None
        if static_mode:
            # static pipeline expects an example_id plus optional input fields
            return self._call_static(*args, **kwargs)
        else:
            # normal LLM-based pipeline
            return self._call_nonstatic(*args, **kwargs)

    def run_subpipeline(self, *args, **kwargs) -> Prediction:
        """
        Run a subset of modules from start_module to end_module.
        Dispatches to either the static or LLM subpipeline logic.
        """
        static_mode = kwargs.get("static_rollout") is not None

        if static_mode:
            return self._run_subpipeline_static(*args, **kwargs)
        else:
            return self._run_subpipeline_nonstatic(*args, **kwargs)

    def _extract_context_from_traj(self, traj: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract the final context from a trajectory dictionary.
        """
        context = {}
        for name, module_traj in traj.items():
            context.update(module_traj["input"])
            context.update(module_traj["output"])
        return context
    # ------------------------------------------------------------------------
    #                     LLM-based Pipeline Implementation
    # ------------------------------------------------------------------------
    def _call_nonstatic(self, **inputs: Any) -> Prediction:
        """
        Executes the pipeline in LLM-based mode, calling each module in sequence
        and optionally sampling multiple candidates, re-ranking them with self.rm.
        """
        pred = self._run_subpipeline_nonstatic(self.execution_order[0], self.execution_order[-1], **inputs)
        context = self._extract_context_from_traj(pred.traj)

        # Extract final outputs
        final_outputs = {
            key: context[key] for key in self.final_output_fields if key in context
        }
        missing_outputs = set(self.final_output_fields) - set(final_outputs.keys())
        if missing_outputs:
            raise ValueError(f"Missing final output keys: {missing_outputs}")

        return Prediction(**final_outputs, traj=pred.traj)

    def _run_subpipeline_nonstatic(
        self,
        start_module: Union[int, str],
        end_module: Union[int, str],
        **inputs: Any
    ) -> Prediction:
        """
        Executes a slice of the pipeline from start_module to end_module in LLM-mode.
        """
        # Convert indices
        if isinstance(start_module, int):
            start_module = self.execution_order[start_module]
        if isinstance(end_module, int):
            end_module = self.execution_order[end_module]

        context = dict(inputs)
        traj = {}

        sub_execution_order = self.execution_order[
            self.execution_order.index(start_module): self.execution_order.index(end_module) + 1
        ]

        for module_name in sub_execution_order:
            module = self.modules[module_name]
            missing_inputs = set(module.input_fields) - set(context.keys())
            if missing_inputs:
                raise ValueError(f"Module '{module_name}' is missing required inputs: {missing_inputs}")

            module_inputs = {key: context[key] for key in module.input_fields}

            is_final_module = (module_name == sub_execution_order[-1])
            do_rm_filtering = self.rm is not None and module_name in self.modules_to_apply

            if do_rm_filtering:
                outputs = self._sample_rollouts_and_rank(module_name, module, module_inputs)
            else:
                outputs = self._single_call(module, module_inputs)

            context.update(outputs)
            traj[module_name] = module.traj

        return Prediction(**outputs, traj=traj)

    def _single_call(self, module: BaseModule, module_inputs: Dict[str, Any]):
        """
        Make a single LLM call to the module and return the outputs.
        """
        outputs = module(**module_inputs)
        return outputs

    def _sample_rollouts_and_rank(self, module_name: str, module: BaseModule, module_inputs: Dict[str, Any]):
        """
        Sample multiple times at higher temperature, evaluate each result with RM,
        pick the best. Return the best outputs.
        """

        def parallel_sample(sample_size):
            output_pool = []
            with ThreadPoolExecutor(max_workers=self.max_sample_workers) as executor:
                futures = [
                    executor.submit(self._single_call, module, module_inputs)
                    for _ in range(sample_size)
                ]
                for f in as_completed(futures):
                    result = f.result()
                    if result is not None:
                        output_pool.append(result)
            return output_pool

        if hasattr(module.config, 'temperature'):
            context = nullcontext() if self.sample_temperature is None else module.context(temperature=self.sample_temperature)
            with context:
                output_pool = parallel_sample(self.sample_size)
        elif hasattr(module, "variable_search_space") and module.variable_search_space:
            all_combinations = [
                dict(zip(module.variable_search_space.keys(), values))
                for values in product(*module.variable_search_space.values())
            ]
            output_pool = []
            for variable in all_combinations:
                with module.context(variable=variable):
                    output_pool.append(parallel_sample(1)[0])
        else:
            output_pool = parallel_sample(1)

        # Evaluate with RM, pick best
        output_pool = unique_objects(output_pool)

        if len(output_pool) > 1:
            batch_pool = [{**module_inputs, **out} for out in output_pool]
            scores = self.rm.batch_evaluate(module_name, batch_pool)
        else:
            scores = [1]

        # sort scores and output_pool
        scores_sorted = sorted(scores, reverse=True)
        outputs_sorted = [output_pool[i] for i in np.argsort(scores)[::-1]]

        logger.info(f"[_sample_rollouts_and_rank] {module_name} Output pool: {outputs_sorted}")
        logger.info(f"[_sample_rollouts_and_rank] {module_name} Scores: {scores_sorted}")
        logger.info(f"[_sample_rollouts_and_rank] {module_name} Best candidate: {outputs_sorted[0]}")
        logger.info(f"[_sample_rollouts_and_rank] {module_name} Best score: {scores_sorted[0]}")

        module.traj = {
            "input": module_inputs,
            "output": outputs_sorted[0],
            "score": scores_sorted[0],
        }

        if self.log_df is not None:
            if hasattr(pd.DataFrame, 'append'):
                self.log_df = self.log_df.append({
                    "module_name": module_name,
                    "module_inputs": module_inputs,
                    "outputs": outputs_sorted,
                    "scores": scores_sorted,
                }, ignore_index=True)
            else:
                self.log_df = pd.concat([self.log_df, pd.DataFrame({
                    "module_name": module_name,
                    "module_inputs": module_inputs,
                    "outputs": outputs_sorted,
                    "scores": scores_sorted,
                }, index=[0])], ignore_index=True)
            self.log_df.to_csv(self.log_file, index=False)

        return outputs_sorted[0]

    # ------------------------------------------------------------------------
    #                    Static-data Pipeline Implementation
    # ------------------------------------------------------------------------
    def _call_static(self, static_rollout: dict, **inputs: Any) -> Prediction:
        """
        Executes the pipeline in static mode for a given static_rollout (plus any extra inputs).
        Follows the nested data structure, optionally using RM or random choice.
        """

        context = dict(inputs)
        traj = {}
        for idx, module_name in enumerate(self.execution_order):
            module = self.modules[module_name]
            missing_inputs = set(module.input_fields) - set(context.keys())
            if missing_inputs:
                raise ValueError(
                    f"Module '{module_name}' is missing required inputs: {missing_inputs}"
                )

            # Possibly limit the number of candidates
            if self.sample_size is not None and len(static_rollout) > self.sample_size:
                static_rollout = static_rollout[:self.sample_size]

            # Decide if we do multi-candidate filtering with RM
            is_final_module = (idx == len(self.execution_order) - 1)
            do_rm_filtering = self.rm is not None and module_name in self.modules_to_apply

            if do_rm_filtering:
                best_cand, best_score = self._pick_best_candidate(module_name, static_rollout, context)
                module.traj = {
                    "input": {k: context[k] for k in module.input_fields},
                    "output": best_cand,
                    "score": best_score
                }
            else:
                best_cand = random.choice(static_rollout)
                module.traj = {
                    "input": {k: context[k] for k in module.input_fields},
                    "output": best_cand
                }

            # Update context
            context.update(best_cand)
            traj[module_name] = module.traj

            # Move to sub-list for the next module
            if not is_final_module:
                next_module_name = self.execution_order[idx + 1]
                if next_module_name not in best_cand:
                    raise ValueError(
                        f"Chosen candidate has no sub-list '{next_module_name}' "
                        f"for module '{module_name}'. Can't proceed."
                    )
                static_rollout = best_cand[next_module_name]

        # Gather final outputs
        final_outputs = {
            key: context[key] for key in self.final_output_fields if key in context
        }
        return Prediction(**final_outputs, traj=traj)

    def _run_subpipeline_static(
        self,
        static_rollout: dict,
        start_module: Union[int, str],
        end_module: Union[int, str],
        **inputs: Any
    ) -> Prediction:
        """
        Run only the slice of modules [start_module : end_module] in static mode.
        """
        if isinstance(start_module, int):
            start_idx = start_module
        else:
            start_idx = self.execution_order.index(start_module)

        if isinstance(end_module, int):
            end_idx = end_module
        else:
            end_idx = self.execution_order.index(end_module)

        if end_idx < start_idx:
            raise ValueError("end_module must come after start_module in execution_order")

        context = dict(inputs)
        traj = {}

        # 1) Skip modules [0 : start_idx]
        for i in range(0, start_idx):
            if not static_rollout:
                raise ValueError(f"No candidates exist for skip at module index {i}")
            chosen = static_rollout[0]
            if i < len(self.execution_order) - 1:
                nxt_mod = self.execution_order[i + 1]
                if nxt_mod in chosen:
                    static_rollout = chosen[nxt_mod]
                else:
                    raise ValueError(
                        f"In skip pass, cannot find next module sub-list '{nxt_mod}' at module index {i}."
                    )

        # 2) Now run modules in [start_idx : end_idx]
        for idx in range(start_idx, end_idx + 1):
            module_name = self.execution_order[idx]
            module = self.modules[module_name]

            missing_inputs = set(module.input_fields) - set(context.keys())
            if missing_inputs:
                raise ValueError(
                    f"Module '{module_name}' is missing required inputs: {missing_inputs}"
                )

            # Possibly limit
            if self.sample_size is not None and len(static_rollout) > self.sample_size:
                static_rollout = static_rollout[:self.sample_size]

            is_final_module = (idx == end_idx)
            do_rm_filtering = self.rm is not None and module in self.modules_to_apply

            if do_rm_filtering:
                best_cand, best_score = self._pick_best_candidate(module_name, static_rollout, context)
                module.traj = {
                    "input": {k: context[k] for k in module.input_fields},
                    "output": best_cand,
                    "score": best_score
                }
            else:
                best_cand = random.choice(static_rollout)
                module.traj = {
                    "input": {k: context[k] for k in module.input_fields},
                    "output": best_cand
                }

            context.update(best_cand)
            traj[module_name] = module.traj

            if not is_final_module and idx < len(self.execution_order) - 1:
                nxt_mod_name = self.execution_order[idx + 1]
                if nxt_mod_name not in best_cand:
                    raise ValueError(
                        f"Chosen candidate has no sub-list '{nxt_mod_name}' after module '{module_name}'."
                    )
                static_rollout = best_cand[nxt_mod_name]

        final_outputs = {
            k: context[k] for k in self.final_output_fields if k in context
        }
        return Prediction(**final_outputs, traj=traj)

    def _pick_best_candidate(
        self,
        module_name: str,
        candidates: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], float]:
        """
        Evaluates all candidates in parallel (if max_sample_workers > 1) or sequentially,
        and returns the best candidate along with its score.

        Args:
            module (BaseModule): The module to evaluate.
            candidates (List[Dict[str, Any]]): The list of candidate outputs.
            context (Dict[str, Any]): The shared context for evaluation.

        Returns:
            Tuple[Dict[str, Any], float]: The best candidate and its score.
        """
        def score_fn(candidate: Dict[str, Any]) -> float:
            if isinstance(self.rm, dict):
                return self.rm[module_name].evaluate(module_name, **{**context, **candidate})
            return self.rm.evaluate(module_name, **{**context, **candidate})

        if len(candidates) == 1:
            return candidates[0], -1

        scores = [score_fn(c) for c in candidates]
        best_idx = np.argmax(scores)

        return candidates[best_idx], scores[best_idx]

    # ------------------------------------------------------------------------
    #                    Evaluation (Single / Batch)
    # ------------------------------------------------------------------------
    def evaluate(self, example: Example, prediction: Optional[Prediction] = None, return_pred: bool = False,
                **kwargs) -> float:
        """
        Generates a prediction (if not provided) and evaluates it against the ground truth.

        Args:
            example (Example): The reference example containing ground truth.
            prediction (Optional[Prediction]): If provided, evaluates this prediction directly;
                                                   otherwise, generates one.

        Returns:
            float: The evaluation score.
        """
        if prediction is None:
            prediction = self(**{k: getattr(example, k) for k in self.required_input_fields})

        try:
            score = self.eval_func(
                **{k: getattr(prediction, k) for k in self.final_output_fields},
                **{k: getattr(example, k) for k in self.ground_fields},
                **self.external,
                **kwargs
            )
            if return_pred:
                return (score, prediction)
            return score

        except Exception as e:
            import traceback

            logger.error(f"Evaluation failed for example {example}: {e}\n{traceback.format_exc()}")
            return float("-inf")

    def evaluate_multiple(self,
                          examples: List[Example],
                          predictions: Optional[List[Prediction]] = None,
                          return_pred: bool = False
        ) -> List[float]:
        """
        Evaluates a batch of examples, either by generating predictions first or using precomputed ones.

        Args:
            examples (List[Example]): The reference examples.
            predictions (Optional[List[Prediction]]): If provided, directly evaluates them.
                                                           Otherwise, generates predictions first.

        Returns:
            List[float]: A list of evaluation scores.
        """
        task_args = (
            [(ex, pred, return_pred) for ex, pred in zip(examples, predictions)]
            if predictions is not None
            else [(ex, None, return_pred) for ex in examples]
        )
        if (self.max_eval_workers > 1 and
            self.rm is not None and
            predictions is None and
            (self.sample_size > 1 or any(module.variable_search_space for module in self.modules.values()))
            ):
            logger.info(f"[evaluate_multiple] Set max_eval_workers to 1 for RM-based evaluation. \n\n***This may lead to performance issues.***\n\n")
            max_eval_workers = 1
        else:
            max_eval_workers = self.max_eval_workers

        return run_parallel_tasks(self.evaluate,
                                  task_args,
                                  use_tqdm=True,
                                  max_workers=max_eval_workers,
                                  task_desc="Evaluating Batch"
                                  )

    def static_reference(self, static_rollout: dict, **inputs: Any) -> float:
        """
        Get the reference score for a given example_id by computing the maximum, minimum,
        and average score based on the static data tree structure and whether do_rm_filtering is applied.
        """
        def traverse_tree(candidates, module_names):
            """ Recursively traverse the candidate tree and compute scores accordingly. """
            if not candidates:
                warnings.warn(f"Encountered an empty candidate list which may indicate missing or malformed data.")
                return 0, 0, 0

            module_name = module_names[0]
            module = self.modules[module_name]
            do_rm_filtering = self.rm is not None and module in self.modules_to_apply

            if isinstance(candidates, list) and all(isinstance(c, dict) and "score" in c for c in candidates):
                scores = [c["score"] for c in candidates]
                return max(scores), min(scores), sum(scores) / len(scores) if scores else (0, 0, 0)

            child_scores = []
            for cand in candidates:
                for key in cand:
                    if isinstance(cand[key], list):
                        leaf_scores = [leaf["score"] for leaf in cand[key] if isinstance(leaf, dict) and "score" in leaf]
                        if leaf_scores:
                            child_scores.append(sum(leaf_scores) / len(leaf_scores))
                        else:
                            child_max, child_min, child_avg = traverse_tree(cand[key], module_names[1:])
                            child_scores.append(child_avg)

            if do_rm_filtering:
                if not child_scores:
                    warnings.warn(f"No valid child scores found at module '{module_name}'.")
                    return 0, 0, 0
                return max(child_scores), min(child_scores), sum(child_scores) / len(child_scores)
            else:
                if not child_scores:
                    warnings.warn(f"No valid child scores found at module '{module_name}', expected hierarchical structure might be missing.")
                    return 0, 0, 0
                return max(child_scores), min(child_scores), sum(child_scores) / len(child_scores)

        max_score, min_score, avg_score = traverse_tree(static_rollout, self.execution_order)
        return {"max": max_score, "min": min_score, "avg": avg_score}

    def get_dspy_module(self, randomize_model: bool = False) -> dspy.Module:
        if randomize_model:
            print("Randomizing model for pipeline execution.")
        return ModuleExecutor(self.modules, self.execution_order, randomize_model)

    def syncronize_modules(self, dspy_module: dspy.Module):
        for name in self.execution_order:
            self.modules[name].dspy_module = getattr(dspy_module, name)
