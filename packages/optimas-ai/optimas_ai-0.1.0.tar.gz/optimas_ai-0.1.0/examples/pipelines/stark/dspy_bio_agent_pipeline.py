import os
import torch

from examples.metrics.mrr import mrr
from optimas.arch.pipeline import CompoundAgentPipeline
from examples.pipelines.stark.bio_agent import FinalScorer
from examples.pipelines.stark.dspy_bio_agent import RelationScorer, TextScorer
from optimas.utils.example import Example

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CKPT_DIR = os.path.join(SCRIPT_DIR, "checkpoints")


class DSPyBioAgentPipeline(CompoundAgentPipeline):
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
            "relation_scorer": RelationScorer(),
            "text_scorer": TextScorer(),
            "final_scorer": FinalScorer()
        })

        # 3. Wire execution order + eval
        self.construct_pipeline(
            module_order = ["relation_scorer", "text_scorer", "final_scorer"],
            final_output_fields = ["final_scores"],        # match solver_mod’s output
            ground_fields = ["candidate_ids", "answer_ids"],   # Example .groundtruth
            eval_func = mrr
        )
        
        # 4. Load in merged .pth of optimized prompts
        merged_pth = os.path.join(CKPT_DIR, "combined_dspy_prompts.pth")
        if os.path.exists(merged_pth):
            # auto-load from disk if exist
            sd = torch.load(merged_pth, map_location="cpu")
            self.load_state_dict(sd)
            print(f"[DSPyBioAgentPipeline] loaded optimized prompts from {merged_pth}")
        else:
            print(f"[DSPyBioAgentPipeline] no optimized prompts found at {merged_pth}; using defaults")

    def state_dict(self) -> dict:
        # Called by pipeline_eval.py to serialize learned prompts
        return {
            "relation_scorer": self.modules["relation_scorer"].dspy_module,
            "text_scorer":  self.modules["text_scorer"].dspy_module,
            "final_scorer": self.modules["final_scorer"]
        }

    def load_state_dict(self, sd: dict):
        # Called by pipeline_eval.py to inject learned prompts back
        if "relation_scorer" in sd:
            self.modules["relation_scorer"].update({"module": sd["relation_scorer"]})
        if "text_scorer" in sd:
            self.modules["text_scorer"].update({"module": sd["text_scorer"]})
        if "final_scorer" in sd:
            self.modules["final_scorer"].update({"module": sd["final_scorer"]})
