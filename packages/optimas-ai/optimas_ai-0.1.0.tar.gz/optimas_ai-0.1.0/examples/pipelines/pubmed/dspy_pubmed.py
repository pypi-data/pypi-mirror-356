from typing import Literal
import dspy
from optimas.arch.base import BaseModule


class ContextAnalystSignature(dspy.Signature):
    """You are supposed to summarize the key information from the given context to answer the provided question."""

    context = dspy.InputField(prefix="Here is the given context:")
    question = dspy.InputField(desc="Question")
    summary = dspy.OutputField(desc="Summary of the context")


class ContextAnalystModule(BaseModule):
    def __init__(self,):
        self.dspy_module = dspy.Predict(ContextAnalystSignature)
        super().__init__(
            description="Context Analyst extracts and summarizes key information from a given context.",
            input_fields=["context", "question"],
            output_fields=["summary"],
        )

    
    @property
    def variable(self):
        return {"module": self.dspy_module}

    
    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]
    
        
    def forward(self, context: str, question: str):
        response = self.dspy_module(context=context, question=question)
        
        return {"summary": response.summary}


class ProblemSolverSignature(dspy.Signature):
    """You are supposed to provide a solution to a given problem based on the provided summary."""

    question: str = dspy.InputField(desc="Question")
    summary: str = dspy.InputField(desc="Summary of relevant information")
    answer: Literal["yes", "no", "maybe"] = dspy.OutputField(desc="Answer[yes/no/maybe]")


class ProblemSolverModule(BaseModule):
    """
    Module that interprets the Context Analyst's summary and determines
    the correct yes/no/maybe answer based on evidence.
    """
    
    def __init__(self,):
        """
        Initialize the Problem Solver Module.
        
        Args:
            model (str): Default model to use (will be overridden by selected model)
            max_tokens (int): Maximum tokens for generation
            temperature (float): Temperature for generation
        """
        super().__init__(
            description="Problem Solver determines the correct yes/no/maybe answer based on the provided summary.",
            input_fields=["question", "summary"],
            output_fields=["answer"],
        )
        
        self.dspy_module = dspy.Predict(ProblemSolverSignature)
        self._optimizable = True


    @property
    def variable(self):
        return {"module": self.dspy_module}


    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]


    def forward(self, question: str, summary: str):
        response = self.dspy_module(question=question, summary=summary)
        
        return {"answer": str(response.answer)}
