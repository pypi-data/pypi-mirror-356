import os
import dspy
import os.path as osp
from dotenv import load_dotenv
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.base import BaseModule
from optimas.arch.adapt import create_module_from_signature
from examples.datasets.hotpot_qa import dataset_engine
from examples.metrics.f1_score import f1_score
from examples.metrics.exact_match import EM


class QuestionRewriter(dspy.Signature):
    """Rephrase the question."""
    question: str = dspy.InputField(
        prefix="Query: "
    )
    rewritten_query: str = dspy.OutputField(
        prefix="Rewritten Query: "
    )

class InfoExtractor(dspy.Signature):
    """Extract keywords from the query to retrieve relevant content."""
    
    rewritten_query: str = dspy.InputField(
        prefix="Query: "
    )
    search_keywords: str = dspy.OutputField(
        prefix="Search Keywords: "
    )


class WikipediaRetriever(BaseModule):
    def __init__(self, k=1, variable_search_space=[1, 5, 10, 25]):
        super().__init__(
            description="Retrieve content from Wikipedia.",
            input_fields=["search_keywords"],
            output_fields=["retrieve_content"],
            variable={"k": k},
            variable_search_space=variable_search_space
        )
        colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
        dspy.settings.configure(rm=colbertv2_wiki17_abstracts)
        
    def forward(self, **inputs):
        search_keywords = inputs.get("search_keywords")
        if not search_keywords:
            raise ValueError("Missing required input: 'search_keywords'")
        
        topk_passages = dspy.Retrieve(k=self.variable["k"])(search_keywords).passages
        retrieve_content = "\n".join(topk_passages)
        return {"retrieve_content": retrieve_content}


class HintGenerator(dspy.Signature):
    """Generate useful hints to answer the query."""

    rewritten_query: str = dspy.InputField(
        prefix="Query: "
    )
    retrieve_content: str = dspy.InputField(
        prefix="Retrieved Information: "
    )
    hints: str = dspy.OutputField(
        prefix="Hints: "
    )


class AnswerGenerator(dspy.Signature):
    """Given some hints, directly answer the query with a short answer for the query."""
    rewritten_query: str = dspy.InputField(
        prefix="Query: "
    )
    hints: str = dspy.InputField(
        prefix="Hints: "
    )
    answer: str = dspy.OutputField(prefix="Short Answer: ")


def pipeline_engine(*args, **kwargs):
    lm = dspy.LM(
        model='openai/gpt-4o-mini',
        max_tokens=1024,
        temperature=0.6
    )
    dspy.settings.configure(lm=lm)

    pipeline = CompoundAgentPipeline(*args, **kwargs)

    # Register modules
    pipeline.register_modules({
        "question_rewriter": create_module_from_signature(QuestionRewriter),
        "info_extractor": create_module_from_signature(InfoExtractor),
        "wikipedia_retriever": WikipediaRetriever(k=1, variable_search_space={"k": [1, 5, 10, 25]}), 
        "hint_generator": create_module_from_signature(HintGenerator),
        "answer_generator": create_module_from_signature(AnswerGenerator),
    })

    # Construct pipeline
    pipeline.construct_pipeline(
        module_order=[
            "question_rewriter", 
            "info_extractor", 
            "wikipedia_retriever", 
            "hint_generator", 
            "answer_generator"
            ],
        final_output_fields=["answer"], 
        ground_fields=["gd_answer"], 
        eval_func=f1_score
    )
    return pipeline
    

if __name__ == "__main__":
    
    trainset, valset, testset = dataset_engine()
    dotenv_path = osp.expanduser('/dfs/project/kgrlm/common/.env')
    load_dotenv(dotenv_path)

    pipeline = pipeline_engine()
    print('state_dict', pipeline.state_dict())

    # pred = pipeline(question=trainset[0].question)
    # print('question', question)
    # print('pred', pred)
    # print('eval', pipeline.evaluate(trainset[0], pred))
    # print(pipeline.modules['question_rewriter'].dspy_prompt(question=trainset[0].question))
    
    if True:
        with pipeline.context({
                'wikipedia_retriever': {'randomize_search_variable': True}, # 'variable': {'k': 1}, 
                'question_rewriter': {'model': 'openai/gpt-4o-mini', 'max_tokens': 1024},
            }):
            scores = pipeline.evaluate_multiple(testset)
            print(sum(scores) / len(scores))
    else:
        with pipeline.modules['wikipedia_retriever'].context(variable={"k": 50}):
            with pipeline.modules['question_rewriter'].context(model="openai/gpt-4o-mini", max_tokens=1024):
                scores = pipeline.evaluate_multiple(testset)
                print(sum(scores) / len(scores))

    # -------- Test Variable Loading
    print("variable: ", pipeline.modules["question_rewriter"].variable)
    pipeline.modules["question_rewriter"].update("dummy variable")
    print("new variable: ", pipeline.modules["question_rewriter"].variable)



