"""
textgrad_amazon.py
This script is used to optimize the instruction of the NextItemDecider module using TextGrad.
"""

import os
import os.path as osp
import json
import re
from typing import Dict, Any, List
from dataclasses import dataclass, field
import torch
import dspy
from dotenv import load_dotenv
from transformers import HfArgumentParser


import textgrad as tg
from textgrad.engine.openai import ChatOpenAI
from textgrad import Variable, TextualGradientDescent

from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.base import BaseModule
from optimas.utils.logging import setup_logger
from optimas.utils.example import Example

# Import original modules directly
from examples.pipelines.amazon_product.amazon_next_item_selection_local import (
    SessionAnalyzerModule,
    CandidateProfilerModule,
    accuracy,
    post_http_request,
    get_response,
    BASE_MODEL_ID,
)

from optimas.reward.eval import eval_pipeline
from optimas.reward.dataset import RewardDataset
from examples.pipelines import registered_pipeline
from examples.datasets import registered_dataset

class NextItemDeciderTextGrad(BaseModule):
    """TextGrad-enabled NextItemDecider with optimizable prompt."""
    
    def __init__(self, model="openai/gpt-4o-mini", api_key=None):
        # Only the instruction part is optimizable, keeping format consistent
        self.instruction = Variable(
            value="Pick the next item based on summary + feedback.",
            role_description="instruction part of prompt",
            requires_grad=True,
        )
        
        # The fixed format parts (not optimized)
        self.format_template = "\n\nContext: {context}\n\nFeedback: {feedback}\n\nAnswer: "
        
        # Setup DSPy for actual predictions
        self.lm = dspy.LM(
            model=model,
            api_key=api_key,
            max_tokens=10,
            temperature=0.0,
        )
        
        super().__init__(
            description="Pick the next item based on summary + feedback",
            input_fields=["context", "feedback"],
            output_fields=["answer"],
            variable='textgrad'
        )
    
    def forward(self, **inputs):
        context = inputs["context"]
        feedback = inputs["feedback"]
        
        # Combine instruction and format
        prompt_content = self.instruction.get_value() + self.format_template.format(
            context=context,
            feedback=feedback
        )
        
        # context_var = Variable(
        #     value=context,
        #     role_description="session context",
        #     requires_grad=False,
        # )
        
        # feedback_var = Variable(
        #     value=feedback,
        #     role_description="candidate feedback",
        #     requires_grad=False,
        # )
        
        # prompt_var = Variable(
        #     value=prompt_content,
        #     role_description="formatted decision prompt",
        #     requires_grad=False,
        #     predecessors=[self.prompt_template, context_var, feedback_var]
        # )
        
        # Get response using DSPy
        with dspy.context(lm=self.lm):
            response = self.lm(prompt_content)
        
        # Extract just the answer, MAY need to extract just the index of chosen item
        # print(response)
        if isinstance(response, list):
            answer = response[0].strip() if response else ""
        else:
            answer = response.strip()
        
        # Create output variable for TextGrad
        output_var = Variable(
            value=answer,
            role_description="next item prediction",
            requires_grad=True,
            predecessors=[self.instruction]
        )
        
        return {"answer": answer, "_textgrad_output": output_var}


@dataclass
class ExecutionConfig:
    """Configuration for execution mode and model settings."""
    use_gpu: bool = False
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"
    tensor_parallel_size: int = 1
    gpu_memory_utilization: float = 0.9
    device: str = "cuda"  # set to "cpu" if use_gpu is False
    
    def __post_init__(self):
        if not self.use_gpu:
            self.device = "cpu"
            self.gpu_memory_utilization = 0.0
            self.tensor_parallel_size = 1

def textgrad_pipeline_engine(*args, mode="train", **kwargs):
    """Create pipeline with TextGrad optimization for NextItemDecider only.
    
    Args:
        mode: Either "train" or "test". In train mode, we use intermediate steps (context, feedback).
              In test mode, we use original sequence and choices.
    """
    dotenv_path = os.getenv("DOTENV_PATH", os.path.expanduser("~/.env"))
    load_dotenv(dotenv_path)
    
    # Set up engines following TextGrad pattern
    llm_api_eval = tg.get_engine(engine_name="gpt-4o-mini")  # For optimization feedback
    # llm_api_test = tg.get_engine(engine_name=model_name)  # For actual predictions
    tg.set_backward_engine(llm_api_eval, override=True)
    
    pipeline = CompoundAgentPipeline(*args, **kwargs)
    
    # if mode == "train":
    #     # For training: Use TextGrad-enabled NextItemDecider with intermediate steps
    #     next_item_decider = NextItemDeciderTextGrad(
    #         model=model_name,
    #         api_key=os.getenv("OPENAI_API_KEY")
    #     )
        
    #     # Register modules for training
    #     pipeline.register_modules({
    #         "next_item_decider": next_item_decider,
    #     })
        
    #     # Construct pipeline for training
    #     pipeline.construct_pipeline(
    #         module_order=["next_item_decider"],
    #         final_output_fields=["answer"],
    #         ground_fields=["gd_answer"],
    #         eval_func=accuracy,
    #     )
        
    #     # Store reference to the TextGrad module
    #     pipeline.textgrad_module = next_item_decider
        
    # else:  # mode == "test"
    #     # For testing: Use full pipeline with original sequence and choices
    #     session_analyzer = SessionAnalyzerModule(engine=llm_api_test)
    #     candidate_profiler = CandidateProfilerModule(engine=llm_api_test)
    #     next_item_decider = NextItemDeciderTextGrad(
    #         model=model_name,
    #         api_key=os.getenv("OPENAI_API_KEY")
    #     )
        
    #     # Register all modules for testing
    #     pipeline.register_modules({
    #         "session_analyzer": session_analyzer,
    #         "candidate_profiler": candidate_profiler,
    #         "next_item_decider": next_item_decider,
    #     })
        
    #     # Construct full pipeline for testing
    #     pipeline.construct_pipeline(
    #         module_order=[
    #             "session_analyzer",
    #             "candidate_profiler",
    #             "next_item_decider",
    #         ],
    #         final_output_fields=["answer"],
    #         ground_fields=["gd_answer"],
    #         eval_func=accuracy,
    #     )
    
    # JUST for training: Use TextGrad-enabled NextItemDecider with intermediate steps
    next_item_decider = NextItemDeciderTextGrad(
        model="gpt-4o-mini",  # Use gpt-4o-mini for optimization
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Register modules for training
    pipeline.register_modules({
        "next_item_decider": next_item_decider,
    })
    
    # Construct pipeline for training
    pipeline.construct_pipeline(
        module_order=["next_item_decider"],
        final_output_fields=["answer"],
        ground_fields=["gd_answer"],
        eval_func=accuracy,
    )
    # Store reference to the TextGrad module
    pipeline.textgrad_module = next_item_decider
    
    return pipeline


def optimize_with_textgrad(pipeline, trainset, num_iterations=3, batch_size=8):
    """Optimize ONLY the NextItemDecider instruction prompt using TextGrad."""
    logger = setup_logger(__name__)
    
    # Get the TextGrad-enabled NextItemDecider
    next_item_decider = pipeline.textgrad_module
    
    # Create TextGrad optimizer with the evaluation engine
    optimizer = TextualGradientDescent(
        engine=tg.get_engine(engine_name="gpt-4o-mini"),  # gpt-4o-mini for optimization only
        parameters=[next_item_decider.instruction]
    )
    
    for iteration in range(num_iterations):
        logger.info(f"Starting TextGrad iteration {iteration + 1}/{num_iterations}")
        
        batch = trainset[:batch_size] if len(trainset) > batch_size else trainset
        
        # Zero gradients at start of iteration
        optimizer.zero_grad()
        
        total_loss = 0.0
        for idx, example in enumerate(batch):
            # Forward pass through next item decider only
            result = next_item_decider(
                context=example.context,
                feedback=example.feedback
            )
            
            textgrad_output = result.get("_textgrad_output")
            if textgrad_output is None:
                continue
            
            pred_answer = result["answer"]
            correct = accuracy(pred_answer, example.gd_answer)  # or textgrad_accuracy
            
            if correct < 1.0:  # Wrong answer
                # Tunable, keep succinct loss feedback
                loss_text = f"""
                The model predicted: {pred_answer}
                The correct answer was: {example.gd_answer}

                Please improve the instruction to help the model select the correct item.
                """
                
                # Create loss variable
                loss = Variable(
                    value=loss_text,
                    role_description="task loss",
                    requires_grad=True,
                    predecessors=[textgrad_output]
                )
                
                # Backward pass (no engine parameter since we set it globally)
                loss.backward()
                total_loss += 1.0
            else:
                total_loss += 0.0
        
        # Step the optimizer to update the instruction
        optimizer.step()
        
        avg_loss = total_loss / len(batch)
        logger.info(f"Iteration {iteration + 1} average loss: {avg_loss:.4f}")
        logger.info(f"Current instruction: {next_item_decider.instruction.get_value()}")
    
    return pipeline


def extract_number(text):
    """Extract a number from text, handling various formats."""
    # Try to find a standalone number
    number_match = re.search(r'\b\d+\b', text)
    if number_match:
        return number_match.group(0)
    
    # Try to find any number
    number_match = re.search(r'\d+', text)
    if number_match:
        return number_match.group(0)
    
    # If no number found, return the original text
    return text

# help it out if it's toooo bad
def textgrad_accuracy(answer, gd_answer):
    """Enhanced accuracy metric that handles different response formats."""
    # Extract numbers from both answers
    answer_num = extract_number(str(answer))
    gd_answer_num = extract_number(str(gd_answer))
    
    # Compare the extracted numbers
    return 1.0 if answer_num == gd_answer_num else 0.0


# --------------------------------------------------------------------------- #
# Main Script                                                                 #
# --------------------------------------------------------------------------- #
@dataclass
class ScriptArgs:
    # Core arguments
    run_name: str = "default"
    dataset: str = "amazon"
    pipeline_name: str = "amazon_textgrad_pipeline"
    output_dir: str = "./outputs"
    
    # TextGrad specific
    num_iterations: int = 3
    batch_size: int = 8
    
    # Evaluation
    num_repeat: int = 3
    
    # Environment
    dotenv_path: str = "~/.env"


def main():
    # Parse arguments
    parser = HfArgumentParser(ScriptArgs)
    args = parser.parse_args_into_dataclasses()[0]
    
    # Set environment
    os.environ["DOTENV_PATH"] = os.path.expanduser(args.dotenv_path)
    
    # Setup output directory
    args.output_dir = osp.join(args.output_dir, args.dataset, args.pipeline_name, args.run_name)
    os.makedirs(args.output_dir, exist_ok=True)
    
    logger = setup_logger(__name__, log_file=osp.join(args.output_dir, "output.log"))
    
    # Load dataset from load_nextitemdecider_dataset.py
    logger.info("Using existing dataset from load_nextitemdecider_dataset.py...")
    pipeline_name = 'amazon_next_item_selection_local_pipeline'
    hf_repo_or_local_dir = f'snap-stanford/{pipeline_name}-preference_scorer'
    pipeline = registered_pipeline[pipeline_name]()
    # This accesses a dataset_engine that is downloaded locally from hugging face
    # Can replace with method that relies on examples/datasets/session_based_next_item_selection_dataset.py
    trainset, valset, testset = registered_dataset["amazon_session_local_dataset"]()
    
    # Create reward dataset for training
    reward_dataset = RewardDataset(
        hf_repo_or_local_dir, pipeline,
        original_trainset=trainset + valset + testset  # or just + testset or + valset
    ).to_inputs_only_dataset()
    
    # Get next item decider specific dataset
    next_item_decider_ds = reward_dataset["next_item_decider"]["input"]
    trainset = [Example(next_item_decider_ds[i]).with_inputs(*pipeline.modules["next_item_decider"].input_fields)
        for i in range(len(next_item_decider_ds))]
    
    # # Format testset use original sequence and choices
    # testset = [
    #     Example({
    #         "sequence": example.sequence,
    #         "choices": example.choices,
    #         "gd_answer": example.gd_answer
    #     }).with_inputs("sequence", "choices")  # use original input fields for testing
    #     for example in testset
    # ]
    
    # logger.info(f"Loaded {len(trainset)} training examples and {len(testset)} test examples")
    logger.info(f"Loaded {len(trainset)} training examples for instruction optimization.")
    
    # Create training pipeline
    train_pipeline = textgrad_pipeline_engine(log_dir=args.output_dir, mode="train")
    
    # Print the original instruction before optimization
    original_instruction = train_pipeline.textgrad_module.instruction.get_value()
    logger.info(f"Original instruction: \"{original_instruction}\"")
    
    # Optimize with TextGrad
    logger.info("Starting TextGrad optimization...")
    optimized_pipeline = optimize_with_textgrad(
        pipeline=train_pipeline,
        trainset=trainset,
        num_iterations=args.num_iterations,
        batch_size=args.batch_size
    )
    
    # Save optimized instruction
    optimized_instruction = optimized_pipeline.textgrad_module.instruction.get_value()
    prompt_state = {
        "next_item_decider": {
            "original_instruction": original_instruction,
            "optimized_instruction": optimized_instruction,
            "optimization_details": {
                "num_iterations": args.num_iterations,
                "batch_size": args.batch_size,
                "num_training_examples": len(trainset)
            }
        }
    }
    
    # Save to JSON file
    with open(osp.join(args.output_dir, "optimized_prompts.json"), "w") as f:
        json.dump(prompt_state, f, indent=2)
    
    # Also save a simple text file with just the instructions
    with open(osp.join(args.output_dir, "optimized_instruction.txt"), "w") as f:
        f.write(f"Original instruction:\n{original_instruction}\n\n")
        f.write(f"Optimized instruction:\n{optimized_instruction}\n")
    
    # # Evaluate on test set
    # logger.info("Evaluating optimized pipeline on test set...")
    # scores = test_pipeline.evaluate_multiple(testset)
    # avg_score = sum(scores) / len(scores)
    
    # Print optimization comparison
    logger.info("\nTextGrad Optimization Results:")
    logger.info(f"Original instruction: \"{original_instruction}\"")
    logger.info(f"Optimized instruction: \"{optimized_instruction}\"")
    # logger.info(f"Final accuracy: {metrics['accuracy']:.4f}")
    
    # # Save evaluation results
    # eval_results = {
    #     "metrics": metrics,
    #     "test_scores": scores,
    #     "average_score": avg_score
    # }
    
    logger.info(f"\nInstructions saved to:")
    logger.info(f"- {osp.join(args.output_dir, 'optimized_prompts.json')}")
    logger.info(f"- {osp.join(args.output_dir, 'optimized_instruction.txt')}")
    logger.info("\nNote: Local model evaluation skipped. Use the optimized instruction with a GPU setup for evaluation.")


if __name__ == "__main__":
    main()
