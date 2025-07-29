import torch
import pandas as pd
import os
from sklearn.metrics import classification_report

from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.utils.example import Example

from examples.pipelines.pubmed.pubmed_agents import pubmed_eval_func
from examples.pipelines.pubmed.dspy_pubmed import ContextAnalystModule, ProblemSolverModule


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CKPT_DIR = os.path.join(SCRIPT_DIR, "checkpoints")


class DSPyPubMedQAPipeline(CompoundAgentPipeline):
    """
    A pipeline that (1) prompt‑tunes via DSPy, (2) loads
    those prompts via state_dict, and (3) can be
    passed to eval_pipeline() for final eval.
    """
    def __init__(self, log_dir: str = None):
        # 1. super to get .register_modules and .construct_pipeline
        super().__init__(log_dir=log_dir)

        
        # 2. Instantiate both TextGrad modules
        self.register_modules({
            "context_analyst": ContextAnalystModule(),
            "problem_solver":  ProblemSolverModule()
        })

        # 3. Wire execution order + eval
        self.construct_pipeline(
            module_order = ["context_analyst", "problem_solver"],
            final_output_fields = ["answer"],        # match solver_mod’s output
            ground_fields = ["groundtruth"],   # Example .groundtruth
            eval_func = pubmed_eval_func
        )
        
        # 4. Load in merged .pth of optimized prompts
        merged_pth = os.path.join(CKPT_DIR, "combined_dspy_prompts.pth")
        if os.path.exists(merged_pth):
            # auto-load from disk if exist
            sd = torch.load(merged_pth, map_location="cpu")
            self.load_state_dict(sd)
            print(f"[DSPyPubMedQAPipeline] loaded optimized prompts from {merged_pth}")
        else:
            print(f"[DSPyPubMedQAPipeline] no optimized prompts found at {merged_pth}; using defaults")

    def state_dict(self) -> dict:
        # Called by pipeline_eval.py to serialize learned prompts
        return {
            "context_prompt": self.modules["context_analyst"].dspy_module,
            "solver_prompt":  self.modules["problem_solver"].dspy_module
        }

    def load_state_dict(self, sd: dict):
        # Called by pipeline_eval.py to inject learned prompts back
        if "context_prompt" in sd:
            self.modules["context_analyst"].update({"module": sd["context_prompt"]})
        if "solver_prompt" in sd:
            self.modules["problem_solver"].update({"module": sd["solver_prompt"]})

    def report_by_model(self, testset):
        """
        Run over the testset one more time, collect which model
        was used at each stage, and print per‑model and overall reports.
        """
        records = []
        for ex in testset:
            pred = self(context=ex.context, question=ex.question)
            records.append({
                "prediction":  pred.answer,
                "groundtruth": ex.groundtruth
            })

        df = pd.DataFrame(records)

        print("=== Overall performance ===")
        print(classification_report(df.groundtruth, df.prediction))

        for m in sorted(df.ctx_model.unique()):
            sub = df[df.ctx_model == m]
            print(f"\n--- Context Analyst = {m} ({len(sub)}) examples ---")
            print(classification_report(sub.groundtruth, sub.prediction))

        for m in sorted(df.sol_model.unique()):
            sub = df[df.sol_model == m]
            print(f"\n--- Problem Solver = {m} ({len(sub)}) examples ---")
            print(classification_report(sub.groundtruth, sub.prediction))
