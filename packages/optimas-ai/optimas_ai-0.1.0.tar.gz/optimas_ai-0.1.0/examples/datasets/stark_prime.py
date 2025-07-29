import os
import os.path as osp
import shutil
import json
import random
import subprocess
import copy
from typing import Dict, List, Optional, Any, Union
from functools import partial
from concurrent.futures import ThreadPoolExecutor, as_completed

import torch
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import pandas as pd
from tqdm import tqdm
import dspy
from huggingface_hub import hf_hub_download, list_repo_files
from optimas.utils.example import Example


try:
    from stark_qa import load_qa
    import stark_qa
    from stark_qa.models import VSS
    from examples.pipelines.stark.tools import *
except ImportError:
    pass


STARK_QA_DATASET = {
    "repo": "snap-stanford/stark",
    "folder": "qa"
}

class STaRKDataset:
    def __init__(self, 
                 name: str, 
                 root: Union[str, None] = None, 
                 human_generated_eval: bool = False):
        """
        Initialize the STaRK dataset.

        Args:
            name (str): Name of the dataset.
            root (Union[str, None]): Root directory to store the dataset. If None, default HF cache paths will be used.
            human_generated_eval (bool): Whether to use human-generated evaluation data.
        """
        self.name = name
        self.root = root
        self.dataset_root = osp.join(self.root, name) if self.root is not None else None
        self._download()
        self.split_dir = osp.join(self.dataset_root, 'split')
        self.query_dir = osp.join(self.dataset_root, 'stark_qa')
        self.human_generated_eval = human_generated_eval

        self.qa_csv_path = osp.join(
            self.query_dir, 
            'stark_qa_human_generated_eval.csv' if human_generated_eval else 'stark_qa.csv'
        )
        
        self.data = pd.read_csv(self.qa_csv_path)
        self.indices = sorted(self.data['id'].tolist())
        self.split_indices = self.get_idx_split()

    def __len__(self) -> int:
        """
        Return the number of queries in the dataset.

        Returns:
            int: Number of queries.
        """
        return len(self.indices)

    def __getitem__(self, idx: int):
        """
        Get the query, id, answer ids, and meta information for a given index.

        Args:
            idx (int): Index of the query.

        Returns:
            tuple: Query, query id, answer ids, and meta information.
        """
        q_id = self.indices[idx]
        row = self.data[self.data['id'] == q_id].iloc[0]
        query = row['query']
        answer_ids = eval(row['answer_ids'])
        meta_info = None  # Replace with actual meta information if available
        return query, q_id, answer_ids, meta_info

    def _download(self):
        """
        Download the dataset from the Hugging Face repository.
        """
        self.dataset_root = download_hf_folder(
            STARK_QA_DATASET["repo"],
            osp.join(STARK_QA_DATASET["folder"], self.name),
            repo_type="dataset",
            save_as_folder=self.dataset_root,
        )

    def get_idx_split(self, test_ratio: float = 1.0) -> dict:
        """
        Return the indices of train/val/test split in a dictionary.

        Args:
            test_ratio (float): Ratio of test data to include.

        Returns:
            dict: Dictionary with split indices for train, val, and test sets.
        """
        if self.human_generated_eval:
            return {'human_generated_eval': torch.LongTensor(self.indices)}

        split_idx = {}
        for split in ['train', 'val', 'test', 'test-0.1']:
            indices_file = osp.join(self.split_dir, f'{split}.index')
            with open(indices_file, 'r') as f:
                indices = f.read().strip().split('\n')
            query_ids = [int(idx) for idx in indices]
            split_idx[split] = torch.LongTensor([self.indices.index(query_id) for query_id in query_ids])

        if test_ratio < 1.0:
            split_idx['test'] = split_idx['test'][:int(len(split_idx['test']) * test_ratio)]
        return split_idx

    def get_query_by_qid(self, q_id: int) -> str:
        """
        Return the query by query id.

        Args:
            q_id (int): Query id.

        Returns:
            str: Query string.
        """
        row = self.data[self.data['id'] == q_id].iloc[0]
        return row['query']

    def get_subset(self, split: str):
        """
        Return a subset of the dataset.

        Args:
            split (str): Split type ('train', 'val', 'test', 'test-0.1').

        Returns:
            STaRKDataset: Subset of the dataset.
        """
        assert split in ['train', 'val', 'test', 'test-0.1'], "Invalid split specified."
        indices_file = osp.join(self.split_dir, f'{split}.index')
        with open(indices_file, 'r') as f:
            indices = f.read().strip().split('\n')
        subset = copy.deepcopy(self)
        subset.indices = [int(idx) for idx in indices]
        return subset


def download_hf_file(repo, file, repo_type="dataset", save_as_file=None):
    """
    Downloads a file from a Hugging Face repository and saves it to the specified path.

    Args:
        repo (str): The repository name.
        file (str): The file path within the repository to download.
        repo_type (str): The type of the repository (e.g., 'dataset').
        save_as_file (str, optional): The local file path to save the downloaded file. 
                                      If not provided, saves the file in the current directory 
                                      with the same name as the original file.
    """
    # Download the file from the repository
    file_path = hf_hub_download(repo, file, repo_type=repo_type)
    
    # Determine the save path
    if save_as_file is None:
        return file_path
    
    # Create necessary directories
    os.makedirs(os.path.dirname(save_as_file), exist_ok=True)
    
    # Copy the downloaded file to the desired location
    if not os.path.exists(save_as_file) and file_path != save_as_file:
        shutil.copy2(file_path, save_as_file)
    
    print(f"Downloaded <file:{file}> from <repo:{repo}> to <path:{save_as_file}>!")
    return save_as_file

def download_hf_folder(repo, folder, repo_type="dataset", save_as_folder=None):
    """
    Downloads a folder from a Hugging Face repository and saves it to the specified directory.

    Args:
        repo (str): The repository name.
        folder (str): The folder path within the repository to download.
        repo_type (str): The type of the repository (e.g., 'dataset').
        save_as_folder (str, optional): The local directory to save the downloaded folder. 
                                        Defaults to "data/".
    """
    # List all files in the repository
    files = list_repo_files(repo, repo_type=repo_type)
    
    # Filter files that belong to the specified folder
    folder_files = [f for f in files if f.startswith(folder + '/')]
    
    # Download and save each file in the folder
    for file in folder_files:
        file_path = hf_hub_download(repo, file, repo_type=repo_type)
        if save_as_folder is not None:  
            new_file_path = os.path.join(save_as_folder, os.path.relpath(file, folder))
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            if not os.path.exists(new_file_path) and file_path != new_file_path:
                shutil.copy2(file_path, new_file_path)
        else:
            # get the upper dir absolute dir name of the file
            save_as_folder = os.path.dirname(os.path.dirname(file_path))
    print(f"Use file from {file_path}.")
    return save_as_folder



def process_item(i, candidate_id_dict, qa_dataset, get_rel_info, get_text_info):
    """Process a single item with its candidate filtering"""
    initial_score_dict = candidate_id_dict[int(i)]
    candidates = list(initial_score_dict.keys())[:5]
    answer_ids = qa_dataset[i][2]
    filtered_candidates = filter_candidates(candidates, answer_ids)
    
    return int(i), {
        "candidate_ids": filtered_candidates,
        "simiarity": [initial_score_dict[cid] for cid in filtered_candidates],
        "relation_info": [get_rel_info(cid) for cid in filtered_candidates],
        "text_info": [get_text_info(cid) for cid in filtered_candidates],
    }


def process_split_parallel(idx_list, candidate_id_dict, qa_dataset, get_rel_info, get_text_info, desc, max_workers=128):
    """Process a dataset split in parallel"""
    results = {}
    # Create a partial function with the common arguments
    process_func = partial(process_item, 
                         candidate_id_dict=candidate_id_dict, 
                         qa_dataset=qa_dataset,
                         get_rel_info=get_rel_info,
                         get_text_info=get_text_info)
    
    # Use a thread pool for I/O-bound tasks or a process pool for CPU-bound tasks
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and get the futures
        future_to_idx = {executor.submit(process_func, i): i for i in idx_list}
        
        # Process the completed futures with a progress bar
        for future in tqdm(concurrent.futures.as_completed(future_to_idx), 
                          total=len(idx_list), desc=desc):
            idx, result = future.result()
            results[idx] = result
            
    return results


def get_vss_topk(vss, query, query_id):
    initial_score_dict = vss(query, query_id)
    initial_score_dict = {
        int(k): float(v) for k, v in initial_score_dict.items()
    }
    # sort the dictionary by values
    initial_score_dict = dict(sorted(initial_score_dict.items(), key=lambda item: item[1], reverse=True))
    return initial_score_dict

def process_single_example(args):
    """Helper function for parallel processing"""
    idx, qa_dataset, vss = args
    initial_score_dict = get_vss_topk(vss, qa_dataset[idx][0], qa_dataset[idx][1])
    return idx, initial_score_dict

def filter_candidates(candidate_ids, answer_ids, num_answers=1, num_non_answers=4):
    """
    Filter candidates to select specified number of answers and non-answers.
    If not enough answers/non-answers, force selection by adding from answer_ids.
    """
    answer_candidates = [cid for cid in candidate_ids if cid in answer_ids]
    non_answer_candidates = [cid for cid in candidate_ids if cid not in answer_ids]

    if len(answer_candidates) >= num_answers and len(non_answer_candidates) >= num_non_answers:
        selected_answers = random.sample(answer_candidates, num_answers)
        selected_non_answers = random.sample(non_answer_candidates, num_non_answers)
    else:
        if answer_ids:
            selected_answers = [random.choice(answer_ids)]
        else:
            selected_answers = []

        remaining_candidates = [cid for cid in candidate_ids if cid not in selected_answers]

        num_needed = 5 - len(selected_answers)
        if len(remaining_candidates) >= num_needed:
            selected_non_answers = random.sample(remaining_candidates, num_needed)
        else:
            selected_non_answers = remaining_candidates
            while len(selected_answers) + len(selected_non_answers) < 5:
                selected_non_answers.append(random.choice(candidate_ids))

    filtered_candidates = selected_answers + selected_non_answers
    random.shuffle(filtered_candidates)

    return filtered_candidates

def dataset_engine(**kwargs):
    stark_data_path = '/dfs/project/kgrlm/multiagent_reward/trl/data/stark_data_processed'
    # stark_data_path = kwargs.get('stark_data_path', 'stark_data_processed/stark_data_processed')
    
    os.makedirs(stark_data_path, exist_ok=True)

    candidate_id_train_path = osp.join(stark_data_path, 'train_ids.json')
    candidate_id_val_path = osp.join(stark_data_path, 'val_ids.json')
    candidate_id_test_path = osp.join(stark_data_path, 'test_ids.json')

    filtered_train_path = osp.join(stark_data_path, 'filtered_train_ids.json')
    filtered_val_path = osp.join(stark_data_path, 'filtered_val_ids.json')
    filtered_test_path = osp.join(stark_data_path, 'filtered_test_ids.json')

    qa_dataset = STaRKDataset('prime')
    # load_qa('prime', human_generated_eval=False)

    if not osp.exists(candidate_id_train_path):
        
        ############################################################
        idx_split = qa_dataset.get_idx_split()
        
        # shuffle the indices
        random.seed(kwargs.get('seed', 42))
        random.shuffle(idx_split['train'])
        random.shuffle(idx_split['val'])
        random.shuffle(idx_split['test'])
        
        # idx_split = {
        #     'train': [int(i) for i in idx_split['train'][:1000]],
        #     'val': [int(i) for i in idx_split['val'][:100]],
        #     'test': [int(i) for i in idx_split['test'][:200]]
        # }

        idx_split = {
            'train': [int(i) for i in idx_split['train'][:250]],
            'val': [int(i) for i in idx_split['val'][:25]],
            'test': [int(i) for i in idx_split['test'][:100]]
        }

        dataset = "prime"
        emb_model = "text-embedding-ada-002"
        # emb_dir = "/dfs/project/kgrlm/multiagent_reward/emb"
        emb_dir = "examples/pipelines/stark/emb"
        node_emb_dir = osp.join(emb_dir, dataset, emb_model, "doc")
        query_emb_dir = osp.join(emb_dir, dataset, emb_model, "query")
        kb = stark_qa.load_skb(dataset)
        vss = VSS(kb, query_emb_dir, node_emb_dir, emb_model=emb_model, device='cpu')

        kb = stark_qa.load_skb(dataset)
        get_rel_info = GetRelationInfo(kb)
        get_text_info = GetTextInfo(kb)
        text_embedding_tool = GetTextEmbedding()
        node_embedding_tool = GetNodeEmbedding(kb=kb, node_emb_dir=node_emb_dir)
        cosine_sim_tool = ComputeCosineSimilarity(kb=kb)
        ############################################################

        if not osp.exists(emb_dir):
            subprocess.run(["python", "functional/emb_download.py", "--dataset", "prime", "--emb_dir", emb_dir])

        train_args = [(int(i), qa_dataset, vss) for i in idx_split['train']]
        candidate_id_train = {}

        with ThreadPoolExecutor(max_workers=128) as executor:
            futures = [executor.submit(process_single_example, arg) for arg in train_args]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing train set"):
                idx, initial_score_dict = future.result()
                candidate_id_train[int(idx)] = initial_score_dict

        with open(candidate_id_train_path, 'w') as f:
            json.dump(candidate_id_train, f)

        val_args = [(int(i), qa_dataset, vss) for i in idx_split['val']]
        candidate_id_val = {}
        with ThreadPoolExecutor(max_workers=128) as executor:
            futures = [executor.submit(process_single_example, arg) for arg in val_args]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing val set"):
                idx, initial_score_dict = future.result()
                candidate_id_val[int(idx)] = initial_score_dict

        with open(candidate_id_val_path, 'w') as f:
            json.dump(candidate_id_val, f)

        test_args = [(int(i), qa_dataset, vss) for i in idx_split['test']]
        candidate_id_test = {}

        with ThreadPoolExecutor(max_workers=128) as executor:
            futures = [executor.submit(process_single_example, arg) for arg in test_args]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing test set"):
                idx, initial_score_dict = future.result()
                candidate_id_test[int(idx)] = initial_score_dict

        with open(candidate_id_test_path, 'w') as f:
            json.dump(candidate_id_test, f)
    else:
        with open(candidate_id_train_path, 'r') as f:
            candidate_id_train = json.load(f)
        with open(candidate_id_val_path, 'r') as f:
            candidate_id_val = json.load(f)
        with open(candidate_id_test_path, 'r') as f:
            candidate_id_test = json.load(f)


    if not osp.exists(filtered_train_path):
        dataset = "prime"
        emb_model = "text-embedding-ada-002"
        # emb_dir = "/dfs/project/kgrlm/multiagent_reward/emb"
        emb_dir = "examples/pipelines/stark/emb"
        node_emb_dir = osp.join(emb_dir, dataset, emb_model, "doc")
        query_emb_dir = osp.join(emb_dir, dataset, emb_model, "query")
        kb = stark_qa.load_skb(dataset)
        vss = VSS(kb, query_emb_dir, node_emb_dir, emb_model=emb_model, device='cpu')

        kb = stark_qa.load_skb(dataset)
        get_rel_info = GetRelationInfo(kb)
        get_text_info = GetTextInfo(kb)
        text_embedding_tool = GetTextEmbedding()
        node_embedding_tool = GetNodeEmbedding(kb=kb, node_emb_dir=node_emb_dir)
        cosine_sim_tool = ComputeCosineSimilarity(kb=kb)

        # Process train, val, and test splits in parallel
        train_info = process_split_parallel(
            idx_split['train'], 
            candidate_id_train, 
            qa_dataset, 
            get_rel_info, 
            get_text_info, 
            "Filtering train candidates"
        )
        
        # Save results
        with open(filtered_train_path, 'w') as f:
            json.dump(train_info, f)
            
        val_info = process_split_parallel(
            idx_split['val'], 
            candidate_id_val, 
            qa_dataset, 
            get_rel_info, 
            get_text_info, 
            "Filtering val candidates"
        )
        with open(filtered_val_path, 'w') as f:
            json.dump(val_info, f)
            
        
        test_info = process_split_parallel(
            idx_split['test'], 
            candidate_id_test, 
            qa_dataset, 
            get_rel_info, 
            get_text_info, 
            "Filtering test candidates"
        )
        
        with open(filtered_test_path, 'w') as f:
            json.dump(test_info, f)
    else:
        with open(filtered_train_path, 'r') as f:
            train_info = json.load(f)
        with open(filtered_val_path, 'r') as f:
            val_info = json.load(f)
        with open(filtered_test_path, 'r') as f:
            test_info = json.load(f)
    
    length_limit = 1024
    train_info = {int(i): train_info[i] for i in train_info.keys()}
    val_info = {int(i): val_info[i] for i in val_info.keys()}
    test_info = {int(i): test_info[i] for i in test_info.keys()}

    def truncate_rel_text_info(info_dict, length_limit=1024):
        def truncate_text(text, limit):
            if len(text) > limit:
                return text[:limit]
            return text
        for key, value in info_dict.items():
            info_dict[key]['text_info'] = [truncate_text(text, length_limit) for text in value['text_info']]
            info_dict[key]['relation_info'] = [truncate_text(text, length_limit) for text in value['relation_info']]

        return info_dict
    
    LIMIT = 1024
    train_info = truncate_rel_text_info(train_info, LIMIT)
    val_info = truncate_rel_text_info(val_info, LIMIT)
    test_info = truncate_rel_text_info(test_info, LIMIT)
    trainset = [Example(
        question=qa_dataset[i][0],
        question_id=qa_dataset[i][1],
        answer_ids=qa_dataset[i][2],
        candidate_ids=train_info[i]["candidate_ids"],
        relation_info=json.dumps(train_info[i]["relation_info"], indent=2),
        text_info=json.dumps(train_info[i]["text_info"], indent=2),
        emb_scores=[round(float(v), 2) for v in train_info[i]["simiarity"]],
    ).with_inputs('question', "relation_info", "text_info", "emb_scores") for i in train_info.keys()]
    
    valset = [Example(
        question=qa_dataset[i][0],
        question_id=qa_dataset[i][1],
        answer_ids=qa_dataset[i][2],
        candidate_ids=val_info[i]["candidate_ids"],
        relation_info=json.dumps(val_info[i]["relation_info"], indent=2),
        text_info=json.dumps(val_info[i]["text_info"], indent=2),
        emb_scores=[round(float(v), 2) for v in val_info[i]["simiarity"]],
    ).with_inputs('question', "relation_info", "text_info", "emb_scores") for i in val_info.keys()]

    testset = [Example(
        question=qa_dataset[i][0],
        question_id=qa_dataset[i][1],
        answer_ids=qa_dataset[i][2],
        candidate_ids=test_info[i]["candidate_ids"],
        relation_info=json.dumps(test_info[i]["relation_info"], indent=2),
        text_info=json.dumps(test_info[i]["text_info"], indent=2),
        emb_scores=[round(float(v), 2) for v in test_info[i]["simiarity"]],
    ).with_inputs('question', "relation_info", "text_info", "emb_scores") for i in test_info.keys()]

    print(f"Loaded {len(trainset)} training examples and {len(testset)} test examples")
    return trainset, valset, testset

def subdataset_engine(**kwargs):
    """Load a subset of the existing filtered dataset."""
    subset_ratio = kwargs.get('subset_ratio', 0.5)
    random_seed = kwargs.get('random_seed', 42)

    stark_data_path = '/dfs/project/kgrlm/multiagent_reward/trl/data/stark_data_processed'
    # stark_data_path = kwargs.get('stark_data_path', 'stark_data_processed/stark_data_processed')
    
    print(f"\nLoading data from: {stark_data_path}")
    filtered_train_path = osp.join(stark_data_path, 'filtered_train_ids.json')
    filtered_val_path = osp.join(stark_data_path, 'filtered_val_ids.json')
    filtered_test_path = osp.join(stark_data_path, 'filtered_test_ids.json')

    qa_dataset = STaRKDataset('prime')

    # Load existing filtered files
    print(f"Loading filtered files from:")
    print(f"  Train: {filtered_train_path}")
    print(f"  Val: {filtered_val_path}")
    print(f"  Test: {filtered_test_path}")
    
    with open(filtered_train_path, 'r') as f:
        train_info = json.load(f)
    with open(filtered_val_path, 'r') as f:
        val_info = json.load(f)
    with open(filtered_test_path, 'r') as f:
        test_info = json.load(f)
    
    # Convert keys to integers and take subset
    train_keys = list(train_info.keys())
    val_keys = list(val_info.keys())
    test_keys = list(test_info.keys())
    
    # Set random seed for reproducibility
    random.seed(random_seed)
    
    # Calculate subset sizes
    train_subset_size = int(len(train_keys) * subset_ratio)
    val_subset_size = int(len(val_keys) * subset_ratio)
    
    # Randomly select subsets
    train_keys = random.sample(train_keys, train_subset_size)
    val_keys = random.sample(val_keys, val_subset_size)
    
    print(f"\nSubset sizes:")
    print(f"  Train: {train_subset_size} examples (from {len(train_info)} total)")
    print(f"  Val: {val_subset_size} examples (from {len(val_info)} total)")
    print(f"  Test: {len(test_keys)} examples (keeping all)")
    
    # Create subset dictionaries
    train_info = {int(i): train_info[i] for i in train_keys}
    val_info = {int(i): val_info[i] for i in val_keys}
    test_info = {int(i): test_info[i] for i in test_keys}
    
    def truncate_rel_text_info(info_dict, length_limit=1024):
        def truncate_text(text, limit):
            if len(text) > limit:
                return text[:limit]
            return text
        for key, value in info_dict.items():
            info_dict[key]['text_info'] = [truncate_text(text, length_limit) for text in value['text_info']]
            info_dict[key]['relation_info'] = [truncate_text(text, length_limit) for text in value['relation_info']]
        return info_dict
    
    LIMIT = 1024
    train_info = truncate_rel_text_info(train_info, LIMIT)
    val_info = truncate_rel_text_info(val_info, LIMIT)
    test_info = truncate_rel_text_info(test_info, LIMIT)

    trainset = [Example(
        question=qa_dataset[i][0],
        question_id=qa_dataset[i][1],
        answer_ids=qa_dataset[i][2],
        candidate_ids=train_info[i]["candidate_ids"],
        relation_info=json.dumps(train_info[i]["relation_info"], indent=2),
        text_info=json.dumps(train_info[i]["text_info"], indent=2),
        emb_scores=[round(float(v), 2) for v in train_info[i]["simiarity"]],
    ).with_inputs('question', "relation_info", "text_info", "emb_scores") for i in train_info.keys()]
    
    valset = [Example(
        question=qa_dataset[i][0],
        question_id=qa_dataset[i][1],
        answer_ids=qa_dataset[i][2],
        candidate_ids=val_info[i]["candidate_ids"],
        relation_info=json.dumps(val_info[i]["relation_info"], indent=2),
        text_info=json.dumps(val_info[i]["text_info"], indent=2),
        emb_scores=[round(float(v), 2) for v in val_info[i]["simiarity"]],
    ).with_inputs('question', "relation_info", "text_info", "emb_scores") for i in val_info.keys()]

    testset = [Example(
        question=qa_dataset[i][0],
        question_id=qa_dataset[i][1],
        answer_ids=qa_dataset[i][2],
        candidate_ids=test_info[i]["candidate_ids"],
        relation_info=json.dumps(test_info[i]["relation_info"], indent=2),
        text_info=json.dumps(test_info[i]["text_info"], indent=2),
        emb_scores=[round(float(v), 2) for v in test_info[i]["simiarity"]],
    ).with_inputs('question', "relation_info", "text_info", "emb_scores") for i in test_info.keys()]

    return trainset, valset, testset

if __name__ == "__main__":
    # Use the original dataset_engine for full dataset
    # trainset, valset, testset = dataset_engine()
    
    # Or use the subset version
    trainset, valset, testset = subdataset_engine()
    print(f"Loaded {len(trainset)} training examples, {len(valset)} validation examples and {len(testset)} test examples")
