import json
import os
import os.path as osp
import random
import dspy
from typing import Dict, List, Optional, Any
from optimas.utils.example import Example


def load_jsonl(file_path: str) -> List[Dict]:
    """Load data from a JSONL file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]


def dataset_engine(**kwargs):
    """
    Load the PubMedQA dataset and create Example objects.
    By default, loads the complete dataset.

    Args:
        args: Dictionary or object with attributes including:
            - train_size: Number of examples for training (default: None, uses full dataset)
            - data_path: Path to the PubMedQA dataset directory (default: '/dfs/project/kgrlm/parth/Pubmed/')
            - train_file: Name of the training file (default: 'combined_PubMedQA_train.jsonl')
            - test_file: Name of the test file (default: 'combined_PubMedQA_test.jsonl')
            - seed: Random seed for reproducibility (default: 42)

    Returns:
        tuple: (trainset, testset) of Example objects
    """

    # Extract parameters with defaults
    train_size = kwargs.get('train_size', None)
    data_path = kwargs.get('data_path', 'examples/data/')
    train_file = kwargs.get('train_file', 'combined_PubMedQA_train.jsonl')
    test_file = kwargs.get('test_file', 'combined_PubMedQA_test.jsonl')
    seed = kwargs.get('seed', 42)

    # Set random seed for reproducibility
    random.seed(seed)

    # Load data
    train_path = osp.join(data_path, train_file)
    test_path = osp.join(data_path, test_file)

    train_data = load_jsonl(train_path)
    test_data = load_jsonl(test_path)

    # Limit training data if specified (but use full dataset by default)
    if train_size is not None and train_size < len(train_data):
        random.shuffle(train_data)
        train_data = train_data[:train_size]

    # Create Example objects
    train_val_set = []
    for item in train_data:
        context = " ".join(item['context']) if isinstance(item['context'], list) else item['context']
        example = Example(
            question=item['question'],
            context=context,
            groundtruth=item['groundtruth']
        ).with_inputs('question', 'context')
        train_val_set.append(example)

    testset = []
    for item in test_data:
        context = " ".join(item['context']) if isinstance(item['context'], list) else item['context']
        example = Example(
            question=item['question'],
            context=context,
            groundtruth=item['groundtruth']
        ).with_inputs('question', 'context')
        testset.append(example)

    if len(train_val_set) < 20:
        trainset = train_val_set[:-1]
        valset = train_val_set[-1]
    else:
        trainset = train_val_set[:int(len(train_val_set) * 0.95)]
        valset = train_val_set[int(len(train_val_set) * 0.95):]

    print(f"Loaded {len(trainset)} training examples and {len(testset)} test examples")
    return trainset, valset, testset


# Example usage
if __name__ == "__main__":
    # Load the full dataset by default
    trainset, valset, testset = dataset_engine()

    # Print a sample
    print("Sample training example:")
    print(trainset[0])

    print("\nSample test example:")
    print(testset[0])
