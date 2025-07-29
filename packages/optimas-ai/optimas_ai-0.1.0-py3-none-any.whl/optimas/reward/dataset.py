import os
import sys
import json
from typing import Union
from datasets import load_dataset, Dataset, DatasetDict

from optimas.utils.template import apply_reward_template
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.utils.numerical import normalization
from optimas.collect.utils import get_context_from_traj
from datasets import load_from_disk
import numpy as np


class RewardDataset:
    def __init__(
        self,
        hf_repo_or_local_dir: str,
        pipeline: CompoundAgentPipeline,
        original_trainset: DatasetDict = None,
    ):
        if os.path.exists(hf_repo_or_local_dir):
            self.dataset = load_from_disk(hf_repo_or_local_dir)
        else:
            self.dataset = load_dataset(hf_repo_or_local_dir)
        self.pipeline = pipeline
        self.module_name_lst = list(self.dataset.keys())
        self.columns = self._dataset_dict_columns()

        self.original_trainset = original_trainset
        if self.original_trainset:
            self.hash_dict_func = lambda x: hash(json.dumps(x, sort_keys=True))
            # create hash mapping for each model
            
            self.input_fields_to_gd_fields = {}
            for m in self.module_name_lst:
                inspect_eg = self.dataset[m][0]
                inspect_context_dict = get_context_from_traj(json.loads(inspect_eg['context']))
                module_context_input_keys = [k for k in inspect_context_dict.keys() if k in self.pipeline.required_input_fields]
                print(f"Module: {m} | Context keys: {module_context_input_keys}")
                for example in self.original_trainset:
                    module_context_input = {k: example[k] for k in module_context_input_keys}
                    self.input_fields_to_gd_fields[self.hash_dict_func(module_context_input)] = {k: example[k] for k in self.pipeline.ground_fields}

            # self.input_fields_to_gd_fields = {
            #     self.hash_dict_func({k: example[k] for k in self.pipeline.required_input_fields}): {k: example[k] for k in self.pipeline.ground_fields} for example in original_trainset
            # }

    def _dataset_dict_columns(self):
        key = self.module_name_lst[0]
        return list(self.dataset[key].features.keys())

    def to_inputs_only_dataset(self, module_name_lst=None):
        """
        Convert the dataset to an inputs
        """
        if module_name_lst is None:
            module_name_lst = self.module_name_lst

        data_dict = {}
        for m in module_name_lst:
            data_dict[m] = {'input': []}
            # find the keys that appear in both required_input_fields and trajectory
            inspect_eg = self.dataset[m][0]
            inspect_context_dict = get_context_from_traj(json.loads(inspect_eg['context']))
            module_context_input_keys = [k for k in inspect_context_dict.keys() if k in self.pipeline.required_input_fields]

            print(f"to_inputs_only_dataset: Module: {m} | Context keys: {module_context_input_keys}")

            for example in self.dataset[m]:
                context_dict = get_context_from_traj(json.loads(example['context']))
                context = {k: context_dict[k] for k in self.pipeline.modules[m].input_fields}

                if self.original_trainset:
                    module_context_input = {k: context_dict[k] for k in module_context_input_keys}
                    gd_fields = self.input_fields_to_gd_fields[self.hash_dict_func(module_context_input)]
                    context.update(gd_fields)

                data_dict[m]['input'].append(context)

            data_dict[m] = Dataset.from_dict(data_dict[m])

        return DatasetDict(data_dict)

    def to_implicit_preference_dataset(self, module_name_lst=None,
                                       add_margin=False, margin_threshold=0.0, normalize_margin=True):
        """
        Convert the dataset to an implicit preference dataset containing columns:
           ["chosen", "rejected"] (+ optional "margin").
        This is typically used for pairwise preference training.
        """
        assert 'response_chosen' in self.columns
        assert 'response_rejected' in self.columns
        assert 'context' in self.columns
        assert ('score_chosen' in self.columns and 'score_rejected' in self.columns) if add_margin else True

        if module_name_lst is None:
            module_name_lst = self.module_name_lst

        data_dict = {'chosen': [], 'rejected': [], 'module_name': []}
        if add_margin:
            data_dict['margin'] = []
        if self.original_trainset:
            data_dict.update({'required_input_fields': [], 'ground_fields': []})

        # one more column: example
        def _invalid_margin(example):
            if add_margin:
                return float(example['score_chosen'] - example['score_rejected']) < margin_threshold
            return False

        for module_name in module_name_lst:
            desc = self.pipeline.modules[module_name].description
            num_valid = 0

            inspect_eg = self.dataset[module_name][0]
            inspect_context_dict = get_context_from_traj(json.loads(inspect_eg['context']))
            module_context_input_keys = [k for k in inspect_context_dict.keys() if k in self.pipeline.required_input_fields]

            for example in self.dataset[module_name]:
                if margin_threshold > 0 and _invalid_margin(example):
                    continue
                num_valid += 1

                context_dict = get_context_from_traj(json.loads(example['context']))
                input_dict = {
                    k: context_dict[k]
                    for k in self.pipeline.modules[module_name].input_fields
                }

                # chosen
                chosen_text = apply_reward_template(
                    input_dict,
                    json.loads(example['response_chosen']),
                    desc=desc
                )
                data_dict['chosen'].append(chosen_text)

                if self.original_trainset:
                    # Get the ground truth fields
                    # required_inputs = {k: context_dict[k] for k in self.pipeline.required_input_fields}
                    # gd_fields = self.input_fields_to_gd_fields[self.hash_dict_func(required_inputs)]
                    # data_dict['required_input_fields'].append(required_inputs)
                    # data_dict['ground_fields'].append(gd_fields)

                    module_context_input = {k: context_dict[k] for k in module_context_input_keys}
                    gd_fields = self.input_fields_to_gd_fields[self.hash_dict_func(module_context_input)]
                    data_dict['required_input_fields'].append(module_context_input)
                    data_dict['ground_fields'].append(gd_fields)

                # rejected
                rejected_text = apply_reward_template(
                    input_dict,
                    json.loads(example['response_rejected']),
                    desc=desc
                )
                data_dict['rejected'].append(rejected_text)
                data_dict['module_name'].append(module_name)

                if add_margin:
                    data_dict['margin'].append(float(example['score_chosen']) - float(example['score_rejected']))

            print(f"[to_implicit_preference_dataset] ({module_name}) After-filtering: #{num_valid} | Ratio: {num_valid / len(self.dataset[module_name])}")
            
            print(f'Chosen Example: ', data_dict['chosen'][-1])
            print(f'Rejected Example: ', data_dict['rejected'][-1])

        if add_margin and normalize_margin:
            margin = np.array(data_dict['margin'])
            data_dict['margin'] = ((margin - np.min(margin)) / (np.max(margin) - np.min(margin))).tolist()

        return Dataset.from_dict(data_dict)

    def to_value_based_dataset(self, module_name_lst=None, normalize=True):
        """
        Convert the dataset to a value-based dataset containing columns:
           ["prompt", "value"].
        """
        if module_name_lst is None:
            module_name_lst = self.module_name_lst

        # Here we assume each record has at least 'context' and 'value' or 'score'
        # Adjust the asserts and field names if your dataset is structured differently.
        assert 'context' in self.columns, (
            "Expected a 'context' column (or rename code if your dataset uses a different name)."
        )
        # For illustration, let's check for 'score'
        # If your dataset is named exactly 'value', adjust as needed
        has_value_column = 'value' in self.columns
        has_score_column = 'score' in self.columns
        if not (has_value_column or has_score_column):
            raise ValueError(
                "No 'value' or 'score' column found. Please adjust your dataset or rename code accordingly."
            )

        data_dict = {'prompt': [], 'value': [], 'module_name': []}

        for module_name in module_name_lst:
            desc = self.pipeline.modules[module_name].description
            for example in self.dataset[module_name]:
                # 'context' typically is the raw prompt; convert if needed
                input_dict = json.loads(example['context'])
                input_dict = {
                    k: v
                    for k, v in input_dict.items()
                    if k in self.pipeline.modules[module_name].input_fields
                }
                output_dict = json.loads(example['response'])
                text = apply_reward_template(input_dict, output_dict, desc=desc)

                # Grab the numeric value
                if has_value_column:
                    val = float(example['value'])
                else:
                    val = float(example['score'])

                data_dict['prompt'].append(text)
                data_dict['value'].append(val)
                data_dict['module_name'].append(module_name)

        if normalize:
            data_dict['value'] = normalization(data_dict['value'])

        return Dataset.from_dict(data_dict)

    def to_format(self, format="implicit_preference", eval_ratio=0.1, **kwargs):
        """
        Switch between "implicit_preference" or "value_based".
        """
        if format == "implicit_preference":
            dataset = self.to_implicit_preference_dataset(**kwargs)
        elif format == "value_based":
            dataset = self.to_value_based_dataset(**kwargs)
        else:
            raise ValueError(f"Unknown dataset format: {format}")

        if eval_ratio > 0:
            module_name_lst = kwargs.get('module_name_lst', self.module_name_lst)
            dataset = dataset.train_test_split(test_size=eval_ratio, seed=42)
            full_testset = dataset['test']
            dataset['test'] = {
                module_name: full_testset.filter(lambda x: x['module_name'] == module_name)
                for module_name in module_name_lst
            }
        else:
            dataset = DatasetDict({'train': dataset})
        return dataset



if __name__ == '__main__':
    from examples.pipelines import registered_pipeline

    pipeline = registered_pipeline["hotpotqa_two_agents_pipeline"]()


    # Example: loading from a hypothetical HF repo
    reward_dataset = RewardDataset(
        "snap-stanford/hotpotqa_two_agents_pipeline-preference_modular_model_prior",
        pipeline
    )
    ds = reward_dataset.to_implicit_preference_dataset(eval_ratio=0.1)

    # Example: loading from a hypothetical HF repo
    reward_dataset = RewardDataset(
        "snap-stanford/hotpotqa_two_agents_pipeline-abs_value_llm_judge",
        pipeline
    )
    ds = reward_dataset.to_value_based_dataset(eval_ratio=0.1)
    print(ds['train'][0])
