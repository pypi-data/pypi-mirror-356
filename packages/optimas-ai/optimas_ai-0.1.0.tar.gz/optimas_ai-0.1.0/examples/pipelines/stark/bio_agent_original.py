import os
import os.path as osp
from dotenv import load_dotenv
import joblib
import dspy
from typing import List
from transformers import AutoTokenizer
from tqdm import tqdm

from optimas.arch.base import BaseModule
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.adapt import create_module_from_signature
from examples.metrics.pass_rate import pass_rate
from optimas.utils.api import get_llm_output

import stark_qa
from stark_qa.evaluator import  Evaluator
from examples.pipelines.stark.tools import *
import os.path as osp
from stark_qa.models import VSS
import torch
import json
from examples.datasets.stark_prime import dataset_engine


class KeywordExtractor(BaseModule):
    
    def __init__(self, model='gpt-4o', max_tokens=2048, temperature=1.0):
        super().__init__(
            description="Extract key information needed to answer the question, which will be used as search keywords to retrieve relevant contents from the knowledge base. There are three types of main keywords: 1. gene/protein 2. drug 3. disease",
            input_fields=["question"],
            output_fields=["extracted_keywords"],
            config={
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            variable="""Extracted keywords from the question that belongs to three classes 1. gene/protein 2. drug 3. disease The output should be a dictionary whose keys are the three classes and values are the keywords from the question under the class. Please output only the keyword dictionary but nothing else."""
        )
    
    def forward(self, **inputs):
        candidate_dict = {}
        question = inputs.get("question")
        
        system_prompt = self._variable
        variable_prompt = f"""Input: 
        The question: {question}\n
        Output:"""

        prompt = system_prompt + variable_prompt
        keywords = get_llm_output(
            message=prompt,
            model=self.config.model,
            max_new_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            json_object=True
        )

        if isinstance(keywords, str):
            keywords = load_json(keywords)

        return {"extracted_keywords": keywords}


# whether we want it to be agent (can be only exact match)
class KeywordScorer(BaseModule):
    def __init__(self, kb, model='gpt-4o', max_tokens=2048, temperature=1.0):
        super().__init__(
            description="Score a list of candidates according to their match/relevance with extracted keywords",
            input_fields=["extracted_keywords", "candidate_ids"],
            output_fields=["keyword_scores"],
            config={
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            variable="""You are a scorer of candidates on how much they are matched with a set of extracted keywords. The score should be floating point between 0 to 1.\nThe input is a dictionary of candidates where the keys are candidate ids and the values are the detailed information of the corresponding candidate. \nYou should compare the detailed information of the candidate with the given set of extracted keywords and score each candidate. \nThe output should be a dictionary whose keys are candidate ids and values are the score of the candidate. Please output only the score dictionary but nothing else."""
        )
        self.kb = kb
    
    def forward(self, **inputs):
        candidate_dict = {}
        extracted_keywords = inputs.get("extracted_keywords", None)
        # print(f'{extracted_keywords=}')
        keywords = set()
        for v in extracted_keywords.values():
            for word in v:
                keywords.add(word)
        candidate_ids = inputs.get("candidate_ids", None)

        for i in candidate_ids:
            candidate_dict[i] = self.kb.get_doc_info(i)
        
        system_prompt = self._variable
        variable_prompt = f"""Input: 
        The set of keywords: {keywords}\n
        The candidate dictionary: {candidate_dict}\n\n
        Output:"""

        prompt = system_prompt + variable_prompt
        scores = get_llm_output(
            message=prompt,
            model=self.config.model,
            max_new_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            json_object=True
        )

        if isinstance(scores, str):
            scores = load_json(scores)

        return {"keyword_scores": scores}

class EmbeddingSimScorer(BaseModule):

    def __init__(self, vss, text_embedding_tool, node_embedding_tool, cosine_sim_tool):
        super().__init__(
            description="Score a list of candidates according to their match/relevance with extracted keywords",
            input_fields=["question", "question_id", "candidate_ids"],
            output_fields=["embedding_scores"],
        )
        self.vss = vss
        self.text_embedding_tool = text_embedding_tool
        self.node_embedding_tool = node_embedding_tool
        self.cosine_sim_tool = cosine_sim_tool

    def forward(self, **inputs):
        question = inputs.get('question', None)
        question_id = inputs.get('question_id', None)
        emb_score = {}
        # func 1
        question_embedding = self.text_embedding_tool(question)
        candidate_ids = inputs.get("candidate_ids")

        for i in candidate_ids:
            # func 2
            node_embedding = self.node_embedding_tool(i)
            # func 3
            similarity = float(self.cosine_sim_tool(question_embedding, node_embedding).item())
            emb_score[i] = similarity
        
        return {"embedding_scores": emb_score}

class FinalScorer(BaseModule):
    def __init__(self, model='gpt-4o', max_tokens=2048, temperature=1.0):
        super().__init__(
            description="Score a list of candidates according to their match/relevance with extracted keywords",
            input_fields=["keyword_scores", "embedding_scores", "candidate_ids"],
            output_fields=["candidate_scores"],
            config={
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            variable={
            'default_score': 0.05,
            'embedding_weight': 0.2,
            'similarity_threshold': 0.75,
            }   
        )

    def forward(self, **inputs):
        candidate_ids = inputs.get("candidate_ids", None)
        print(f'{candidate_ids=}')
        score = {int(k): self._variable['default_score'] for k in candidate_ids}

        keyword_scores = inputs.get("keyword_scores", None)
        for i, key_score in keyword_scores.items():
            score[int(i)] += key_score

        embedding_score = inputs.get("embedding_scores", None)

        threshold = self._variable.get("similarity_threshold", None)
        emb_weight = self._variable.get("embedding_weight", None)
        for i, emb_score in embedding_score.items():
            if emb_score >= threshold:
                score[int(i)] += emb_score * emb_weight
                
        candidate_scores_list = [score[i] for i in candidate_ids]
        return {"candidate_scores": candidate_scores_list, "candidate_ids": candidate_ids} 


def pipeline_engine(*args, **kwargs):

    dataset = kwargs.get('dataset', None)
    emb_model = kwargs.get('emb_model', None)
    emb_dir = kwargs.get('emb_dir', None)

    if not osp.exists(emb_dir):
        subprocess.run(["python", "functional/emb_download.py", "--dataset", "prime", "--emb_dir", emb_dir])

    node_emb_dir = osp.join(emb_dir, dataset, emb_model, "doc")
    query_emb_dir = osp.join(emb_dir, dataset, emb_model, "query")

    kb = stark_qa.load_skb(dataset)
    vss = VSS(kb, query_emb_dir, node_emb_dir, emb_model=emb_model)

    text_embedding_tool = GetTextEmbedding()
    node_embedding_tool = GetNodeEmbedding(kb=kb, node_emb_dir=node_emb_dir)
    cosine_sim_tool = ComputeCosineSimilarity(kb=kb)

    pipeline = CompoundAgentPipeline()
    pipeline.register_modules(
        {
            "keyword_extractor": KeywordExtractor(),
            "keyword_scorer": KeywordScorer(kb=kb),
            "embedding_scorer": EmbeddingSimScorer(vss=vss, text_embedding_tool=text_embedding_tool, node_embedding_tool=node_embedding_tool, cosine_sim_tool=cosine_sim_tool),
            "final_scorer": FinalScorer(),
        }
    )

    pipeline.construct_pipeline(
        module_order=[
            "keyword_extractor",
            "keyword_scorer",
            "embedding_scorer",
            "final_scorer",
        ],
        final_output_fields=["candidate_scores"],
        ground_fields=["question", "question_id", "answer_ids", "candidate_ids"],
        eval_func=eval_func,
        kb=kb
    )
    return pipeline

def load_json(response):
    if isinstance(response, str):
        response = response.strip().strip('python').strip('\'').strip('json').strip('```json').strip('"')
        try:
            response = json.loads(response)
            return response
        except Exception as e:
            try:
                response = load_string_to_dict(response)
                return response
            except Exception as e:
                print(f'Warning: {e}, PARSE FAILED')
    return response

def load_string_to_dict(input_string):
    """
    Convert a string representation of a dictionary to an actual Python dictionary.
    The input string should be in format '{key1: value1, key2: value2, ...}'
    
    Args:
        input_string (str): String representation of dictionary
        
    Returns:
        dict: Dictionary with integer keys and float values
    """
    content = input_string.strip('{}')
    result = {}
    try:
        pairs = content.split(', ')
        for pair in pairs:
            key, value = pair.split(': ')
            result[int(key)] = float(value)
    except:
        pairs = content.split(',')
        for pair in pairs:
            key, value = pair.split(': ')
            result[int(key)] = float(value)
    
    return result


def eval_func(question, question_id, candidate_scores, answer_ids, candidate_ids, kb, metrics=["mrr"]):

    candidate_score_dict = {_id: score for _id, score in zip(candidate_ids, candidate_scores)} 
    evaluator = Evaluator(kb.candidate_ids)
    return evaluator(candidate_score_dict, torch.LongTensor(answer_ids), metrics)


if __name__ == "__main__":

    dotenv_path = osp.expanduser("/dfs/project/kgrlm/common/.env")
    load_dotenv(dotenv_path)
    
    dataset = "prime"
    emb_model = "text-embedding-ada-002"
    emb_dir = "/dfs/project/kgrlm/multiagent_reward/emb"

    if not osp.exists(emb_dir):
        subprocess.run(["python", "functional/emb_download.py", "--dataset", "prime", "--emb_dir", emb_dir])

    node_emb_dir = osp.join(emb_dir, dataset, emb_model, "doc")
    query_emb_dir = osp.join(emb_dir, dataset, emb_model, "query")
    kb = stark_qa.load_skb(dataset)
    vss = VSS(kb, query_emb_dir, node_emb_dir, emb_model=emb_model)
    lm = dspy.LM(
        model='openai/gpt-4o-mini',
        max_tokens=1024,
        temperature=0.6
    )
    dspy.settings.configure(lm=lm)
    trainset, valset, testset = dataset_engine(model="gpt-4o-mini")

    text_embedding_tool = GetTextEmbedding()
    node_embedding_tool = GetNodeEmbedding(kb=kb, node_emb_dir=node_emb_dir)
    cosine_sim_tool = ComputeCosineSimilarity(kb=kb)

    stark_args = {
        "dataset": "prime",
        "emb_model": "text-embedding-ada-002",
        "emb_dir": "/dfs/project/kgrlm/multiagent_reward/emb"
    }

    # pipeline = pipeline_engine(kb=kb, vss=vss, text_embedding_tool=text_embedding_tool, node_embedding_tool=node_embedding_tool, cosine_sim_tool=cosine_sim_tool)
    pipeline = pipeline_engine(**stark_args)

    res = []
    for i in tqdm(range(len(testset)), total=len(testset), desc="Eval zero shot pipeline"):
        pred = pipeline(question=testset[i].question, question_id=testset[i].question_id, candidate_ids=testset[i].candidate_ids)
        metric = pipeline.evaluate(example=testset[i], prediction=pred)
        res.append(metric['mrr'])
    
    avg_mrr = sum(res) / len(res)

    print(avg_mrr)
    # print(metric)