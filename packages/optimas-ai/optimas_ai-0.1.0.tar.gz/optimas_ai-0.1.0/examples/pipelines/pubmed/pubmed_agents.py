import os
import os.path as osp
import json
import datetime
import argparse
import random
import re
from tqdm import tqdm
from typing import Dict, List, Any
from dotenv import load_dotenv
import dspy
import random
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.base import BaseModule
from optimas.utils.api import get_llm_output
import torch
import torch.nn.functional as F
import numpy as np
import re
from optimas.reward.model import RewardModel
from optimas.utils.load import load_model_and_tokenizer

# List of available models
MODELS_LIST = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-3.5-turbo-0125",
    "gpt-4-turbo",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20241022",
    "claude-3-7-sonnet-20250219",
]


# class ModelSelectorModule(BaseModule):
#     """
#     Module that selects the most appropriate model for a given task.
#     """
    
#     def __init__(self, task_type="context_analyst", models_list=MODELS_LIST, model="gpt-4o-mini", max_tokens=1024, temperature=0.0):
#         """
#         Initialize the Model Selector Module.
        
#         Args:
#             task_type (str): Type of task to select model for ('context_analyst' or 'problem_solver')
#             models_list (list): List of available models
#             model (str): Model to use for the selector itself
#             max_tokens (int): Maximum tokens for generation
#             temperature (float): Temperature for generation
#         """
#         self.models_list = models_list
#         self.task_type = task_type
#         self.force_model = None

#         if task_type == "context_analyst":
#             variable = f"""YOUR TASK:
# 1. Analyze the complexity of the context and the nature of the biomedical question
# 2. Select the most appropriate model for summarizing the key information from this context
# 3. RESPOND WITH ONLY THE INDEX NUMBER (0-{len(self.models_list)-1}) OF YOUR SELECTED MODEL
# """
#         elif self.task_type == "problem_solver":
#             variable = f"""YOUR TASK:
# 1. Analyze the complexity of the reasoning required to answer this biomedical question
# 2. Select the most appropriate model for determining the answer from the given information
# 3. RESPOND WITH ONLY THE INDEX NUMBER (0-{len(self.models_list)-1}) OF YOUR SELECTED MODEL
# """
#         super().__init__(
#             description=f"Model Selector chooses the most appropriate model for the {task_type} task.",
#             input_fields=["context", "question", "summary"] if task_type == "problem_solver" else ["context", "question"],
#             output_fields=[f"{task_type}_model"],
#             variable=variable,
#             config={
#                 "model": model,
#                 "max_tokens": max_tokens,
#                 "temperature": temperature,
#             }
#         )
        
#     def forward(self, **inputs):
#         """
#         Select the most appropriate model or use the forced model if provided.
        
#         Args:
#             context (str): The medical context to analyze
#             question (str): The biomedical question to answer
#             summary (str, optional): The summary from context analyst (for problem_solver task)
            
#         Returns:
#             dict: Dictionary with the selected model name
#         """
#         return {f"{self.task_type}_model": random.choice(self.models_list)}

#         # Check if a forced model is specified
#         if self.force_model is not None:
#             # Make sure the forced model is in the models list
#             if self.force_model in self.models_list:
#                 return {f"{self.task_type}_model": self.force_model}
#             else:
#                 # Default to first model if forced model is invalid
#                 return {f"{self.task_type}_model": self.models_list[0]}
        
#         context = inputs.get("context", "")
#         question = inputs.get("question", "")
#         summary = inputs.get("summary", "")
        
#         if not question:
#             raise ValueError("Question is required")
        
#         # Format the prompt with numbered model options
#         models_str = "\n".join([f"{i}: {model}" for i, model in enumerate(self.models_list)])
        
#         if self.task_type == "context_analyst":
#             user_prompt = f"""You are a model selector for the Context Analyst task in biomedical question answering.

# TASK DESCRIPTION:
# The Context Analyst analyzes the provided context to summarize the key information needed to answer a biomedical question.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# AVAILABLE MODELS:
# {models_str}

# {self.variable}
# """
#         elif self.task_type == "problem_solver":
#             user_prompt = f"""You are a model selector for the Problem Solver task in biomedical question answering.

# TASK DESCRIPTION:
# The Problem Solver analyzes a summary of biomedical context and determines whether the answer to a yes/no/maybe question is yes, no, or maybe.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# SUMMARY FROM CONTEXT ANALYST:
# {summary}

# AVAILABLE MODELS:
# {models_str}

# {self.variable}
# """
#         # Call the LLM
#         response = get_llm_output(
#             message=user_prompt,
#             model=self.config.model,
#             max_new_tokens=self.config.max_tokens,
#             temperature=self.config.temperature,
#             system_prompt="You are a model selector that only outputs a single number corresponding to your choice."
#         )
        
#         # Extract the model index from the response
#         digit_match = re.search(r'\d+', response.strip())
#         if digit_match:
#             try:
#                 model_index = int(digit_match.group())
#                 # Ensure the index is valid
#                 if model_index < 0 or model_index >= len(self.models_list):
#                     model_index = 0  # Default to the first model if invalid
#             except ValueError:
#                 model_index = 0  # Default to the first model if parsing fails
#         else:
#             model_index = 0  # Default to the first model if no digit found
        
#         # Get the selected model name
#         selected_model = self.models_list[model_index]
        
#         # Return the selected model with appropriate field name
#         return {
#             f"{self.task_type}_model": selected_model
#         }


class ModelSelectorModule(BaseModule):
    """
    Module that selects the most appropriate model for a given task.
    Uses a reward model to score and rank candidate models when available.
    """
    
    def __init__(self, task_type="context_analyst", models_list=MODELS_LIST, model="gpt-4o-mini", max_tokens=1024, temperature=0.0):
        """
        Initialize the Model Selector Module.
        
        Args:
            task_type (str): Type of task to select model for ('context_analyst' or 'problem_solver')
            models_list (list): List of available models
            model (str): Model to use for the selector itself
            max_tokens (int): Maximum tokens for generation
            temperature (float): Temperature for generation
        """
        self.models_list = models_list
        self.task_type = task_type
        self.force_model = None
        self.reward_model = None
        self.softmax_temperature = 1.0  # Controls randomness in softmax sampling

        if task_type == "context_analyst":
            variable = f"""YOUR TASK:
1. Analyze the complexity of the context and the nature of the biomedical question
2. Select the most appropriate model for summarizing the key information from this context
3. RESPOND WITH ONLY THE INDEX NUMBER (0-{len(self.models_list)-1}) OF YOUR SELECTED MODEL
"""
        elif self.task_type == "problem_solver":
            variable = f"""YOUR TASK:
1. Analyze the complexity of the reasoning required to answer this biomedical question
2. Select the most appropriate model for determining the answer from the given information
3. RESPOND WITH ONLY THE INDEX NUMBER (0-{len(self.models_list)-1}) OF YOUR SELECTED MODEL
"""
        super().__init__(
            description=f"Model Selector chooses the most appropriate model for the {task_type} task.",
            input_fields=["context", "question", "summary"] if task_type == "problem_solver" else ["context", "question"],
            output_fields=[f"{task_type}_model"],
            variable=variable,
            config={
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        )
    
    def set_reward_model(self, reward_model):
        """
        Set the reward model to use for scoring candidate models.
        
        Args:
            reward_model (RewardModel): The reward model to use for scoring
        """
        self.reward_model = reward_model
        
    def forward(self, **inputs):
        """
        Select the most appropriate model using reward model scoring and softmax sampling.
        
        Args:
            context (str): The medical context to analyze
            question (str): The biomedical question to answer
            summary (str, optional): The summary from context analyst (for problem_solver task)
            
        Returns:
            dict: Dictionary with the selected model name
        """
        # Check if a forced model is specified
        if self.force_model is not None:
            # Make sure the forced model is in the models list
            if self.force_model in self.models_list:
                return {f"{self.task_type}_model": self.force_model}
            else:
                # Default to first model if forced model is invalid
                return {f"{self.task_type}_model": self.models_list[0]}
        
        # If a reward model is available, use it to score and sample model choices
        if self.reward_model is not None:
            print("using reward model")
            scores = []
            
            for model_name in self.models_list:
                # Create a candidate output
                output = {f"{self.task_type}_model": model_name}
                
                # Combine inputs and the candidate output for scoring
                full_input = {**inputs, **output}
                
                # Get score from reward model
                if self.task_type == "context_analyst":
                    score = self.reward_model.evaluate('context_model_selector', **full_input)
                elif self.task_type == "problem_solver":
                    score = self.reward_model.evaluate('solver_model_selector', **full_input)

                scores.append(score)
            
            # Apply softmax to convert scores to probabilities
            scores_tensor = torch.tensor(scores) / self.softmax_temperature
            probabilities = F.softmax(scores_tensor, dim=0).numpy()
            
            # Sample from the probability distribution
            selected_index = np.random.choice(len(self.models_list), p=probabilities)
            selected_model = self.models_list[selected_index]
            
            # Log the selection process for debugging/analysis
            print(f"[{self.task_type}_selector] Model scores: {list(zip(self.models_list, scores))}")
            print(f"[{self.task_type}_selector] Probabilities after softmax: {list(zip(self.models_list, probabilities))}")
            print(f"[{self.task_type}_selector] Selected model: {selected_model}")
            
            return {f"{self.task_type}_model": selected_model}
        
        return {f"{self.task_type}_model": random.choice(self.models_list)}

# Format prompt for yes/no/maybe answers
FORMAT_PROMPT_YESNO = '''Always conclude the last line of your response should be of the following format: 'Answer: $VALUE' (without quotes) where VALUE is either 'yes' or 'no' or 'maybe'.'''

# System prompt
SYS_SINGLE_SOL_PROMPT = '''You are a scientist.'''

class ContextAnalystModule(BaseModule):
    """
    Module that extracts and summarizes key information from a given context
    to address a question.
    """
    
    def __init__(self, model="gpt-4o-mini", max_tokens=4096, temperature=0.0):
        """
        Initialize the Context Analyst Module.
        
        Args:
            model (str): Default model to use (will be overridden by selected model)
            max_tokens (int): Maximum tokens for generation
            temperature (float): Temperature for generation
        """
        instruction_prompt = "You are supposed to summarize the key information from the given context to answer the provided question."
        super().__init__(
            description="Context Analyst extracts and summarizes key information from a given context.",
            input_fields=["context", "question", "context_analyst_model"],
            output_fields=["summary"],
            variable=instruction_prompt,
            config={
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        )
        
    def forward(self, **inputs):
        """
        Process the context and extract key information.
        
        Args:
            context (str): The medical context to analyze
            question (str): The question to answer
            context_analyst_model (str): The model selected for this task
            
        Returns:
            dict: Dictionary with summary of the context
        """
        context = inputs.get("context")
        question = inputs.get("question")
        model = inputs.get("context_analyst_model", self.config.model)
        
        if not context:
            raise ValueError("Context is required")
        if not question:
            raise ValueError("Question is required")
        
        # Format the prompt
        user_prompt = f'''{self.variable}

Here is the given context:
"{context}"

Problem:
"{question}"

Please summarize the relevant information from the context related to the question.'''
        
        # Call the LLM with the selected model
        response = get_llm_output(
            message=user_prompt,
            model=model,  
            max_new_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system_prompt=SYS_SINGLE_SOL_PROMPT
        )
        
        return {"summary": response}
        

class ProblemSolverModule(BaseModule):
    """
    Module that interprets the Context Analyst's summary and determines
    the correct yes/no/maybe answer based on evidence.
    """
    
    def __init__(self, model="gpt-4o-mini", max_tokens=4096, temperature=0.0):
        """
        Initialize the Problem Solver Module.
        
        Args:
            model (str): Default model to use (will be overridden by selected model)
            max_tokens (int): Maximum tokens for generation
            temperature (float): Temperature for generation
        """
        instruction_prompt = "You are supposed to provide a solution to a given problem based on the provided summary.",
        super().__init__(
            description="Problem Solver determines the correct yes/no/maybe answer based on the provided summary.",
            input_fields=["question", "summary", "problem_solver_model"],
            output_fields=["answer"],
            variable=instruction_prompt,
            config={
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        )
        
    def forward(self, **inputs):
        """
        Process the analyst's summary and determine the answer.
        
        Args:
            question (str): The medical question to answer
            summary (str): The summary provided by the Context Analyst
            problem_solver_model (str): The model selected for this task
            
        Returns:
            dict: Dictionary with the final answer
        """
        question = inputs.get("question")
        summary = inputs.get("summary")
        model = inputs.get("problem_solver_model", self.config.model)
        
        if not question:
            raise ValueError("Question is required")
        if not summary:
            raise ValueError("Summary is required")
        
        # Format the prompt
        user_prompt = f'''{self.variable}

Problem:
"{question}"

Here is a summary of relevant information:
"{summary}"

Please provide yes, no or maybe to the given problem. {FORMAT_PROMPT_YESNO}'''
        
        # Call the LLM with the selected model
        response = get_llm_output(
            message=user_prompt,
            model=model,
            max_new_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            system_prompt=SYS_SINGLE_SOL_PROMPT
        )
        
        return {"answer": response}
        

def extract_answer_yesno(input_string):
    """Extract yes/no/maybe answer from model response."""
    pattern = r"(?i)\s*(yes|no|maybe|Yes|No|Maybe)"
    match = re.search(pattern, input_string)
    extracted_answer = match.group(1).lower() if match else input_string
    return extracted_answer
    

def pubmed_eval_func(answer, groundtruth):
    """
    Evaluation function for PubMedQA that uses the extract_answer_yesno function
    to maintain consistency with your existing code.
    
    Args:
        answer (str): The model's answer text
        groundtruth (str): The correct answer (yes/no/maybe)
        
    Returns:
        float: 1.0 if correct, 0.0 if incorrect
    """
    import re
    
    # Extract the answer using your existing function
    predicted = extract_answer_yesno(answer)
    
    # Normalize groundtruth
    groundtruth = groundtruth.lower().strip()
    
    # Simple exact match scoring
    if predicted.lower() == groundtruth.lower():
        return 1.0
    else:
        return 0.0


def pipeline_engine(force_context_model=None, force_solver_model=None, *args, **kwargs):
    """
    Create and configure a PubMed pipeline with two-stage model selection.
    
    Args:
        force_context_model (str, optional): Force a specific model for context analyst
        force_solver_model (str, optional): Force a specific model for problem solver
        *args: Positional arguments passed to CompoundAgentPipeline
        **kwargs: Keyword arguments
        
    Returns:
        CompoundAgentPipeline: The configured pipeline
    """
    # Extract specific module configurations
    selector_model = kwargs.pop("selector_model", "gpt-4o-mini")
    temperature = kwargs.pop("temperature", 0.0)
    eval_func = kwargs.pop("eval_func", pubmed_eval_func)
    max_tokens = kwargs.pop("max_tokens", 4096)
    
    # Create the pipeline
    pipeline = CompoundAgentPipeline(*args, **kwargs)

    # Register modules
    pipeline.register_modules({
        "context_model_selector": ModelSelectorModule(
            task_type="context_analyst",
            models_list=MODELS_LIST,
            model=selector_model,
            temperature=temperature,
            max_tokens=1024  # Lower tokens for the selector
        ),
        "context_analyst": ContextAnalystModule(
            model="gpt-4o-mini",  # Default model, will be overridden
            temperature=temperature,
            max_tokens=max_tokens
        ),
        "solver_model_selector": ModelSelectorModule(
            task_type="problem_solver",
            models_list=MODELS_LIST,
            model=selector_model,
            temperature=temperature,
            max_tokens=1024  # Lower tokens for the selector
        ),
        "problem_solver": ProblemSolverModule(
            model="gpt-4o-mini",  # Default model, will be overridden
            temperature=temperature,
            max_tokens=max_tokens
        )
    })

    # Set force model if provided
    if force_context_model:
        pipeline.modules["context_model_selector"].config.force_model = force_context_model
    
    if force_solver_model:
        pipeline.modules["solver_model_selector"].config.force_model = force_solver_model

    # Construct pipeline
    pipeline.construct_pipeline(
        module_order=[
            "context_model_selector", 
            "context_analyst", 
            "solver_model_selector",
            "problem_solver"
        ],
        final_output_fields=["answer"], 
        ground_fields=["groundtruth"], 
        eval_func=eval_func
    )
    
    return pipeline

if __name__ == "__main__":
    # Load environment variables 
    dotenv_path = osp.expanduser('/dfs/project/kgrlm/common/.env')
    load_dotenv(dotenv_path)
    
    # Create the pipeline
    pipeline = pipeline_engine(force_context_model="gpt-4o-mini", force_solver_model="claude-3-haiku-20240307")
    
    # Example PubMed question
    context = "Programmed cell death (PCD) is the regulated death of cells within an organism. The lace plant (Aponogeton madagascariensis) produces perforations in its leaves through PCD. The following paper elucidates the role of mitochondrial dynamics during developmentally regulated PCD in vivo in A. madagascariensis. This treatment resulted in lace plant leaves with a significantly lower number of perforations compared to controls, and that displayed mitochondrial dynamics similar to that of non-PCD cells."
    question = "Do mitochondria play a role in remodelling lace plant leaves during programmed cell death?"
    
    # Run the pipeline
    result = pipeline(context=context, question=question)
    
    # Extract and print the answer
    answer = extract_answer_yesno(result.answer)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
