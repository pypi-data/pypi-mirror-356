import os.path as osp
from dotenv import load_dotenv
import dspy
import os
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.base import BaseModule
from optimas.utils.prediction import Prediction
from optimas.arch.adapt import create_module_from_signature
from examples.datasets.hotpot_qa import dataset_engine
from examples.metrics.f1_score import f1_score
from examples.metrics.exact_match import EM


class QuestionRewriter(dspy.Signature):
    """Please rephrase the following trivia question to enhance its clarity while maintaining the original intent:"""
    question: str = dspy.InputField(
        prefix="Query: ",
        desc="The original query",
    )
    rewritten_query: str = dspy.OutputField(
        prefix="Rewritten Query: ",
        desc="The rewritten query"
    )

class InfoExtractor(dspy.Signature):
    """Extract key information needed to answer the query, which will be used as search keywords to retrieve relevant contents from the Wikipedia."""
    
    rewritten_query: str = dspy.InputField(
        prefix="Query: ",
        desc="Query used to extract relevant search keywords from"
    )
    search_keywords: str = dspy.OutputField(
        prefix="Search Keywords: ",
        desc="Keywords that will be used to search for relevant information"
    )

class WikipediaRetriever(BaseModule):
    def __init__(self, k=1):
        super().__init__(
            description="Retrieve content from Wikipedia.",
            input_fields=["search_keywords"],
            output_fields=["retrieve_content"],
            config={"k": k}
        )
        
        colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
        dspy.settings.configure(rm=colbertv2_wiki17_abstracts)
        
    def forward(self, **inputs):
        search_keywords = inputs.get("search_keywords")
        if not search_keywords:
            raise ValueError("Missing required input: 'search_keywords'")
        
        topk_passages = dspy.Retrieve(k=self.config.k)(search_keywords).passages
        retrieve_content = "\n".join(topk_passages)
        return {"retrieve_content": retrieve_content}


class HintGenerator(dspy.Signature):
    """Generate useful hints for the models to answer a query better."""

    rewritten_query: str = dspy.InputField(
        prefix="Query: ",
        desc="Query that you should answer",
    )
    retrieve_content: str = dspy.InputField(
        prefix="Retrieved Information: ",
        desc="Results retrieved from Wikipedia",
    )
    hints: str = dspy.OutputField(
        prefix="Hints: ",
        desc="Useful hints about how to answer the query",
    )


class AnswerGenerator(dspy.Signature):
    """
    Generate answer for a query following the given hints. Please directly generate a short answer less than 10 words.
    """
    rewritten_query: str = dspy.InputField(
        prefix="Query: ",
        desc="Query that you should answer",
    )
    retrieve_content: str = dspy.InputField(
        prefix="Retrieved Information: ",
        desc="Results retrieved from Wikipedia",
    )
    hints: str = dspy.InputField(
        prefix="Hints: ",
        desc="Useful hints about how to answer the query",
    )
    answer: str = dspy.OutputField(prefix="Answer: ")


def pipeline_engine(*args, **kwargs):
    lm = dspy.LM(
        model='openai/gpt-4o-mini',
        api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=1024,
        temperature=1.0
    )
    dspy.settings.configure(lm=lm)

    pipeline = CompoundAgentPipeline(*args, **kwargs)

    # Register modules
    pipeline.register_modules({
        "question_rewriter": create_module_from_signature(QuestionRewriter),
        "info_extractor": create_module_from_signature(InfoExtractor),
        "wikipedia_retriever": WikipediaRetriever(), 
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

    rewriter = pipeline.modules['question_rewriter']
    inputs = {'question': trainset[0].question}
    original_sys_prompt = rewriter.dspy_prompt_system()
    print(f'{original_sys_prompt=}')

    orignal_output = rewriter(question=trainset[0].question)
    print(f'{orignal_output=}')

    dsp_output = rewriter.forward_with_prompt(custom_prompt_template=original_sys_prompt, question=trainset[0].question)
    print(f'{dsp_output=}')

    ppl_output = pipeline._run_subpipeline_nonstatic('question_rewriter', 'question_rewriter', question=trainset[0].question)
    context = pipeline._extract_context_from_traj(ppl_output.traj)
    final_outputs = {
        key: context[key] for key in pipeline.final_output_fields if key in context
    }
    ppl_res = Prediction(**final_outputs, traj=ppl_output.traj)
    print(f'{ppl_res=}')
    
    pred = pipeline(question=trainset[0].question)
    metric = pipeline.evaluate(trainset[0], pred)
    print(pred)
    print(metric)

    # -------- Test Variable Loading
    print("variable: ", pipeline.modules["question_rewriter"].variable)
    pipeline.modules["question_rewriter"].update("dummy variable")
    print("new variable: ", pipeline.modules["question_rewriter"].variable)
    
    import pdb; pdb.set_trace()

    scores = pipeline.evaluate_multiple(testset)
    avg_score = sum(scores) / len(scores)
    print(avg_score) 


