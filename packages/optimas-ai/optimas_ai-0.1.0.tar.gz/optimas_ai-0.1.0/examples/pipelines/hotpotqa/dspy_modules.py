"""
DSPy modules for HotPotQA pipeline, similar to textgrad_modules.py but using DSPy.
Place this in examples/pipelines/hotpotqa/dspy_modules.py
"""
import dspy
from optimas.arch.base import BaseModule
from examples.pipelines.hotpotqa.four_agents import (
    QuestionRewriter as QuestionRewriterSignature,
    InfoExtractor as InfoExtractorSignature,
    HintGenerator as HintGeneratorSignature,
    AnswerGenerator as AnswerGeneratorSignature,
    WikipediaRetriever
)


class DSPyQuestionRewriter(BaseModule):
    def __init__(self):
        super().__init__(
            description="Rephrase question using DSPy",
            input_fields=["question"],
            output_fields=["rewritten_query"],
        )
        self.dspy_module = dspy.ChainOfThought(QuestionRewriterSignature)
        self._optimizable = True

    @property
    def variable(self):
        return {"module": self.dspy_module}

    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]

    def forward(self, question):
        result = self.dspy_module(question=question)
        return {"rewritten_query": result.rewritten_query}


class DSPyInfoExtractor(BaseModule):
    def __init__(self):
        super().__init__(
            description="Extract search keywords using DSPy",
            input_fields=["rewritten_query"],
            output_fields=["search_keywords"],
        )
        self.dspy_module = dspy.ChainOfThought(InfoExtractorSignature)
        self._optimizable = True

    @property
    def variable(self):
        return {"module": self.dspy_module}

    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]

    def forward(self, rewritten_query):
        result = self.dspy_module(rewritten_query=rewritten_query)
        return {"search_keywords": result.search_keywords}


class DSPyHintGenerator(BaseModule):
    def __init__(self):
        super().__init__(
            description="Generate hints using DSPy",
            input_fields=["rewritten_query", "retrieve_content"],
            output_fields=["hints"],
        )
        self.dspy_module = dspy.ChainOfThought(HintGeneratorSignature)
        self._optimizable = True

    @property
    def variable(self):
        return {"module": self.dspy_module}

    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]

    def forward(self, rewritten_query, retrieve_content):
        result = self.dspy_module(
            rewritten_query=rewritten_query,
            retrieve_content=retrieve_content
        )
        return {"hints": result.hints}


class DSPyAnswerGenerator(BaseModule):
    def __init__(self):
        super().__init__(
            description="Generate answer using DSPy",
            input_fields=["rewritten_query", "hints"],
            output_fields=["answer"],
        )
        self.dspy_module = dspy.ChainOfThought(AnswerGeneratorSignature)
        self._optimizable = True

    @property
    def variable(self):
        return {"module": self.dspy_module}

    def update(self, variable):
        if "module" in variable:
            self.dspy_module = variable["module"]

    def forward(self, rewritten_query, hints):
        result = self.dspy_module(
            rewritten_query=rewritten_query,
            hints=hints
        )
        return {"answer": result.answer}




class DSPyHotPotQAProgram(dspy.Module):
    """Complete DSPy program for MIPROv2 optimization"""
    
    def __init__(self):
        super().__init__()
        self.question_rewriter = dspy.ChainOfThought(QuestionRewriterSignature)
        self.info_extractor = dspy.ChainOfThought(InfoExtractorSignature)
        self.hint_generator = dspy.ChainOfThought(HintGeneratorSignature)
        self.answer_generator = dspy.ChainOfThought(AnswerGeneratorSignature)
        
        self.retriever = dspy.Retrieve(k=1)
    
    def forward(self, question):
        rewritten = self.question_rewriter(question=question)
        search_info = self.info_extractor(rewritten_query=rewritten.rewritten_query)
        
        # Retrieve content
        topk_passages = self.retriever(search_info.search_keywords).passages
        retrieve_content = "\n".join(topk_passages)
        
        # Generate hint + answer
        hints = self.hint_generator(
            rewritten_query=rewritten.rewritten_query,
            retrieve_content=retrieve_content
        )
        
        answer = self.answer_generator(
            rewritten_query=rewritten.rewritten_query,
            hints=hints.hints
        )
        
        return answer