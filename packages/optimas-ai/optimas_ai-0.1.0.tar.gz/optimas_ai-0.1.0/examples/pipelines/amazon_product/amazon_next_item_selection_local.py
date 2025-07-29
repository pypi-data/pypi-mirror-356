# agentic_pipeline.py
import os
import os.path as osp
import json
import requests
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv
import dspy

from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.base import BaseModule
from optimas.arch.adapt import create_module_from_signature
from examples.datasets.session_based_next_item_selection_dataset import (
    dataset_engine,
)
from optimas.reward.model import RewardModel
from datasets import Dataset

BASE_MODEL_ID = os.getenv(
    "VLLM_BASE_MODEL",
    "/dfs/project/kgrlm/multiagent_reward/trl/local_lm/qwen-1_5b/base",
)


# Helper functions
def accuracy(answer: str, gd_answer: str) -> float:
    """Exact-match accuracy metric."""
    return 1.0 if str(answer) == str(gd_answer) else 0.0


def post_http_request(
    prompt: str,
    api_url: str,
    headers: Dict[str, str],
    base_model: str,
    model_id: str,
    *,
    n: int = 1,
    stream: bool = False,
    max_tokens: int = 512,
) -> requests.Response:
    """
    Send a completion request to *local* vLLM in OpenAI-compatible mode.
    """
    payload: Dict[str, Any] = {
        "model": base_model,
        "prompt": prompt,
        "n": n,
        "temperature": 0.0,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    if model_id is not None:
        payload["model"] = model_id

    return requests.post(
        api_url,
        headers=headers,
        json=payload,
        stream=stream,
        timeout=180,
    )


def get_response(response: requests.Response) -> str:
    """
    Extract the first completion string from an OpenAI response.
    """
    response.raise_for_status()
    data = response.json()
    # OpenAI schema → choices[0].text
    return data["choices"][0]["text"].strip()


# --------------------------------------------------------------------------- #
#  Modules                                                                    #
# --------------------------------------------------------------------------- #
class SessionAnalyzerModule(BaseModule):
    """Summarise a user's session into a compact context string (local LLM)."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8001,
        model_id: str | None = None,
    ):
        self.api_url = f"http://{host}:{port}/v1/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('VLLM_API_KEY', 'dummy')}",
            "User-Agent": "SessionAnalyzerClient",
        }
        self.model_id = model_id
        self._current_adapter_path = None

        super().__init__(
            description="Summarise session into context using local VLLM",
            input_fields=["sequence"],
            output_fields=["context"],
            variable="local_lm",
        )

    def forward(self, **inputs):
        sequence = inputs["sequence"]
        prompt = (
            "You are an e-commerce behaviour analyst.\n\n"
            "Session sequence:\n"
            f"{sequence}\n\n"
            "Provide a 2-3 sentence summary of the user's browsing intent."
        )

        # Use the current model_id (which might be an adapter) or the base model
        model_to_use = self.model_id if self.model_id else BASE_MODEL_ID

        response = post_http_request(
            prompt,
            self.api_url,
            headers=self.headers,
            base_model=BASE_MODEL_ID,
            model_id=model_to_use,
        )
        summary = get_response(response)
        return {"context": summary}


class CandidateProfilerModule(BaseModule):
    """Give line-by-line feedback on each candidate item (local LLM)."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8001,
        model_id: str | None = None,
    ):
        self.api_url = f"http://{host}:{port}/v1/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('VLLM_API_KEY', 'dummy')}",
            "User-Agent": "CandidateProfilerClient",
        }
        self.model_id = model_id
        self._current_adapter_path = None

        super().__init__(
            description="Generate feedback for each candidate using local VLLM",
            input_fields=["context", "choices"],
            output_fields=["feedback"],
            variable="local_lm",
        )

    def forward(self, **inputs):
        context = inputs["context"]
        choices = inputs["choices"]
        prompt = (
            "You are an e-commerce candidate profiler.\n\n"
            "Session summary:\n"
            f"{context}\n\n"
            "Candidate items:\n"
            f"{json.dumps(choices, indent=2)}\n\n"
            "For each item, on its own line, write a brief (1-2 sentence) "
            "comment on why the user might or might not choose it next."
        )

        # Use the current model_id (which might be an adapter) or the base model
        model_to_use = self.model_id if self.model_id else BASE_MODEL_ID

        response = post_http_request(
            prompt,
            self.api_url,
            headers=self.headers,
            base_model=BASE_MODEL_ID,
            model_id=model_to_use,
        )
        feedback = get_response(response)
        return {"feedback": feedback}


class NextItemDecider(dspy.Signature):
    """Select the next item by considering both the summary and the provided feedback carefully."""
    context: str = dspy.InputField(prefix="Context: ", desc="Summary of behaviour")
    feedback: str = dspy.InputField(prefix="Feedback: ", desc="Comments per option")
    answer: str = dspy.OutputField(prefix="Answer: ", desc="Index of item chosen")


# --------------------------------------------------------------------------- #
#  Pipeline factory                                                           #
# --------------------------------------------------------------------------- #
def pipeline_engine(*args, **kwargs):

    session_adapter = kwargs.pop("session_adapter", None)
    profiler_adapter = kwargs.pop("profiler_adapter", None)
    print(f"{session_adapter=}, {profiler_adapter=}")
    # Load secrets
    dotenv_path = osp.expanduser("/dfs/project/kgrlm/common/.env")
    load_dotenv(dotenv_path)

    lm = dspy.LM(
        model="openai/gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        max_tokens=1024,
        temperature=0.3,
    )
    dspy.settings.configure(lm=lm)

    host = os.getenv("VLLM_HOST", "localhost")
    port = int(os.getenv("VLLM_PORT", "8001"))

    # adapter_name = os.getenv("VLLM_ADAPTER_NAME")
    # model_id = os.getenv("VLLM_MODEL_ID")

    pipeline = CompoundAgentPipeline(*args, **kwargs)
    # print("[Pipeline] Registering modules...")
    pipeline.register_modules(
        {
            "session_analyzer": SessionAnalyzerModule(
                host=host, port=port, model_id=session_adapter
            ),
            "candidate_profiler": CandidateProfilerModule(
                host=host, port=port, model_id=profiler_adapter
            ),
            "next_item_decider": create_module_from_signature(NextItemDecider),
        }
    )
    pipeline.construct_pipeline(
        module_order=[
            "session_analyzer",
            "candidate_profiler",
            "next_item_decider",
        ],
        final_output_fields=["answer"],
        ground_fields=["gd_answer"],
        eval_func=accuracy,
    )
    return pipeline




def build_prompt(
    module_name: str,
    sample: Dict,
    policy_role: str = "assistant",
) -> str:
    """
    Re-create *exactly* the prompt used inside the pipeline
    so the policy sees the same distribution it will face at inference.
    """
    if module_name == "session_analyzer":
        sequence = sample.get("sequence", "")
        if not sequence:
            raise ValueError("Missing required 'sequence' field for session_analyzer")

        prompt = (
            "You are an e-commerce behavior analyst.\n\n"
            "Session sequence:\n"
            f"{sequence}\n\n"
            "Provide a 2-3 sentence summary of the user's browsing intent."
        )
    elif module_name == "candidate_profiler":
        context = sample.get("context", "")
        choices = sample.get("choices", [])

        if not context or not choices:
            raise ValueError("Missing required 'context' or 'choices' fields for candidate_profiler")

        prompt = (
            "You are an e-commerce candidate profiler.\n\n"
            "Session summary:\n"
            f"{context}\n\n"
            "Candidate items:\n"
            f"{json.dumps(choices, indent=2)}\n\n"
            "For each item, on its own line, write a brief (1-2 sentence) "
            "comment on why the user might or might not choose it next."
        )
    else:
        raise ValueError(f"Unknown module: {module_name}")

    # We let the **policy** continue from the prompt.
    return prompt


def make_dataset(module_name: str, output_dir: str, split: str = "train", train_size: int = -1) -> Dataset:
    """
    Convert your optimization dataset into a 🤗 Dataset with only the columns
    we need. This function handles the data transformation necessary for PPO training.
    """
    trainset, valset, testset = dataset_engine()
    if train_size != -1:
        trainset = trainset[:min(len(trainset), train_size)]
        print(f"Using {len(trainset)} training examples for ppo training")
    raw_dataset = trainset if split == "train" else testset
    random.seed(42)
    random.shuffle(raw_dataset)

    # Create an intermediary processing pipeline to generate missing fields
    # hard code for Amazon pipeline for now
    temp_pipeline =  pipeline = pipeline_engine(log_dir=output_dir)

    temp_pipeline.rm = None
    temp_pipeline.sample_size = None
    temp_pipeline.modules_to_apply = []

    processed_examples = []
    for example in raw_dataset:
        example_dict = {"sequence": example.sequence, "choices": example.choices, "gd_answer": example.gd_answer}

        # For candidate_profiler, we need to generate 'context' by running through session_analyzer
        if module_name == "candidate_profiler":
            session_result = temp_pipeline.modules["session_analyzer"](sequence=example.sequence)
            example_dict["context"] = session_result["context"]

        processed_examples.append(example_dict)

    hf_dataset = Dataset.from_list(processed_examples)

    def add_prompt(example):
        example["prompt"] = build_prompt(module_name, example)
        return example

    hf_dataset = hf_dataset.map(add_prompt)
    return hf_dataset


def reward_fn_factory(
    reward_model: RewardModel, module_name: str
):
    """
    Wrap the optimas RewardModel so PPOTrainer can call it.
    PPOTrainer expects `reward_fn(samples: List[dict]) -> List[float]`.
    Each sample is a dict with keys `prompt` and `completion`.
    """

    def reward_fn(samples: List[Dict]) -> List[float]:
        rewards = []
        for s in samples:
            if isinstance(s, str):
                s = json.loads(s)

            # Ensure we have the original data
            orig_data = s.get("orig", {})

            if module_name == "session_analyzer":
                reward = reward_model.evaluate(
                    module_name,
                    sequence=orig_data.get("sequence", ""),
                    context=s["completion"],
                    sigmoid=True,
                )
            elif module_name == "candidate_profiler":
                reward = reward_model.evaluate(
                    module_name,
                    context=orig_data.get("context", ""),
                    choices=orig_data.get("choices", []),
                    feedback=s["completion"],
                    sigmoid=True,
                )
            else:
                raise ValueError(f"Unknown module: {module_name}")

            rewards.append(float(reward))
        return rewards

    return reward_fn

if __name__ == "__main__":
    trainset, testset = dataset_engine()

    pipeline = pipeline_engine()

    pred = pipeline(sequence=trainset[0].sequence, choices=trainset[0].choices)

    print("Evaluating on testset...")
    scores = pipeline.evaluate_multiple(testset)
    print("Average score:", sum(scores) / len(scores))
