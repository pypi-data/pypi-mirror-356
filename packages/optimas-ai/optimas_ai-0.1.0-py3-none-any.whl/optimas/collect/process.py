import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List

import os
import os.path as osp
import json
from tqdm import tqdm
import numpy as np
import dspy
import hashlib
from datasets import Dataset, DatasetDict

from optimas.arch.pipeline import CompoundAgentPipeline


def process_example(pipeline, example) -> Dict[str, Any]:
    """Process a single example through the pipeline with error handling."""
    try:
        pred = pipeline(**{k: getattr(example, k) for k in pipeline.required_input_fields})
        score = pipeline.evaluate(example, pred)
        return example, pred, score
    except Exception as e:
        print(f"Error processing example: {str(e)}")
        return None


def process_dataset_parallel(dataset: List, pipeline: CompoundAgentPipeline, max_workers: int = 4) -> tuple:
    """
    Process dataset in parallel using multiple threads.
    
    Args:
        dataset: List of examples to process
        max_workers: Number of parallel threads to use
        batch_size: Number of examples to process
    
    Returns:
        tuple: (processed examples, list of f1 scores)
    """
    examples, preds, scores = [], [], []
    
    # Thread-safe counter for progress bar
    counter_lock = threading.Lock()
    counter = {"processed": 0}
    
    # Create progress bar
    pbar = tqdm(total=len(dataset), desc="Processing examples")
    
    def update_progress(_):
        with counter_lock:
            counter["processed"] += 1
            pbar.update(1)
    
    # Process examples in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_example = {
            executor.submit(process_example, pipeline=pipeline, example=example): example 
            for example in dataset
        }
        
        # Process completed tasks
        for future in as_completed(future_to_example):
            result = future.result()
            if result is not None:
                examples.append(result[0])
                preds.append(result[1])
                scores.append(result[2])
            update_progress(future)
    
    pbar.close()
    
    return examples, preds, scores

