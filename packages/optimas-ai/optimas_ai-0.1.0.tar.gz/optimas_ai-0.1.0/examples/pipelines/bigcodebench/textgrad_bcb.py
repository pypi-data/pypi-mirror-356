"""
TextGrad optimization for BigCodeBench pipeline.

Focusing on optimizing the prompts for CodeGenerator, UnitTestGenerator, and FinalCodeGenerator modules.
"""

import os
import os.path as osp
import json
import re
import torch
import dspy
from typing import List, Dict, Any
import numpy as np
from transformers import AutoTokenizer
from tqdm import tqdm
from dotenv import load_dotenv
import argparse

import textgrad as tg
from textgrad import Variable, TextualGradientDescent
from textgrad.loss import TextLoss

from examples.metrics.pass_rate import pass_rate
from examples.datasets.bigcodebench import dataset_engine

from optimas.arch.base import BaseModule
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.adapt import create_module_from_signature
from optimas.utils.api import get_llm_output
from optimas.utils.logging import setup_logger

from bigcodebench.data import get_bigcodebench, write_jsonl
from bigcodebench.sanitize import sanitize


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CKPT_DIR = os.path.join(SCRIPT_DIR, "checkpoints", "train_size=500")
if not os.path.exists(CKPT_DIR):
    os.makedirs(CKPT_DIR)

UNIT_TEST_PROMPT = '''
**Role**: You are a software programmer.
**Task**: As a programmer, you are required to complete the function. Use a Chain-of-Thought approach to break
down the problem, create pseudocode, and then write the code in Python language. Ensure that your code is
efficient, readable, and well-commented.

For example:
**Input Code Snippet**:
```python
from typing import List
def has_close_elements(numbers: List[float], threshold: float) -> bool:
 """
 Check if in given list of numbers, are any two numbers closer to each other than given threshold.
 >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
 False
 >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
 True
 """
 # TODO: Implement the logic to determine if any two numbers are closer than the threshold
 pass
# Add your code here to complete the function
```

**Instructions**:
1. **Understand and Clarify**: Make sure you understand the task.
2. **Algorithm/Method Selection**: Decide on the most efficient way.
3. **Pseudocode Creation**: Write down the steps you will follow in pseudocode.
4. **Code Generation**: Translate your pseudocode into executable Python code.
'''


def make_raw_chat_prompt(
    task_prompt: str,
    split: str,
    instruction_prefix: str,
) -> str:
    # directly return prompt if it does not have a tokenizer.chat_template

    assert instruction_prefix is not None, "Instruction prefix is required!"

    if split == "complete":
        task_prompt = f"""\
{instruction_prefix}
```
{task_prompt.strip()}
```
"""
    else:
        task_prompt = f"""\
{instruction_prefix}
{task_prompt.strip()}
"""
    return task_prompt


class TextGradCodeGenerator(BaseModule):
    """Generate a runnable Python solution for a given coding problem."""

    def __init__(self, model='claude-3-haiku-20240307', max_tokens=1572, temperature=0.6):
        # Initialize the instruction as a TextGrad Variable
        self.instruction = Variable(
            value="Provide a self-contained Python solution:",
            role_description="code generation instruction",
            requires_grad=True
        )
        
        super().__init__(
            description="Generate Python solution for coding problem.",
            input_fields=["question"],
            output_fields=["initial_code"],
            variable=self.instruction.value,
            config={"model": model, 
                    "max_tokens": max_tokens, 
                    "temperature": temperature
            },
        )
    
    def forward(self, **inputs):
        """
        Generate a runnable Python solution for a given coding problem.

        Args:
            question (str): A clear and concise description of the coding problem.
            **inputs: May include model, temperature, max_tokens set by pipeline

        Returns:
            dict: Contains initial_code and TextGrad output variable
        """
        prompt = make_raw_chat_prompt(
            inputs["question"], 
            instruction_prefix=self.instruction.get_value(), 
            split="complete"
        )

        initial_code = get_llm_output(
            message=prompt,
            model=self.config.model,
            max_new_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
        )

        # Sanitize
        if 'entry_point' in inputs:
            entry_point = inputs['entry_point']
        else:
            entry_point = 'task_func'
        initial_code = sanitize(initial_code, entry_point)

        # Create output variable for TextGrad
        output_var = Variable(
            value=initial_code,
            role_description="generated code solution",
            requires_grad=True,
            predecessors=[self.instruction]
        )

        return {"initial_code": initial_code, "_textgrad_output": output_var}


class TextGradUnitTestGenerator(BaseModule):
    """Generate a set of Python unit tests to validate the correctness of the generated code."""

    def __init__(self, model='claude-3-haiku-20240307', max_tokens=1572, temperature=0.6):

       
        base_prompt = UNIT_TEST_PROMPT
        
        # Initialize the instruction as a TextGrad Variable
        self.instruction = Variable(
            # value=base_prompt,
            value="Write a TestCases class with 3 tests for task_func.",
            role_description="unit test generation instruction",
            requires_grad=True
        )
        
        super().__init__(
            description="Generate a set of Python unit tests to validate the correctness of the generated code.",
            input_fields=["question"],
            output_fields=["additional_unit_tests"],
            variable=self.instruction.value,
            config={
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        )

    def forward(self, question):
        """
        Generate a set of Python unit tests to validate the correctness of the generated code.
        
        Args:
            question (str): The coding problem description
            
        Returns:
            dict: Contains additional_unit_tests and TextGrad output variable
        """
        prompt = make_raw_chat_prompt(
            question,
            instruction_prefix=self.instruction.get_value(),
            split="complete"
        )
        
        unit_tests = get_llm_output(
            message=prompt,
            model=self.config.model,
            max_new_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
        )
        
        # regex code block if present
        match = re.search(r"```python\s*(.*?)\s*```", unit_tests, re.DOTALL)
        if match:
            unit_tests = match.group(1).strip("\n").strip()
        else:
            unit_tests = ""
        
        # Create output variable for TextGrad
        output_var = Variable(
            value=unit_tests,
            role_description="generated unit tests",
            requires_grad=True,
            predecessors=[self.instruction]
        )

        return {"additional_unit_tests": unit_tests, "_textgrad_output": output_var}


class Executor(BaseModule):
    """Execute the generated code against the generated unit tests and return the results."""

    def __init__(self):
        super().__init__(
            description="Execute the generated Python code using the provided unit tests.",
            input_fields=["initial_code", "additional_unit_tests"],
            output_fields=["execution_result"],
        )

    def forward(self, initial_code, additional_unit_tests):
        result = pass_rate(initial_code, additional_unit_tests, entry_point="task_func")
        return {"execution_result": result}


class TextGradFinalCodeGenerator(dspy.Signature):
    """Refine code based on test results."""
    
    question = dspy.InputField(desc="The coding problem.")
    initial_code = dspy.InputField(desc="Initial code solution.")
    additional_unit_tests = dspy.InputField(desc="Unit tests for evaluation.")
    execution_result = dspy.InputField(desc="Test execution results, including errors.")
    code = dspy.OutputField(desc="Improved code solution based on test results.")


class TextGradFinalCodeGeneratorModule(BaseModule):
    """Refine code based on test results with TextGrad optimization."""
    
    def __init__(self, model='claude-3-haiku-20240307', max_tokens=1572, temperature=0.6):
        self.instruction = Variable(
            value="Refine code based on test results.",
            role_description="final code generator instruction",
            requires_grad=True
        )
        
        # Recreate DSPy signature with its instructions
        self.signature = TextGradFinalCodeGenerator
        
        super().__init__(
            description="Refine code based on test results.",
            input_fields=["question", "initial_code", "additional_unit_tests", "execution_result"],
            output_fields=["code"],
            variable=self.instruction.value,
            config={"model": model, "max_tokens": max_tokens, "temperature": temperature},
        )
    
    def forward(self, **inputs):
        """
        Refine code based on test results.
        
        Args:
            question (str): The coding problem
            initial_code (str): The initial code solution
            additional_unit_tests (str): The unit tests
            execution_result (dict): The test execution results
            
        Returns:
            dict: Contains refined code and TextGrad output variable
        """
        # Create a signature with the current instruction
        signature = self.signature.with_instructions(self.instruction.get_value())
        
        # Manually onvert config to dictionary
        config_dict = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }
        
        predictor = dspy.Predict(signature)
        
        # Formatted prompt using dspy's internal formatting
        with dspy.settings.context(lm=dspy.LM(**config_dict)):
            adapter = dspy.settings.adapter or dspy.ChatAdapter()
            
            prompt = adapter.format(
                signature,
                demos=[],
                inputs=inputs
            )
            
            prediction = predictor(**inputs)
            refined_code = prediction.code
        
        output_var = Variable(
            value=refined_code,
            role_description="refined code solution",
            requires_grad=True,
            predecessors=[self.instruction]
        )
        
        return {"code": refined_code, "_textgrad_output": output_var}


def merge_textgrad_checkpoints(code_gen_path: str, unit_test_path: str, final_code_path: str, out_path: str):
    """
    Load three JSON prompt checkpoints and merge into a single state dict .pth file.
    """
    with open(code_gen_path, 'r') as f:
        code_gen = json.load(f)
    with open(unit_test_path, 'r') as f:
        unit_test = json.load(f)
    with open(final_code_path, 'r') as f:
        final_code = json.load(f)

    combined = {
        'code_generator_instruction': code_gen['prompt'],
        'unit_test_generator_instruction': unit_test['prompt'],
        'final_code_generator_instruction': final_code['prompt']
    }
    torch.save(combined, out_path)
    print(f"Saved combined prompts to {out_path}")


def code_loss_fn(code_var: Variable, question: str, unit_tests: str, execution_result: float):
    """Loss function for evaluating code quality."""
    if execution_result > 0: 
        return 0.0 
    
    prompt = (
        f"Evaluate this Python code solution for the following problem:\n"
        f"Problem: {question}\n\n"
        f"Unit Tests:\n{unit_tests}\n\n"
        f"All tests failed. Provide concise feedback to improve the code generation instruction."
    )
    
    loss = TextLoss(Variable(prompt, 
                           requires_grad=False,
                           role_description="code evaluation"))(code_var)
    return loss


def unit_test_loss_fn(unit_test_var: Variable, question: str, code: str, execution_result: float):
    """Loss function for evaluating unit test quality."""
    if execution_result == 0: 
        prompt = (
            f"Evaluate these unit tests for the following problem:\n"
            f"Problem: {question}\n\n"
            f"Implementation:\n{code}\n\n"
            f"Issues: All tests failed, need more comprehensive testing\n\n"
            "Provide concise feedback to improve the unit test generation instruction."
        )
        
        loss = TextLoss(Variable(prompt, 
                               requires_grad=False,
                               role_description="unit test evaluation"))(unit_test_var)
        return loss
    
    return 0.0 


def final_code_loss_fn(final_code_var: Variable, question: str, initial_code: str, unit_tests: str, execution_result: float):
    """Loss function for evaluating final code refinement quality."""
    if execution_result > 0: 
        return 0.0 
    
    prompt = (
        f"Evaluate this refined Python code solution for the following problem:\n"
        f"Problem: {question}\n\n"
        f"Original Code:\n{initial_code}\n\n"
        f"Unit Tests:\n{unit_tests}\n\n"
        f"All tests failed. Provide concise feedback to improve the code refinement instruction."
    )
    
    loss = TextLoss(Variable(prompt, 
                           requires_grad=False,
                           role_description="final code evaluation"))(final_code_var)
    return loss


def pipeline_engine(*args, **kwargs):
    """Create the TextGrad-optimized BigCodeBench pipeline."""
    model = 'claude-3-haiku-20240307'
    lm = dspy.LM(
        model=model,
        max_tokens=1572,
        temperature=0.6
    )
    dspy.settings.configure(lm=lm)
    
    llm_api_eval = tg.get_engine(engine_name="gpt-4o-mini")
    tg.set_backward_engine(llm_api_eval, override=True)
    
    # patch, remove max_workers from kwargs before passing to CompoundAgentPipeline
    max_workers = kwargs.pop('max_workers', None)
    
    pipeline = CompoundAgentPipeline(*args, **kwargs)
    
    # Set max_workers after pipeline creation if provided
    if max_workers is not None:
        pipeline.max_workers = max_workers

    pipeline.register_modules(
        {
            "code_generator": TextGradCodeGenerator(model=model),
            "unit_test_generator": TextGradUnitTestGenerator(model=model),
            "executor": Executor(),
            # "final_code_generator": create_module_from_signature(TextGradFinalCodeGenerator),
            "final_code_generator": TextGradFinalCodeGeneratorModule(model=model),
        }
    )

    pipeline.construct_pipeline(
        module_order=[
            "code_generator",
            "unit_test_generator",
            "executor",
            "final_code_generator",
        ],
        final_output_fields=["code"],
        ground_fields=["unit_tests", "entry_point"],
        eval_func=pass_rate,
    )
    
    # Store references to TextGrad-enabled modules
    pipeline.textgrad_modules = {
        "code_generator": pipeline.modules["code_generator"],
        "unit_test_generator": pipeline.modules["unit_test_generator"],
        "final_code_generator": pipeline.modules["final_code_generator"]
    }
    
    merged_pth = os.path.join(CKPT_DIR, "combined_textgrad_prompts.pth")
    if os.path.exists(merged_pth):
        sd = torch.load(merged_pth, map_location="cpu")
        pipeline.modules["code_generator"].instruction.value = sd["code_generator_instruction"]
        pipeline.modules["unit_test_generator"].instruction.value = sd["unit_test_generator_instruction"]
        pipeline.modules["final_code_generator"].instruction.value = sd["final_code_generator_instruction"]
        print(f"Loaded optimized prompts from {merged_pth}")
    else:
        print(f"No optimized prompts found at {merged_pth}; using defaults")
    
    return pipeline


def optimize_with_textgrad(pipeline, trainset, num_iterations=3, batch_size=8):
    """Optimize the prompts using TextGrad."""
    logger = setup_logger(__name__)
    
    # Get the TextGrad-enabled modules
    code_generator = pipeline.textgrad_modules["code_generator"]
    unit_test_generator = pipeline.textgrad_modules["unit_test_generator"]
    final_code_generator = pipeline.textgrad_modules["final_code_generator"]
    
    # Create TextGrad optimizers
    code_gen_optimizer = TextualGradientDescent(
        engine=tg.get_engine(engine_name="gpt-4o-mini"),
        parameters=[code_generator.instruction]
    )
    
    unit_test_optimizer = TextualGradientDescent(
        engine=tg.get_engine(engine_name="gpt-4o-mini"),
        parameters=[unit_test_generator.instruction]
    )
    
    final_code_optimizer = TextualGradientDescent(
        engine=tg.get_engine(engine_name="gpt-4o-mini"),
        parameters=[final_code_generator.instruction]
    )
    
    for iteration in range(num_iterations):
        logger.info(f"Starting TextGrad iteration {iteration + 1}/{num_iterations}")
        
        # Use a subset of training data for each iteration
        # batch = trainset[:batch_size] if len(trainset) > batch_size else trainset
        batch = trainset
        
        code_gen_optimizer.zero_grad()
        unit_test_optimizer.zero_grad()
        final_code_optimizer.zero_grad()
        
        code_gen_total_loss = 0.0
        unit_test_total_loss = 0.0
        final_code_total_loss = 0.0
        
        for idx, example in enumerate(batch):
            # Forward pass through pipeline
            output = {}
            
            code_gen_result = code_generator(question=example.question)
            output["initial_code"] = code_gen_result["initial_code"]
            code_gen_var = code_gen_result["_textgrad_output"]
            
            unit_test_result = unit_test_generator(question=example.question)
            output["additional_unit_tests"] = unit_test_result["additional_unit_tests"]
            unit_test_var = unit_test_result["_textgrad_output"]
            
            exec_result = pipeline.modules["executor"](
                initial_code=output["initial_code"],
                additional_unit_tests=output["additional_unit_tests"]
            )
            output["execution_result"] = exec_result["execution_result"]
            
            final_code_result = final_code_generator(
                question=example.question,
                initial_code=output["initial_code"],
                additional_unit_tests=output["additional_unit_tests"],
                execution_result=output["execution_result"]
            )
            output["code"] = final_code_result["code"]
            final_code_var = final_code_result["_textgrad_output"]
            
            if output["execution_result"] == 0:  
                code_loss = code_loss_fn(
                    code_var=code_gen_var,
                    question=example.question,
                    unit_tests=output["additional_unit_tests"],
                    execution_result=output["execution_result"]
                )
                if code_loss is not None:
                    code_loss.backward()
                    code_gen_total_loss += 1.0
            
            if output["execution_result"] == 0:  
                unit_test_loss = unit_test_loss_fn(
                    unit_test_var=unit_test_var,
                    question=example.question,
                    code=output["initial_code"],
                    execution_result=output["execution_result"]
                )
                if unit_test_loss is not None:
                    unit_test_loss.backward()
                    unit_test_total_loss += 1.0
            
            if output["execution_result"] == 0:  
                final_code_loss = final_code_loss_fn(
                    final_code_var=final_code_var,
                    question=example.question,
                    initial_code=output["initial_code"],
                    unit_tests=output["additional_unit_tests"],
                    execution_result=output["execution_result"]
                )
                if final_code_loss is not None:
                    final_code_loss.backward()
                    final_code_total_loss += 1.0
        
        # Step the optimizers
        if code_gen_total_loss > 0:
            code_gen_optimizer.step()
            logger.info(f"Updated code generator instruction")
        
        if unit_test_total_loss > 0:
            unit_test_optimizer.step()
            logger.info(f"Updated unit test generator instruction")
            
        if final_code_total_loss > 0:
            final_code_optimizer.step()
            logger.info(f"Updated final code generator instruction")
        
        code_gen_checkpoint = {
            "prompt": code_generator.instruction.get_value(),
            "iteration": iteration + 1
        }
        
        unit_test_checkpoint = {
            "prompt": unit_test_generator.instruction.get_value(),
            "iteration": iteration + 1
        }
        
        final_code_checkpoint = {
            "prompt": final_code_generator.instruction.get_value(),
            "iteration": iteration + 1
        }
        
        code_gen_checkpoint_path = os.path.join(CKPT_DIR, f"checkpoint_CodeGenerator_epoch_{iteration+1}.json")
        unit_test_checkpoint_path = os.path.join(CKPT_DIR, f"checkpoint_UnitTestGenerator_epoch_{iteration+1}.json")
        final_code_checkpoint_path = os.path.join(CKPT_DIR, f"checkpoint_FinalCodeGenerator_epoch_{iteration+1}.json")
        
        with open(code_gen_checkpoint_path, "w") as f:
            json.dump(code_gen_checkpoint, f, indent=2)
            
        with open(unit_test_checkpoint_path, "w") as f:
            json.dump(unit_test_checkpoint, f, indent=2)
            
        with open(final_code_checkpoint_path, "w") as f:
            json.dump(final_code_checkpoint, f, indent=2)
        
        # Merge and save combined checkpoint
        merged_out_path = os.path.join(CKPT_DIR, "combined_textgrad_prompts.pth")
        merge_textgrad_checkpoints(
            code_gen_path=code_gen_checkpoint_path,
            unit_test_path=unit_test_checkpoint_path,
            final_code_path=final_code_checkpoint_path,
            out_path=merged_out_path
        )
        
        logger.info(f"Completed iteration {iteration + 1}/{num_iterations}")
    
    return pipeline


if __name__ == "__main__":
    # Argument parsing for flexible experiment control
    parser = argparse.ArgumentParser(description="TextGrad optimization for BigCodeBench pipeline.")
    parser.add_argument('--num_iterations', type=int, default=3, help='Number of TextGrad optimization iterations')
    parser.add_argument('--train_size', type=int, default=500, help='Number of training examples to use')
    parser.add_argument('--eval_size', type=int, default=20, help='Number of evaluation examples to use')
    parser.add_argument('--batch_size', type=int, default=8, help='Batch size for TextGrad optimization (currently not used for batching)')
    parser.add_argument('--max_workers', type=int, default=2, help='Number of workers for pipeline execution')
    args = parser.parse_args()

    dotenv_path = osp.expanduser("/dfs/project/kgrlm/common/.env")
    # dotenv_path = os.getenv("DOTENV_PATH", os.path.expanduser("~/.env"))
    load_dotenv(dotenv_path)
    # 
    
    trainset, valset, testset = dataset_engine()

    # Subset the data for small-scale runs
    trainset = trainset[:args.train_size]
    evalset = testset[:args.eval_size]

    pipeline = pipeline_engine(max_workers=args.max_workers)
    pipeline = optimize_with_textgrad(pipeline, trainset, num_iterations=args.num_iterations, batch_size=args.batch_size)

    metrics = pipeline.evaluate_multiple(evalset)
    print(metrics)
    print(f"Average pass rate: {np.mean(metrics)}")