import os.path as osp
import dspy
from dotenv import load_dotenv
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.adapt import create_module_from_signature
from examples.metrics.f1_score import f1_score


class HintGenerator(dspy.Signature):
    """Generate useful hints for the models to answer a query better."""

    question: str = dspy.InputField(
        prefix="Query: ",
        desc="Query that you should answer",
    )
    hints: str = dspy.OutputField(
        prefix="Hints: ",
        desc="Useful hints about how to answer the query",
    )


class AnswerGenerator(dspy.Signature):
    """
    Generate answer for a query following the given hints. 
    """
    # Please directly generate a short answer less than 10 words.
    question: str = dspy.InputField(
        prefix="Query: ",
        desc="Query that you should answer",
    )
    hints: str = dspy.InputField(
        prefix="Hints: ",
        desc="Useful hints about how to answer the query",
    )
    answer: str = dspy.OutputField(prefix="Answer: ")


def pipeline_engine(*args, **kwargs):
    pipeline = CompoundAgentPipeline(*args, **kwargs)

    # Register modules using create_module_from_signature and custom BaseModule
    pipeline.register_modules({
        "hint_generator": create_module_from_signature(HintGenerator),
        "answer_generator": create_module_from_signature(AnswerGenerator),
    })

    # Construct pipeline
    pipeline.construct_pipeline(
        module_order=["hint_generator", "answer_generator"],
        final_output_fields=["answer"], 
        ground_fields=["gd_answer"],
        eval_func=f1_score
    )
    return pipeline


# ------------------------------------------------------------------------
#                           Baseline Pipeline
# ------------------------------------------------------------------------
class SingleAnswerGenerator(dspy.Signature):
    """
    Generate answer for a query. Please directly generate a short answer less than 10 words.
    """
    question: str = dspy.InputField(
        prefix="Query: ",
        desc="Query that you should answer",
    )
    answer: str = dspy.OutputField(prefix="Answer: ")


def single_agent_pipeline_engine(*args, **kwargs):
    pipeline = CompoundAgentPipeline(*args, **kwargs)

    # Register modules using create_module_from_signature and custom BaseModule
    pipeline.register_modules({
        "answer_generator": create_module_from_signature(SingleAnswerGenerator),
    })

    # Construct pipeline
    pipeline.construct_pipeline(
        module_order=["answer_generator"],
        final_output_fields=["answer"], 
        ground_fields=["gd_answer"],
        eval_func=f1_score
    )
    return pipeline


if __name__ == "__main__":
    import os
    from examples.datasets.hotpot_qa import dataset_engine
    
    trainset, valset, testset = dataset_engine()
    dotenv_path = osp.expanduser('/dfs/project/kgrlm/common/.env')
    load_dotenv(dotenv_path)

    lm = dspy.OpenAI(
        model='gpt-4o-mini',
        api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=1024,
        temperature=1.0
    )
    dspy.settings.configure(lm=lm)
    pipeline = pipeline_engine()

    pred = pipeline(question=trainset[0].question)
    metric = pipeline.evaluate(trainset[0], pred)

    print(pred)
    print(metric)

    scores = pipeline.evaluate_multiple(testset)
    avg_score = sum(scores) / len(scores)

    print(avg_score) 
    import pdb; pdb.set_trace()


