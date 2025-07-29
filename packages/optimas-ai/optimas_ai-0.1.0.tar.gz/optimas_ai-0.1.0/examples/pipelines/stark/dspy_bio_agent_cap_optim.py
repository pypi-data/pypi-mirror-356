"""Train all DSPy modules for HotpotQA using MIPROv2 and merge them."""
import os
import json
import time
import dspy
import os.path as osp

import dspy.evaluate
from dspy.teleprompt import MIPROv2
from dotenv import load_dotenv


from examples.metrics.mrr import mrr
from examples.datasets.stark_prime import dataset_engine
from examples.pipelines.stark.dspy_bio_agent_pipeline import DSPyBioAgentPipeline

SCRIPT_DIR = osp.dirname(osp.realpath(__file__))
CKPT_DIR = osp.join(SCRIPT_DIR, "checkpoints")
os.makedirs(CKPT_DIR, exist_ok=True)

# load_dotenv()

# Configure DSPy# claude-3-5-haiku-20241022
lm = dspy.LM(model='anthropic/claude-3-haiku-20240307', max_tokens=256, temperature=0.6, cache=False)
dspy.settings.configure(lm=lm)


def train_with_mipro(trainset, 
                     valset,
                     testset,
                     num_trials, 
                     auto="medium"
                    ):
    """Train the entire pipeline using MIPROv2"""
    cap_program = DSPyBioAgentPipeline()
    program = cap_program.get_dspy_module()


    def metric(example, prediction, trace=None):
        final_scores = prediction.final_scores

        answer_ids = example.answer_ids
        candidate_ids = example.candidate_ids

        acc = mrr(answer_ids, final_scores, candidate_ids)
        return acc

    optimizer = MIPROv2(
        metric=metric,
        auto=auto,
        max_bootstrapped_demos=0, 
        max_labeled_demos=0,
        num_threads=1,
        max_errors=100,
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
        "relation_scorer": optimized_program.relation_scorer,
        "text_scorer": optimized_program.text_scorer,
        "final_scorer": optimized_program.final_scorer
    }
    
    for name, module in modules.items():
        ckpt = osp.join(CKPT_DIR, f"checkpoint_{name}_mipro.json")

        module_state = {
            "class": module.__class__.__name__,
            "signature": str(module.signature) if hasattr(module, 'signature') else None,
        }
        with open(ckpt, "w") as f:
            json.dump(module_state, f, indent=2)
    
    return cap_program, modules


def merge_and_save_modules(optimized_program):
    """Merge optimized modules and save in a format compatible with the pipeline"""
    
    merged = {
        "relation_scorer": optimized_program.relation_scorer,
        "text_scorer": optimized_program.text_scorer,
        "final_scorer": optimized_program.final_scorer
    }
    
    # torch.save(merged, osp.join(CKPT_DIR, "combined_dspy_modules.pth"))
    
    # for inspection
    text_state = {
        "relation_scorer": str(optimized_program.relation_scorer),
        "text_scorer": str(optimized_program.text_scorer),
        "final_scorer": str(optimized_program.final_scorer),
    }
    
    with open(osp.join(CKPT_DIR, "optimized_modules_info.json"), "w") as f:
        json.dump(text_state, f, indent=2)

    with open(osp.join(CKPT_DIR, "module_call_history.json"), "w") as f:
        json.dump(lm.history, f, indent=2)
    
    return merged


if __name__ == "__main__":
    print("Loading dataset...")

    dotenv_path = osp.expanduser("/dfs/project/kgrlm/common/.env")
    load_dotenv(dotenv_path)
    
    trainset, valset, testset = dataset_engine()
    
    trainset = trainset[:1000]
    valset = valset[:20]
    
    # Train with MIPROv2
    start_time = time.time()
    cap_program, modules = train_with_mipro(
        trainset=trainset,
        valset=valset,
        testset=testset,
        num_trials=50,
        auto="medium"
    )

    optimized_program
    