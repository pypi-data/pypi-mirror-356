"""
Evaluation-time pipeline that loads the optimized DSPy modules.

NUM_REPEAT=3
OUTPUT_DIR=examples/pipelines/hotpotqa/eval/dspy_hotpoqa
DATASET=hotpotqa
PIPELINE_NAME=dspy_hotpotqa_pipeline
RUN_NAME=dspy-repeat$NUM_REPEAT

CUDA_VISIBLE_DEVICES=0 caffeinate python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --num_repeat $NUM_REPEAT \
    --dotenv_path /Users/aaronlee/Documents/Research/preference-prompter/.env \
    --requires_permission_to_run=False
"""
import os
from examples.datasets.hotpot_qa import dataset_engine
import torch
import pandas as pd
import os.path as osp
import dspy
from optimas.arch.pipeline import CompoundAgentPipeline
from examples.metrics.f1_score import f1_score
from examples.pipelines.hotpotqa.dspy_modules import (
    DSPyQuestionRewriter, DSPyInfoExtractor, WikipediaRetriever,
    DSPyHintGenerator, DSPyAnswerGenerator
)

SCRIPT_DIR = osp.dirname(osp.realpath(__file__))
CKPT_DIR = osp.join(SCRIPT_DIR, "checkpoints")

# CompoundAgentPipeline -> DSPy Modules
class DSPyHotpotQAPipeline(CompoundAgentPipeline):
    def __init__(self, log_dir=None, max_workers=25):
        super().__init__(log_dir=log_dir)
        
        lm = dspy.LM(model='openai/gpt-4o-mini', max_tokens=1024, temperature=0.6)
        dspy.settings.configure(lm=lm)
        colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
        dspy.settings.configure(rm=colbertv2_wiki17_abstracts)
        
        self.register_modules({
            "question_rewriter": DSPyQuestionRewriter(),
            "info_extractor": DSPyInfoExtractor(),
            "wikipedia_retriever": WikipediaRetriever(k=1, variable_search_space=(1, 5, 10, 100)),
            "hint_generator": DSPyHintGenerator(),
            "answer_generator": DSPyAnswerGenerator()
        })
        
        # Enable retriever randomization
        self.modules["wikipedia_retriever"].context(
            randomize_search_variable=True,
            apply=True
        )
        self.modules["wikipedia_retriever"].randomize_search_variable = True
        
        self.construct_pipeline(
            module_order=[
                "question_rewriter", "info_extractor", "wikipedia_retriever",
                "hint_generator", "answer_generator"
            ],
            final_output_fields=["answer"],
            ground_fields=["gd_answer"],
            eval_func=f1_score
        )
        
        # Load optimized modules if available
        merged_path = osp.join(CKPT_DIR, "combined_dspy_modules.pth")
        if os.path.exists(merged_path):
            self.load_state_dict(torch.load(merged_path, map_location="cpu"))
            print(f"[DSPyHotpotQAPipeline] Loaded optimized modules from {merged_path}")
        else:
            print("[DSPyHotpotQAPipeline] Using default modules - none optimized yet")

    def state_dict(self):
        """Return current state of all modules"""
        return {
            "rewriter_module": self.modules["question_rewriter"].dspy_module,
            "extractor_module": self.modules["info_extractor"].dspy_module,
            "retriever_k": self.modules["wikipedia_retriever"].variable["k"],
            "retriever_randomize": True,
            "hint_module": self.modules["hint_generator"].dspy_module,
            "answer_module": self.modules["answer_generator"].dspy_module
        }

    def load_state_dict(self, sd):
        """Load optimized modules"""
        if "rewriter_module" in sd:
            self.modules["question_rewriter"].update({"module": sd["rewriter_module"]})
        if "extractor_module" in sd:
            self.modules["info_extractor"].update({"module": sd["extractor_module"]})
        if "hint_module" in sd:
            self.modules["hint_generator"].update({"module": sd["hint_module"]})
        if "answer_module" in sd:
            self.modules["answer_generator"].update({"module": sd["answer_module"]})
        
        # Update retriever settings
        self.modules["wikipedia_retriever"].update({"k": sd.get("retriever_k", 10)})
        if sd.get("retriever_randomize", False):
            self.modules["wikipedia_retriever"].context(randomize_search_variable=True, apply=True)

    def report_by_model(self, testset):
        """Optional detailed performance report"""
        records = []
        for ex in testset:
            # Run, randomized k value
            with self.modules["wikipedia_retriever"].context(randomize_search_variable=True):
                pred = self(question=ex.question)
                traj = pred.traj
                
                f1, _, _ = f1_score(pred.answer, ex.gd_answer)
                
                records.append({
                    "retriever_k": self.modules["wikipedia_retriever"].variable["k"],
                    "prediction": pred.answer,
                    "groundtruth": ex.gd_answer,
                    "f1_score": f1
                })
                
        df = pd.DataFrame(records)
        
        print("=== Overall Performance ===")
        print(f"Average F1 Score: {df.f1_score.mean():.4f}")
        
        print("\n=== Performance by k value ===")
        for k in sorted(df.retriever_k.unique()):
            subset = df[df.retriever_k == k]
            print(f"k = {k} ({len(subset)} examples): F1 = {subset.f1_score.mean():.4f}")
        
        return df


def pipeline_engine(*args, **kwargs):
    return DSPyHotpotQAPipeline(*args, **kwargs)
