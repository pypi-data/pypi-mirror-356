import dspy

from optimas.arch.base import BaseModule
from examples.pipelines.stark.bio_agent import RelationScorerSignature, TextScorerSignature


class RelationScorer(BaseModule):
    def __init__(self):
        super().__init__(
            description="Relation Scorer",
            input_fields=["question", "relation_info"],
            output_fields=["relation_scores"],
        )
        self.dspy_module = dspy.Predict(RelationScorerSignature)

    @property
    def variable(self):
        return {"module": self.dspy_module}

    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]


    def forward(self, question: str, relation_info: str):
        return self.dspy_module(question=question, relation_info=relation_info)


class TextScorer(BaseModule):
    def __init__(self):
        super().__init__(
            description="Text Scorer",
            input_fields=["question", "text_info"],
            output_fields=["text_scores"],
        )
        self.dspy_module = dspy.Predict(TextScorerSignature)

    @property
    def variable(self):
        return {"module": self.dspy_module}

    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]
            

    def forward(self, question: str, text_info: str):
        return self.dspy_module(question=question, text_info=text_info)
