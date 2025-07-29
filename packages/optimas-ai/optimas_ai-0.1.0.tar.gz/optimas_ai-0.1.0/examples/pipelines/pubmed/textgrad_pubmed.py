import os
from dotenv import load_dotenv
import json, torch, random, os.path as osp
import numpy as np
import time
from tqdm import tqdm
from sklearn.metrics import classification_report, confusion_matrix
import dspy
import random

import textgrad as tg
from textgrad import Variable, TGD, BlackboxLLM
from textgrad.loss import TextLoss

from optimas.arch.base import BaseModule
from optimas.utils.example import Example
from examples.pipelines.pubmed.pubmed_agents import MODELS_LIST

SCRIPT_DIR = osp.dirname(osp.realpath(__file__))
CKPT_DIR = osp.join(SCRIPT_DIR, "checkpoints")
os.makedirs(CKPT_DIR, exist_ok=True)

# Format prompt for yes/no/maybe answers
FORMAT_PROMPT_YESNO = '''Always conclude the last line of your response should be of the following format: 'Answer: $VALUE' (without quotes) where VALUE is either 'yes' or 'no' or 'maybe'.'''

# System prompt
SYS_SINGLE_SOL_PROMPT = '''You are a scientist.'''

SYS_VAR = Variable(
    SYS_SINGLE_SOL_PROMPT,
    requires_grad=False,
    role_description="system prompt"
)


load_dotenv()
tg.set_backward_engine("gpt-4o-mini", override=True)


def seed_everything(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    try:
        torch.manual_seed(seed)
    except ImportError:
        pass

def merge_textgrad_checkpoints(context_path: str, solver_path: str, out_path: str):
    """
    Load two JSON prompt checkpoints and merge into a single state dict .pth file.
    """
    with open(context_path, 'r') as f:
        ctx = json.load(f)
    with open(solver_path, 'r') as f:
        sol = json.load(f)
    combined = {
        'context_prompt': ctx['prompt'],
        'solver_prompt': sol['prompt']
    }
    torch.save(combined, out_path)
    print(f"Saved combined prompts to {out_path}")

class TextGradContextAnalystModule(BaseModule):
    """
        Summarizer class for context analysis.
        Instruction prompt is learnable.
        Args:
            BaseModule
    """
    def __init__(self, model="gpt-4o-mini", max_tokens=4096, temperature=0.0):
        self.default_model = model
        self.models_list = MODELS_LIST
        
        # Learnable prompt variable via TextGrad
        self.prompt = Variable(
            "You are supposed to summarize the key information from the given context to answer the provided question.",
            requires_grad=True,
            role_description="context instruction"
        )
        
        super().__init__(
            description="TextGrad Context Analyst extracts and summarizes key information from a given context.",
            input_fields=["context", "question"],
            output_fields=["summary", "context_analyst_model"],
            variable=self.prompt.value,
            config={
                "model": model, 
                "max_tokens": max_tokens, 
                "temperature": temperature
            }
        )
        
    @property
    def optimizable(self) -> bool:
        return False 
        
        # self.description   = "TextGrad Context Analyst"
        # self.input_fields  = ["context", "question"]
        # self.output_fields = ["summary"]
        # self.variable      = self.prompt.value
        # self.config        = {
        #     "model": model,
        #     "max_tokens": max_tokens,
        #     "temperature": temperature
        # }
        # self.optimizable = False  # candidate output reranking

    def summarize(self, context: str, question: str) -> Variable:
        """
        For training,
        Sends the combined prompt + context + question to the LLM and returns the response as a Variable
        Args:
            context (str)
            question (str)

        Returns:
            Variable
        """
        # pick at random each instance
        chosen_model = random.choice(self.models_list) if self.models_list else self.default_model
        user_prompt = f'''{self.prompt.value}
        
        Here is the given context: 
        "{context}"
        
        Problem: 
        "{question}"
        
        Please summarize the relevant information from the context related to the question.'''
        response = Variable(user_prompt, requires_grad=True, role_description="summary input")
        return BlackboxLLM(chosen_model, SYS_VAR)(response)
    
    # pipeline API
    def forward(self, context: str, question: str) -> dict:
        # select random model
        chosen_model = random.choice(self.models_list) if self.models_list else self.default_model

        user_prompt = f'''{self.prompt.value}
        
        Here is the given context: 
        "{context}"
        
        Problem: 
        "{question}"
        
        Please summarize the relevant information from the context related to the question.'''        
        x = Variable(user_prompt, requires_grad=True, role_description="summary input")
        response = BlackboxLLM(chosen_model, SYS_VAR)(x)

        return {
            "summary": response.value,
            "context_analyst_model": chosen_model
        }



class TextGradProblemSolverModule(BaseModule):
    """
    Feedback class for problem solving.
    Instruction prompt is learnable.
    """
    def __init__(self, model="gpt-4o-mini", max_tokens=4096, temperature=0.0):
        self.default_model = model
        self.models_list = MODELS_LIST
        
        self.prompt = Variable(
            "You are supposed to provide a solution to a given problem based on the provided summary.",
            requires_grad=True,
            role_description="answer instruction"
        )
        
        super().__init__(
            description="TextGrad Problem Solver determines the correct yes/no/maybe answer based on the provided summary.",
            input_fields=["question", "summary"],
            output_fields=["answer","problem_solver_model"],
            variable=self.prompt.value,
            config={
                "model": model, 
                "max_tokens": max_tokens, 
                "temperature": temperature
            }
        )
        
    @property
    def optimizable(self) -> bool:
        return False 
        
        # self.description   = "TextGrad Problem Solver"
        # self.input_fields  = ["summary", "question"]
        # self.output_fields = ["answer"]
        # self.variable      = self.prompt.value
        # self.config        = {
        #     "model": model,
        #     "max_tokens": max_tokens,
        #     "temperature": temperature
        # }
        # self.optimizable = False


    def solve(self, question: str, summary: str) -> Variable:
        """
        For training,
        Input is a summary + question, and the output is an answer.
        Args:
            summary (str)
            question (str)

        Returns:
            Variable
        """
        # pick the model here
        chosen_model = random.choice(self.models_list) if self.models_list else self.default_model

        # build & call
        user_prompt = f'''{self.prompt.value}
        
        Problem: 
        "{question}"
        
        Here is a summary of relevant information: 
        "{summary}"
        
        Please provide yes, no or maybe to the given problem. {FORMAT_PROMPT_YESNO}'''
        response = Variable(user_prompt, requires_grad=True, role_description="answer input")
        return BlackboxLLM(chosen_model, SYS_VAR)(response)
    
    # pipeline API
    def forward(self, question: str, summary: str) -> dict:
        # pick the model
        chosen_model = random.choice(self.models_list) if self.models_list else self.default_model

        # build & call
        user_prompt = f'''{self.prompt.value}
        
        Problem: 
        "{question}"
        
        Here is a summary of relevant information: 
        "{summary}"
        
        Please provide yes, no or maybe to the given problem. {FORMAT_PROMPT_YESNO}'''
        x = Variable(user_prompt, requires_grad=True, role_description="answer input")
        response = BlackboxLLM(chosen_model, SYS_VAR)(x)

        return {
            "answer": response.value,
            "problem_solver_model": chosen_model
        }

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]
    
def load_prompt_checkpoint(module, epoch):
    ckpt_path = osp.join(
        CKPT_DIR,
        f"checkpoint_{module.__class__.__name__}_epoch_{epoch}.json"
    )
    if osp.exists(ckpt_path):
        with open(ckpt_path, "r") as f:
            checkpoint = json.load(f)
        module.prompt.value = checkpoint["prompt"]
        print(f"Loaded checkpoint from {ckpt_path}")
    else:
        print(f"WARNING: No checkpoint found for {module.__class__.__name__} at epoch {epoch}. Starting over.")

def dataset_engine(data_path="examples/data/", 
                   train_file="combined_PubMedQA_train.jsonl",
                   test_file="combined_PubMedQA_test.jsonl", 
                   train_size=450,  # Number of training examples to use
                   val_size=50,     # Number of validation examples
                   seed=42):
    random.seed(seed)
    train = load_jsonl(osp.join(data_path, train_file))
    test = load_jsonl(osp.join(data_path, test_file))
    
    def to_example(item):
        context = " ".join(item['context']) if isinstance(item['context'], list) else item['context']
        return Example(
            question=item['question'],
            context=context,
            groundtruth=item['groundtruth']
        ).with_inputs('question','context')
    
    # Convert all examples
    train_examples = [to_example(x) for x in train]
    test_examples = [to_example(x) for x in test]
    
    # Shuffle training data
    random.shuffle(train_examples)
    
    # Split training data into train and validation
    val_examples = train_examples[:val_size]
    train_examples = train_examples[val_size:val_size + train_size]
    
    print(f"Dataset sizes:")
    print(f"- Training: {len(train_examples)} examples")
    print(f"- Validation: {len(val_examples)} examples")
    print(f"- Test: {len(test_examples)} examples")
    
    return train_examples, val_examples, test_examples

def summary_loss_fn(summary_var: Variable, question: str, groundtruth: str):
    prompt = (
      f"Is this summary missing crucial details to answer the question?\n"
      f"Question: {question}\n"
      f"Ground Truth Answer: {groundtruth}\n"
      "Provide concise feedback to improve the summary."
    )
    loss = TextLoss(Variable(prompt, 
                             requires_grad=False,
                             role_description="summary evaluation"))(summary_var)
    return loss

def answer_loss_fn(answer_var: Variable, question: str, groundtruth: str):
    prompt = (
      f"Evaluate whether this answer is correct for the biomedical question:\n"
      f"Question: {question}\n"
      f"Ground Truth: {groundtruth}\n"
      "Provide concise feedback to improve the answer instruction."
    )
    return TextLoss(Variable(prompt, 
                             requires_grad=False,
                             role_description="answer evaluation"))(answer_var)

def evaluate_on_validation(module, valset, forward_fn):
    """
    Evaluate a module on the validation set.
    
    Args:
        module: The module to evaluate (context_analyst or problem_solver)
        valset: Validation dataset
        forward_fn: Forward function to use (summarize or solve)
    
    Returns:
        float: Average loss on validation set
    """
    total_loss = 0
    for ex in valset:
        if forward_fn.__name__ == "summarize":
            out = forward_fn(ex.question, ex.context)
            loss = summary_loss_fn(out, ex.question, ex.groundtruth)
        else:
            summary = context_module.summarize(ex.context, ex.question).value
            out = forward_fn(ex.question, summary)
            loss = answer_loss_fn(out, ex.question, ex.groundtruth)
        total_loss += loss.value
    return total_loss / len(valset)

def optimize_module_over_dataset(
    module,         # either ContextAnalyst or ProblemSolver
    trainset,
    valset,         # Added validation set
    forward_fn,     # module.summarize or module.solve
    loss_fn,        # summary_loss_fn or answer_loss_fn
    optimizer,
    n_epochs=3,     # default
    batch_size=8,
    start_epoch=0
):
    n_batches = (len(trainset)+batch_size-1)//batch_size
    
    # Try to load checkpoint if resuming
    if start_epoch > 0:
        load_prompt_checkpoint(module, start_epoch)

    best_val_loss = float('inf')
    best_prompt = None
    
    for epoch in range(start_epoch, n_epochs):
        random.shuffle(trainset)
        all_losses = []
        
        for b in tqdm(range(n_batches), desc=f"Epoch {epoch+1}/{n_epochs}"):
            batch = trainset[b*batch_size:(b+1)*batch_size]
            optimizer.zero_grad()
            
            batch_loss = None
            for ex in batch:
                # forward pass
                if forward_fn.__name__ == "summarize":
                    start = time.time()
                    out = forward_fn(ex.question, ex.context)
                    print(f"summarize took {time.time() - start:.2f}s")
                    # to compute answer you need groundtruth, but summary_loss doesn't need an answer
                    loss = loss_fn(out, ex.question, ex.groundtruth)
                else:
                    # for solver need a summary
                    start_summary = time.time()
                    summary = context_module.summarize(ex.context, ex.question).value
                    duration_summary = time.time() - start_summary
                    print(f"summarize for solver took {duration_summary:.2f}s")

                    start_solve = time.time()
                    out = forward_fn(ex.question, summary)
                    duration_solve = time.time() - start_solve
                    print(f"solve for solver took {duration_solve:.2f}s")
                    loss = loss_fn(out, ex.question, ex.groundtruth)

                batch_loss = loss if batch_loss is None else (batch_loss + loss)

            # Combine losses and step/update
            # Loss is computed per input, but gradient descent is applied once per batch
            batch_loss.backward()
            optimizer.step()
            all_losses.append(loss.value)

        # Evaluate on validation set
        val_loss = evaluate_on_validation(module, valset, forward_fn)
        print(f"\nEpoch {epoch+1} validation loss: {val_loss:.4f}")
        
        # Save best prompt based on validation loss
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_prompt = module.prompt.value
            print(f"New best validation loss: {best_val_loss:.4f}")
            
            # Save best checkpoint
            os.makedirs(CKPT_DIR, exist_ok=True)
            ckpt_path = osp.join(
                CKPT_DIR, 
                f"best_checkpoint_{module.__class__.__name__}.json"
            )
            with open(ckpt_path, "w") as f:
                json.dump({"prompt": best_prompt}, f)
            print(f"Saved best checkpoint to {ckpt_path}")

        # Print a handful of loss messages
        print(f"\n=== Epoch {epoch+1}/{n_epochs} textual loss samples ===")
        for i, txt in enumerate(all_losses[:3]):
            print(f" Batch {i+1}: {txt}")
        if len(all_losses) > 3:
            print(f"  ... (+ {len(all_losses)-3} more batches)")

        # Persist the entire epoch's feedback to JSON
        os.makedirs("eval_results", exist_ok=True)
        with open(f"eval_results/loss_epoch_{epoch+1}.json", "w") as f:
            json.dump(all_losses, f, indent=2)

        # Save regular checkpoint at end of epoch
        os.makedirs(CKPT_DIR, exist_ok=True)
        ckpt_path = osp.join(
            CKPT_DIR, 
            f"checkpoint_{module.__class__.__name__}_epoch_{epoch+1}.json"
        )
        with open(ckpt_path, "w") as f:
            json.dump({"prompt": module.prompt.value}, f)
        print(f"Saved checkpoint to {ckpt_path}")
    
    # Restore best prompt at the end
    if best_prompt:
        module.prompt.value = best_prompt
        print(f"\nRestored best prompt with validation loss: {best_val_loss:.4f}")

if __name__ == "__main__":
    seed_everything(42)
    trainset, valset, testset = dataset_engine(train_size=100, val_size=20)
    os.makedirs(CKPT_DIR, exist_ok=True)
    
    print(f"Loaded {len(trainset)} train examples, {len(valset)} val examples, {len(testset)} test examples")

    # 1. Initialize both modules
    context_module = TextGradContextAnalystModule(model="gpt-4o-mini")
    solver_module = TextGradProblemSolverModule(model="gpt-4o-mini")
    context_start_epoch = 0  # move back to 0 if retrain context analyst prompt
    context_n_epochs = 2
    solver_start_epoch = 0
    solver_n_epochs = 2

    # 2. Optimizers for each prompt
    opt_context = TGD([context_module.prompt])
    opt_solver = TGD([solver_module.prompt])

    # 3. Optimize ContextAnalyst over the training set
    optimize_module_over_dataset(
        context_module,
        trainset,
        valset,
        forward_fn=context_module.summarize,
        loss_fn=summary_loss_fn,
        optimizer=opt_context,
        n_epochs=context_n_epochs,
        batch_size=8,
        start_epoch=context_start_epoch
    )

    # 4. Optimize ProblemSolver over the training set (using current summaries)
    optimize_module_over_dataset(
        solver_module,
        trainset,
        valset, 
        forward_fn=solver_module.solve,
        loss_fn=answer_loss_fn,
        optimizer=opt_solver,
        n_epochs=solver_n_epochs,
        batch_size=8,
        start_epoch=solver_start_epoch
    )

    # 5. Merge TextGrad-optimized prompts 
    context_checkpoint_path = osp.join(
        CKPT_DIR, 
        f"best_checkpoint_{context_module.__class__.__name__}.json"  # Use best checkpoint
    )
    solver_checkpoint_path = osp.join(
        CKPT_DIR, 
        f"best_checkpoint_{solver_module.__class__.__name__}.json"  # Use best checkpoint
    )
    merged_out_path = osp.join(
        CKPT_DIR, 
        "combined_textgrad_prompts.pth"
    )
    merge_textgrad_checkpoints(
        context_path=context_checkpoint_path,
        solver_path=solver_checkpoint_path,
        out_path=merged_out_path
    )
