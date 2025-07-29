import os
import os.path as osp
from dotenv import load_dotenv
import joblib
import dspy
from typing import List
from transformers import AutoTokenizer
from tqdm import tqdm
import numpy as np

from optimas.arch.base import BaseModule
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.adapt import create_module_from_signature
from examples.metrics.mrr import mrr
from optimas.utils.api import get_llm_output
from examples.datasets.stark_prime import dataset_engine

import os.path as osp
import torch
import json


class RelationScorerSignature(dspy.Signature):
    """Given a question and a list of 5 entities with their relational information, assign each entity a relevance score (between 0 and 1) based on how well its relations match the information in the question."""
    question: str = dspy.InputField(
        prefix="Query: "
    )
    relation_info: str = dspy.InputField(
        prefix="Relational Information: "
    )
    relation_scores: str = dspy.OutputField(
        prefix="Json Scores \{1: score1, ..., 5: score5\}: "
    )

# """Given a question and a list of 5 entities, each with detailed property information, assign a relevance score between 0 and 1 to each entity based on the following criteria:"""


class TextScorerSignature(dspy.Signature):
    """Given a question and a list of 5 entities with their property information, assign each entity a relevance score between 0 and 1 based on how well its properties match the requirements described in the question."""
    question: str = dspy.InputField(
        prefix="Query: "
    )
    text_info: str = dspy.InputField(
        prefix="Property Information: "
    )
    text_scores: str = dspy.OutputField(
        prefix="Json Scores \{1: score1, ..., 5: score5\}: "
    )


class FinalScorer(BaseModule):
    def __init__(self):
        super().__init__(
            description="Given a question, assess the importance of textual properties, relational cues, and general semantics in retrieving an entity. Combine the three score lists into a final score list using weighted aggregation.",
            input_fields=["question", "emb_scores", "relation_scores", "text_scores"],
            output_fields=["final_scores"],
            variable={
                'relation_weight': 0.1,
                'text_weight': 0.1
            },
            variable_search_space={
                'relation_weight': [0.1, 1.0],
                'text_weight': [0.1, 1.0]
            }
        )

    def forward(self, **inputs):
        question = inputs.get("question")
        emb_scores = inputs.get("emb_scores")
        relation_scores = inputs.get("relation_scores")
        text_scores = inputs.get("text_scores")
        
        try:
            relation_scores = json.loads(relation_scores).values()
            relation_scores = [float(x) for x in relation_scores]
            assert len(relation_scores) == 5
        except:
            relation_scores = [0 for _ in range(5)]
        try:
            text_scores = json.loads(text_scores).values()
            text_scores = [float(x) for x in text_scores]
            assert len(text_scores) == 5
        except:
            text_scores = [0 for _ in range(5)]

        relation_weight = self.variable['relation_weight']
        text_weight = self.variable['text_weight']

        final_scores = [relation_weight * r + text_weight * t + e for r, t, e in zip(relation_scores, text_scores, emb_scores)]
        return {"final_scores": [round(x, 2) for x in final_scores]}


def pipeline_engine(*args, **kwargs):

    lm = dspy.LM(
        model="anthropic/claude-3-haiku-20240307",
        max_tokens=256,
        temperature=0.6,
    )
    dspy.settings.configure(lm=lm)
    dataset = kwargs.get('dataset', None)

    pipeline = CompoundAgentPipeline(*args, **kwargs)
    pipeline.register_modules(
        {
            "relation_scorer": create_module_from_signature(RelationScorerSignature),
            "text_scorer": create_module_from_signature(TextScorerSignature),
            "final_scorer": FinalScorer(),
        }
    )


    pipeline.construct_pipeline(
        module_order=[
            "relation_scorer",
            "text_scorer",
            "final_scorer"
        ],
        final_output_fields=["final_scores"],
        ground_fields=["candidate_ids", "answer_ids"],
        eval_func=mrr
    )
    return pipeline


if __name__ == "__main__":

    dotenv_path = osp.expanduser("/dfs/project/kgrlm/common/.env")
    load_dotenv(dotenv_path)
    
    trainset, valset, testset = dataset_engine()
    pipeline = pipeline_engine()
    
    # pred = pipeline(**testset[0])
    # metric = pipeline.evaluate(example=testset[0], prediction=pred)
    # print(metric)

    pipeline.max_eval_workers = 2
    metrics = pipeline.evaluate_multiple(testset)
    print(metrics)
    print(np.mean(metrics))
    import pdb; pdb.set_trace()

