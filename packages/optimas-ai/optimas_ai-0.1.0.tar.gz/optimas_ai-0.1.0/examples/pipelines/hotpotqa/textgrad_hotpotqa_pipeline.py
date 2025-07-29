"""Evaluation‑time pipeline that loads the merged TextGrad prompts."""
import os, torch, pandas as pd, os.path as osp
from optimas.arch.pipeline import CompoundAgentPipeline
from examples.metrics.f1_score import f1_score
from examples.pipelines.hotpotqa.modules import (
    TextGradQuestionRewriter, TextGradInfoExtractor, WikipediaRetriever,
    TextGradHintGenerator, TextGradAnswerGenerator
)

SCRIPT_DIR = osp.dirname(osp.realpath(__file__))
CKPT_DIR   = osp.join(SCRIPT_DIR, "checkpoints")

class TextGradHotpotQAPipeline(CompoundAgentPipeline):
    def __init__(self, log_dir=None):
        super().__init__(log_dir=log_dir)
        self.register_modules({
            "question_rewriter": TextGradQuestionRewriter(),
            "info_extractor":   TextGradInfoExtractor(),
            "wikipedia_retriever": WikipediaRetriever(k=1, search_space=(1, 5, 10, 25)),
            "hint_generator":   TextGradHintGenerator(),
            "answer_generator": TextGradAnswerGenerator()
        })
        with self.context({
            'wikipedia_retriever': {'randomize_search_variable': True}
        }):
            pass
        self.construct_pipeline(
            module_order=[
                "question_rewriter", "info_extractor", "wikipedia_retriever",
                "hint_generator", "answer_generator"
            ],
            final_output_fields=["answer"],
            ground_fields=["gd_answer"],
            eval_func=f1_score
        )
        merged = osp.join(CKPT_DIR, "combined_textgrad_prompts.pth")
        if os.path.exists(merged):
            self.load_state_dict(torch.load(merged, map_location="cpu"))
            print(f"[HotpotQAPipeline] loaded prompts from {merged}")
        else:
            print("[HotpotQAPipeline] using default prompts – none trained yet")

    # state serialization for pipeline_eval.py
    def state_dict(self):
        return {
            "rewriter_prompt": self.modules["question_rewriter"].prompt.value,
            "extractor_prompt": self.modules["info_extractor"].prompt.value,
            "retriever_k": self.modules["wikipedia_retriever"].variable["k"],
            "retriever_randomize": True,
            "hint_prompt": self.modules["hint_generator"].prompt.value,
            "answer_prompt": self.modules["answer_generator"].prompt.value
        }

    def load_state_dict(self, sd):
        self.modules["question_rewriter"].prompt.value = sd["rewriter_prompt"]
        self.modules["info_extractor"].prompt.value = sd["extractor_prompt"]
        self.modules["wikipedia_retriever"].variable = {"k": sd["retriever_k"]}
        if sd.get("retriever_randomize", False):
            self.modules["wikipedia_retriever"].context(randomize_search_variable=True, apply=True)
        self.modules["hint_generator"].prompt.value = sd["hint_prompt"]
        self.modules["answer_generator"].prompt.value = sd["answer_prompt"]

    # optional report (not run off pure pipeline_eval.py)
    def report_by_model(self, testset):
        records = []
        for ex in testset:
            # Run with randomized k value to test different retrieval depths
            with self.modules["wikipedia_retriever"].context(randomize_search_variable=True):
                pred = self(question=ex.question)
                traj = pred.traj
                
                # F1 score
                f1, _, _ = f1_score(pred.answer, ex.gd_answer)
                
                records.append({
                    "rewriter": traj["question_rewriter"]["output"]["rewriter_model"],
                    "extractor": traj["info_extractor"]["output"]["extractor_model"],
                    "retriever_k": self.modules["wikipedia_retriever"].variable["k"],
                    "hint": traj["hint_generator"]["output"]["hint_model"],
                    "answer": traj["answer_generator"]["output"]["answer_model"],
                    "prediction": pred.answer,
                    "groundtruth": ex.gd_answer,
                    "f1_score": f1
                })
                
        df = pd.DataFrame(records)
        
        print("=== Overall Performance ===")
        print(f"Average F1 Score: {df.f1_score.mean():.4f}")
        
        # Performance by model type (wip)
        print("\n=== Performance by Model Type ===")
        for col in ["rewriter", "extractor", "hint", "answer"]:
            print(f"\n--- By {col} model ---")
            for model in sorted(df[col].unique()):
                subset = df[df[col] == model]
                print(f"Model {model} ({len(subset)} examples): F1 = {subset.f1_score.mean():.4f}")
        
        print("\n=== Performance by k value ===")
        for k in sorted(df.retriever_k.unique()):
            subset = df[df.retriever_k == k]
            print(f"k = {k} ({len(subset)} examples): F1 = {subset.f1_score.mean():.4f}")
        
        return df

# factory for pipeline_eval.py
def pipeline_engine(*args, **kwargs):
    return TextGradHotpotQAPipeline(*args, **kwargs)