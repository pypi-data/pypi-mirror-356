import joblib
import dspy
from datasets import load_dataset
import random
from optimas.utils.example import Example


def dataset_engine(*args, **kwargs):

    train_size = kwargs.get('train_size', 1000)
    raw_data = load_dataset("bigcode/bigcodebench", split="v0.1.3")
    splits = ['train'] * train_size + ['test'] * (len(raw_data) - train_size)

    random.seed(42)
    random.shuffle(splits)

    dataset = [Example(
        question=raw_data[i]['instruct_prompt'],
        code=raw_data[i]['code_prompt'] + raw_data[i]['canonical_solution'],
        unit_tests=raw_data[i]['test'],
        task_id=raw_data[i]['task_id'],
        entry_point='task_func'
    ).with_inputs('question') for i in range(len(raw_data))]


    train_val_set = [x for x, split in zip(dataset, splits) if split == 'train']
    if len(train_val_set) < 20:
        trainset = train_val_set[:-1]
        valset = train_val_set[-1]
    else:
        trainset = train_val_set[:int(len(train_val_set) * 0.95)]
        valset = train_val_set[int(len(train_val_set) * 0.95):]
    testset = [x for x, split in zip(dataset, splits) if split == 'test']

    return trainset, valset, testset
