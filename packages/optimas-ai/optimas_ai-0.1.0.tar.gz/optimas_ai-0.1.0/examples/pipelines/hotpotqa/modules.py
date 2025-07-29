import os, random, os.path as osp
import dspy
import textgrad as tg
from textgrad import Variable, BlackboxLLM
from optimas.arch.base import BaseModule

MODELS_LIST = [
    "gpt-4o-mini",  
    "claude-3-haiku-20240307", 
]

SYS_PROMPT = """You are a helpful question‑answering assistant."""
SYS_VAR    = Variable(SYS_PROMPT, requires_grad=False,
                      role_description="system prompt")

# could/should tune the prompts for each module
class TextGradQuestionRewriter(BaseModule):
    """Rephrase a user question for clarity and retrieval."""
    def __init__(self, model="gpt-4o-mini", max_tokens=1024, temperature=0.6):
        self.models_list = MODELS_LIST
        self.default_model = model
        self.prompt = Variable(
            "Rephrase the question",
            requires_grad=True,
            role_description="rewriter instruction"
        )
        super().__init__(
            description="Question rewriter (TextGrad)",
            input_fields=["question"],
            output_fields=["rewritten_query", "rewriter_model"],
            variable=self.prompt.value,
            config={"model": model, "max_tokens": max_tokens, "temperature": temperature}
        )

    @property
    def optimizable(self):
        return True

    # forward helpers for training
    def rewrite(self, question: str) -> Variable:
        chosen = random.choice(self.models_list)
        user_prompt = f"""{self.prompt.value}\n\nQuery: \"{question}\"\n\nRewritten Query:"""
        x = Variable(user_prompt, requires_grad=True, role_description="rewriter input")
        return BlackboxLLM(chosen, SYS_VAR)(x)

    # pipeline run
    def forward(self, **inputs):
        q = inputs["question"]
        chosen = self.config.get("model", self.default_model)
        user_prompt = f"""{self.variable}\n\nQuery: \"{q}\"\n\nRewritten Query:"""
        x = Variable(user_prompt, requires_grad=True, role_description="rewriter input")
        resp = BlackboxLLM(chosen, SYS_VAR)(x)
        return {"rewritten_query": resp.value, "rewriter_model": chosen}


class TextGradInfoExtractor(BaseModule):
    """Extract search keywords from rewritten query."""
    def __init__(self, model="gpt-4o-mini", max_tokens=1024, temperature=0.6):
        self.models_list = MODELS_LIST
        self.default_model = model
        self.prompt = Variable(
            "Extract keywords from the query to retrieve relevant content.",
            requires_grad=True,
            role_description="extractor instruction"
        )
        super().__init__(
            description="Info extractor (TextGrad)",
            input_fields=["rewritten_query"],
            output_fields=["search_keywords", "extractor_model"],
            variable=self.prompt.value,
            config={"model": model, "max_tokens": max_tokens, "temperature": temperature}
        )

    @property
    def optimizable(self):
        return True

    def extract(self, rewritten_query: str) -> Variable:
        chosen = random.choice(self.models_list)
        user_prompt = f"""{self.prompt.value}\n\nQuery: \"{rewritten_query}\"\n\nSearch Keywords:"""
        x = Variable(user_prompt, requires_grad=True, role_description="extractor input")
        return BlackboxLLM(chosen, SYS_VAR)(x)

    def forward(self, **inputs):
        rq = inputs["rewritten_query"]
        chosen = self.config.get("model", self.default_model)
        user_prompt = f"""{self.variable}\n\nQuery: \"{rq}\"\n\nSearch Keywords:"""
        x = Variable(user_prompt, requires_grad=True, role_description="extractor input")
        resp = BlackboxLLM(chosen, SYS_VAR)(x)
        return {"search_keywords": resp.value, "extractor_model": chosen}


class WikipediaRetriever(BaseModule):
    """Retrieve top‑k passages from ColBERT v2 Wiki17."""
    def __init__(self, k=5, search_space=(1, 5, 10, 20)):
        super().__init__(
            description="Wikipedia ColBERT retriever",
            input_fields=["search_keywords"],
            output_fields=["retrieve_content"],
            variable={"k": k},
            variable_search_space={"k": list(search_space)}
        )
        colbert = dspy.ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
        dspy.settings.configure(rm=colbert)

    @property
    def optimizable(self):
        return True  # tune k via variable‑search

    def forward(self, **inputs):
        kws = inputs["search_keywords"]
        k_val = self.variable.get("k", 5)
        passages = dspy.Retrieve(k=k_val)(kws).passages
        return {"retrieve_content": "\n".join(passages)}


class TextGradHintGenerator(BaseModule):
    """Generate hints given query + retrieved content."""
    def __init__(self, model="gpt-4o-mini", max_tokens=1024, temperature=0.6):
        self.models_list = MODELS_LIST
        self.default_model = model
        self.prompt = Variable(
            "Generate useful hints to answer the query.",
            requires_grad=True,
            role_description="hint instruction"
        )
        super().__init__(
            description="Hint generator (TextGrad)",
            input_fields=["rewritten_query", "retrieve_content"],
            output_fields=["hints", "hint_model"],
            variable=self.prompt.value,
            config={"model": model, "max_tokens": max_tokens, "temperature": temperature}
        )

    @property
    def optimizable(self):
        return True

    def generate_hints(self, rq: str, content: str) -> Variable:
        chosen = random.choice(self.models_list)
        user_prompt = f"""{self.prompt.value}\n\nQuery: \"{rq}\"\n\nRetrieved Information:\n{content}\n\nHints:"""
        x = Variable(user_prompt, requires_grad=True, role_description="hint input")
        return BlackboxLLM(chosen, SYS_VAR)(x)

    def forward(self, **inputs):
        rq, content = inputs["rewritten_query"], inputs["retrieve_content"]
        chosen = self.config.get("model", self.default_model)
        user_prompt = f"""{self.variable}\n\nQuery: \"{rq}\"\n\nRetrieved Information:\n{content}\n\nHints:"""
        x = Variable(user_prompt, requires_grad=True, role_description="hint input")
        resp = BlackboxLLM(chosen, SYS_VAR)(x)
        return {"hints": resp.value, "hint_model": chosen}


class TextGradAnswerGenerator(BaseModule):
    """Produce short answer (<10 words) from hints."""
    def __init__(self, model="gpt-4o-mini", max_tokens=512, temperature=0.6):
        self.models_list = MODELS_LIST
        self.default_model = model
        self.prompt = Variable(
            "Given some hints, directly answer the query with a short answer for the query.",
            requires_grad=True,
            role_description="answer instruction"
        )
        super().__init__(
            description="Answer generator (TextGrad)",
            input_fields=["rewritten_query", "hints"],
            output_fields=["answer", "answer_model"],
            variable=self.prompt.value,
            config={"model": model, "max_tokens": max_tokens, "temperature": temperature}
        )

    @property
    def optimizable(self):
        return True

    def generate_answer(self, rq: str, hints: str) -> Variable:
        chosen = random.choice(self.models_list)
        user_prompt = f"""{self.prompt.value}\n\nQuery: \"{rq}\"\n\nHints:\n{hints}\n\nAnswer:"""
        x = Variable(user_prompt, requires_grad=True, role_description="answer input")
        return BlackboxLLM(chosen, SYS_VAR)(x)

    def forward(self, **inputs):
        rq, hints = inputs["rewritten_query"], inputs["hints"]
        chosen = self.config.get("model", self.default_model)
        user_prompt = f"""{self.variable}\n\nQuery: \"{rq}\"\n\nHints:\n{hints}\n\nAnswer:"""
        x = Variable(user_prompt, requires_grad=True, role_description="answer input")
        resp = BlackboxLLM(chosen, SYS_VAR)(x)
        return {"answer": resp.value, "answer_model": chosen}