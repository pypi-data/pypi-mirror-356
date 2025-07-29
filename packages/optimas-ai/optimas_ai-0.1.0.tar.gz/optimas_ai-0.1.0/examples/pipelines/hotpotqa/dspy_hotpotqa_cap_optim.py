"""Train all DSPy modules for HotpotQA using MIPROv2 and merge them."""
import os
import json
from pprint import pprint
import time
import random
import os.path as osp

import dspy.evaluate
from examples.pipelines.hotpotqa.dspy_hotpotqa_pipeline import DSPyHotpotQAPipeline
import torch
from tqdm import tqdm
from dotenv import load_dotenv

import dspy
from dspy.evaluate.evaluate import Evaluate
from dspy.teleprompt import MIPROv2, BootstrapFewShotWithRandomSearch

from examples.metrics.f1_score import f1_score
# from examples.pipelines.utils import OptimasAdapter
from examples.datasets.hotpot_qa import dataset_engine
from examples.pipelines.hotpotqa.dspy_modules import DSPyHotPotQAProgram

SCRIPT_DIR = osp.dirname(osp.realpath(__file__))
CKPT_DIR = osp.join(SCRIPT_DIR, "checkpoints")
os.makedirs(CKPT_DIR, exist_ok=True)

load_dotenv()

# Configure DSPy
lm = dspy.LM(model='openai/gpt-4o-mini', max_tokens=1024, temperature=0.6, cache=False)
dspy.settings.configure(lm=lm)
colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
dspy.settings.configure(rm=colbertv2_wiki17_abstracts)


def train_with_mipro(trainset, 
                     valset,
                     testset,
                     num_trials, 
                     auto="medium"
                    ):
    """Train the entire pipeline using MIPROv2"""
    cap_program = DSPyHotpotQAPipeline()
    program = cap_program.get_dspy_module()


    def metric(example, prediction, trace=None):
        answer = prediction.answer

        f1_score_val = f1_score(answer, example.gd_answer)
        return f1_score_val

    optimizer = MIPROv2(
        metric=metric,
        auto=auto,
        max_bootstrapped_demos=0, 
        max_labeled_demos=0,
        num_threads=24,
        verbose=True
    )
    
    print(f"Starting MIPROv2 optimization (mode: {auto})")
    print(f"Training set size: {len(trainset)}")
    print(f"Validation set size: {len(valset)}")

    optimized_program = optimizer.compile(
        program,
        trainset=trainset,
        valset=valset,
        num_trials=num_trials,
        requires_permission_to_run=False
    )

    cap_program.syncronize_modules(optimized_program)
    test_metrics = sum(cap_program.evaluate_multiple(testset)) / len(testset)
    print(f"Test F1: {test_metrics:.3f}")

    print(f"LM history: {len(lm.history)}")
    print(lm.history[-4:])
    
    modules = {
        "question_rewriter": optimized_program.question_rewriter,
        "info_extractor": optimized_program.info_extractor,
        "hint_generator": optimized_program.hint_generator,
        "answer_generator": optimized_program.answer_generator
    }
    
    for name, module in modules.items():
        ckpt = osp.join(CKPT_DIR, f"checkpoint_{name}_mipro.json")

        module_state = {
            "class": module.__class__.__name__,
            "signature": str(module.signature) if hasattr(module, 'signature') else None,
        }
        with open(ckpt, "w") as f:
            json.dump(module_state, f, indent=2)
    
    return optimized_program, modules


def merge_and_save_modules(optimized_program):
    """Merge optimized modules and save in a format compatible with the pipeline"""
    
    merged = {
        "rewriter_module": optimized_program.question_rewriter,
        "extractor_module": optimized_program.info_extractor,
        "retriever_k": 10,  # Default k value, should randomize for hotpotqa eval
        "retriever_randomize": True,  # for evaluation
        "hint_module": optimized_program.hint_generator,
        "answer_module": optimized_program.answer_generator
    }
    
    # torch.save(merged, osp.join(CKPT_DIR, "combined_dspy_modules.pth"))
    
    # for inspection
    text_state = {
        "rewriter": str(optimized_program.question_rewriter),
        "extractor": str(optimized_program.info_extractor),
        "hint": str(optimized_program.hint_generator),
        "answer": str(optimized_program.answer_generator),
    }
    
    with open(osp.join(CKPT_DIR, "optimized_modules_info.json"), "w") as f:
        json.dump(text_state, f, indent=2)

    with open(osp.join(CKPT_DIR, "module_call_history.json"), "w") as f:
        json.dump(lm.history, f, indent=2)
    
    return merged


if __name__ == "__main__":
    print("Loading dataset...")
    trainset, valset, testset = dataset_engine()
    
    trainset = trainset[:1000]
    valset = valset[:20]
    
    # Train with MIPROv2
    start_time = time.time()
    optimized_program, modules = train_with_mipro(
        trainset=trainset,
        valset=valset,
        testset=testset,
        num_trials=30,
        auto="medium"
    )
    
    # training_time = time.time() - start_time
    # print(f"\nTraining completed in {training_time:.2f} seconds")
    
    # merged = merge_and_save_modules(optimized_program)
    
    # print("\n[train_hotpotqa_dspy] Training complete - modules optimized and merged.")
    # print(f"Checkpoints saved to: {CKPT_DIR}")
    
    # print("\nOptimization Summary:")
    # for name in ["question_rewriter", "info_extractor", "hint_generator", "answer_generator"]:
    #     print(f"  {name}: Optimized with MIPROv2")
    
    # print("\nQuick eval on 5 examples:")
    # for i, ex in enumerate(testset[50:55]):
    #     pred = optimized_program(question=ex.question)
    #     f1_val, _, _ = f1_score(pred.answer, ex.gd_answer)
    #     print(f"  Example {i+1}: F1 = {f1_val:.3f}")
