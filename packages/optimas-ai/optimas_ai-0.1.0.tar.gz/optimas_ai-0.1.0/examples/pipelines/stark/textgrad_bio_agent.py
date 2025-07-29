import os
import os.path as osp
from dotenv import load_dotenv
import joblib
import dspy
from typing import List
from transformers import AutoTokenizer
from tqdm import tqdm
import numpy as np
import json
import textgrad as tg
from textgrad import Variable, TextualGradientDescent
import random

from optimas.arch.base import BaseModule
from optimas.arch.pipeline import CompoundAgentPipeline
from optimas.arch.adapt import create_module_from_signature
from examples.metrics.mrr import mrr
from optimas.utils.api import get_llm_output
from examples.datasets.stark_prime import subdataset_engine
from optimas.utils.logging import setup_logger

from examples.pipelines.stark.bio_agent import RelationScorerSignature, TextScorerSignature, FinalScorer


class TextGradRelationScorer(BaseModule):
    """TextGrad-enabled RelationScorer with optimizable prompt."""
    
    def __init__(self, model="anthropic/claude-3-haiku-20240307", api_key=None):
        # Only the instruction part is optimizable
        self.instruction = Variable(
            value="Given a question and a list of 5 entities with their relational information, assign each entity a relevance score (between 0 and 1) based on how well its relations match the information in the question.",
            role_description="instruction part of prompt",
            requires_grad=True,
        )
        
        # The fixed format parts (not optimized)
        self.format_template = "\n\nQuery: {question}\n\nRelational Information:\n\n{relation_info}\n\nScores (format as {{1: score1, 2: score2, 3: score3, 4: score4, 5: score5}}): "
        
        # Setup DSPy for actual predictions
        self.lm = dspy.LM(
            model=model,
            api_key=api_key,
            max_tokens=256,
            temperature=0.6,
        )
        
        super().__init__(
            description="Score entities based on relational information",
            input_fields=["question", "relation_info"],
            output_fields=["relation_scores"],
            variable='textgrad'
        )
    
    def forward(self, **inputs):
        logger = setup_logger(__name__)
        # Debug logging
        logger.info(f"Input keys: {list(inputs.keys())}")

        
        question = str(inputs["question"])
        relation_info = inputs["relation_info"]
        
        # Format the relation_info list into a readable string
        if isinstance(relation_info, list):
            logger.info(f"Converting list of length {len(relation_info)}")
            formatted_info = "\n".join([f"Entity {i+1}:\n{str(info)}" for i, info in enumerate(relation_info)])
        else:
            formatted_info = str(relation_info)
        
        logger.info(f"Formatted info type: {type(formatted_info)}")
        
        # Combine instruction and format
        prompt_content = self.instruction.get_value() + self.format_template.format(
            question=question,
            relation_info=formatted_info
        )
        
        logger.info(f"Prompt content type: {type(prompt_content)}")
        
        # Get response using DSPy
        with dspy.context(lm=self.lm):
            response = self.lm(prompt_content)
        
        logger.info(f"Response type: {type(response)}")
        
        # Ensure response is a string
        if not isinstance(response, str):
            response = str(response)
        
        # Create output variable for TextGrad
        output_var = Variable(
            value=response,
            role_description="relation scores prediction",
            requires_grad=True,
            predecessors=[self.instruction]
        )
        
        return {"relation_scores": response, "_textgrad_output": output_var}

class TextGradTextScorer(BaseModule):
    """TextGrad-enabled TextScorer with optimizable prompt."""
    
    def __init__(self, model="anthropic/claude-3-haiku-20240307", api_key=None):
        self.instruction = Variable(
            value="Given a question and a list of 5 entities with their property information, assign each entity a relevance score between 0 and 1 based on how well its properties match the requirements described in the question.",
            role_description="instruction part of prompt",
            requires_grad=True,
        )
        
        # fixed format parts (not optimized)
        self.format_template = "\n\nQuery: {question}\n\nProperty Information:\n\n{text_info}\n\nScores (format as {{1: score1, 2: score2, 3: score3, 4: score4, 5: score5}}): "
        
        self.lm = dspy.LM(
            model=model,
            api_key=api_key,
            max_tokens=256,
            temperature=0.6,
        )
        
        super().__init__(
            description="Score entities based on property information",
            input_fields=["question", "text_info"],
            output_fields=["text_scores"],
            variable='textgrad'
        )
    
    def forward(self, **inputs):
        logger = setup_logger(__name__)
        
        # Debug logging
        logger.info("=== Debug Info ===")
        logger.info(f"Input keys: {list(inputs.keys())}")
        logger.info(f"Question type: {type(inputs['question'])}")
        logger.info(f"Text info type: {type(inputs['text_info'])}")
        
        question = str(inputs["question"])
        text_info = inputs["text_info"]
        
        # Format the text_info list into a readable string
        if isinstance(text_info, list):
            logger.info(f"Converting list of length {len(text_info)}")
            formatted_info = "\n".join([f"Entity {i+1}:\n{str(info)}" for i, info in enumerate(text_info)])
        else:
            formatted_info = str(text_info)
        
        logger.info(f"Formatted info type: {type(formatted_info)}")
        
        # Combine instruction and format
        prompt_content = self.instruction.get_value() + self.format_template.format(
            question=question,
            text_info=formatted_info
        )
        
        logger.info(f"Prompt content type: {type(prompt_content)}")
        
        # Get response using DSPy
        with dspy.context(lm=self.lm):
            response = self.lm(prompt_content)
        
        logger.info(f"Response type: {type(response)}")
        
        # Ensure response is a string
        if not isinstance(response, str):
            response = str(response)
        
        # Create output variable for TextGrad
        output_var = Variable(
            value=response,
            role_description="text scores prediction",
            requires_grad=True,
            predecessors=[self.instruction]
        )
        
        return {"text_scores": response, "_textgrad_output": output_var}

class TextGradFinalScorer(BaseModule):
    """TextGrad-enabled FinalScorer with optimizable prompt."""
    
    def __init__(self, model="anthropic/claude-3-haiku-20240307", api_key=None):
        # Only the instruction part is optimizable
        self.instruction = Variable(
            value="Given a question, assess the importance of textual properties, relational cues, and general semantics in retrieving an entity. Combine the three score lists into a final score list using weighted aggregation.",
            role_description="instruction part of prompt",
            requires_grad=True,
        )
        
        # The fixed format parts (not optimized)
        self.format_template = "\n\nQuery: {question}\n\nEmbedding Scores: {emb_scores}\n\nRelation Scores: {relation_scores}\n\nText Scores: {text_scores}\n\nFinal Scores: "
        
        # Setup DSPy for actual predictions
        self.lm = dspy.LM(
            model=model,
            api_key=api_key,
            max_tokens=256,
            temperature=0.6,
        )
        
        # Initialize weights similar to original pipeline
        variable = {
            'relation_weight': 0.1,
            'text_weight': 0.1
        }
        
        super().__init__(
            description="Combine scores using weighted aggregation",
            input_fields=["question", "emb_scores", "relation_scores", "text_scores"],
            output_fields=["final_scores"],
            variable=variable,
            variable_search_space={
                'relation_weight': [0.1, 1.0],
                'text_weight': [0.1, 1.0]
            }
        )

    def forward(self, **inputs):
        logger = setup_logger(__name__)
        
        question = inputs.get("question")
        emb_scores = inputs.get("emb_scores")
        relation_scores = inputs.get("relation_scores")
        text_scores = inputs.get("text_scores")
        
        # More robust extraction of scores from relation_scores
        relation_scores_parsed = [0] * 5
        if isinstance(relation_scores, str):
            # Try to find JSON-like pattern {1: 0.5, 2: 0.7, ...} in the text
            import re
            json_pattern = r'\{(?:\s*\d+\s*:\s*\d+(?:\.\d+)?\s*,?\s*)+\}'
            json_matches = re.findall(json_pattern, relation_scores)
            if json_matches:
                try:
                    # Extract the first JSON-like pattern and parse it
                    scores_dict = json.loads(json_matches[0].replace("'", '"'))
                    relation_scores_parsed = [float(scores_dict.get(str(i), 0)) for i in range(1, 6)]
                except:
                    logger.warning("Failed to parse JSON from relation_scores")
        
        # More robust extraction of scores from text_scores
        text_scores_parsed = [0] * 5
        if isinstance(text_scores, str):
            # Try to find JSON-like pattern {1: 0.5, 2: 0.7, ...} in the text
            import re
            json_pattern = r'\{(?:\s*\d+\s*:\s*\d+(?:\.\d+)?\s*,?\s*)+\}'
            json_matches = re.findall(json_pattern, text_scores)
            if json_matches:
                try:
                    # Extract the first JSON-like pattern and parse it
                    scores_dict = json.loads(json_matches[0].replace("'", '"'))
                    text_scores_parsed = [float(scores_dict.get(str(i), 0)) for i in range(1, 6)]
                except:
                    logger.warning("Failed to parse JSON from text_scores")
            
        # Handle embedding scores
        try:
            if isinstance(emb_scores, str):
                emb_scores = json.loads(emb_scores)
            if isinstance(emb_scores, list):
                emb_scores = [float(x) for x in emb_scores]
            else:
                emb_scores = [0 for _ in range(5)]
            assert len(emb_scores) == 5
        except:
            emb_scores = [0 for _ in range(5)]
            
        relation_weight = self.variable['relation_weight']
        text_weight = self.variable['text_weight']

        # Calculate final scores using weighted combination
        final_scores = [relation_weight * r + text_weight * t + e for r, t, e in zip(relation_scores_parsed, text_scores_parsed, emb_scores)]
        final_scores = [round(x, 2) for x in final_scores]
        
        # Log the extracted scores for debugging
        logger.info(f"Extracted relation scores: {relation_scores_parsed}")
        logger.info(f"Extracted text scores: {text_scores_parsed}")
        logger.info(f"Final scores (computed): {final_scores}")
        
        # Create output variable for TextGrad
        output_var = Variable(
            value=str(final_scores),  # Convert to string for TextGrad
            role_description="final scores prediction",
            requires_grad=True,
            predecessors=[self.instruction]
        )
        
        return {"final_scores": final_scores, "_textgrad_output": output_var}

def pipeline_engine(*args, **kwargs):
    """Create pipeline with TextGrad optimization for Stark modules."""
    dotenv_path = os.getenv("DOTENV_PATH", os.path.expanduser("~/.env"))
    load_dotenv(dotenv_path)
    
    # Set up engines following TextGrad pattern
    llm_api_eval = tg.get_engine(engine_name=kwargs.get("optimization_model", "gpt-4o-mini"))
    tg.set_backward_engine(llm_api_eval, override=True)

    pipeline = CompoundAgentPipeline(*args, **kwargs)
    
    # Create TextGrad-enabled modules with prediction model
    prediction_model = kwargs.get("prediction_model", "anthropic/claude-3-haiku-20240307")
    
    relation_scorer = TextGradRelationScorer(
        model=prediction_model,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    text_scorer = TextGradTextScorer(
        model=prediction_model,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    # final_scorer = FinalScorer()
    
    final_scorer = TextGradFinalScorer(
        model=prediction_model,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    # Register modules
    pipeline.register_modules({
        "relation_scorer": relation_scorer,
        "text_scorer": text_scorer,
        "final_scorer": final_scorer,
    })

    # Construct pipeline
    pipeline.construct_pipeline(
        module_order=[
            "relation_scorer",
            "text_scorer",
            "final_scorer"
        ],
        final_output_fields=["final_scores"],
        ground_fields=["candidate_ids", "answer_ids"],
        eval_func=mrr
    )
    
    # Store references to TextGrad modules
    pipeline.textgrad_modules = {
        "relation_scorer": relation_scorer,
        "text_scorer": text_scorer,
        "final_scorer": final_scorer
    }
    
    return pipeline

def optimize_module_with_textgrad(
    module,
    module_name,
    trainset,
    valset,
    testset,
    num_epochs=3,
    batch_size=8,
    max_eval_workers=4,
    start_epoch=0
):
    """Optimize a single module using TextGrad."""
    logger = setup_logger(__name__)
    
    # Create TextGrad optimizer
    optimizer = TextualGradientDescent(
        engine=tg.get_engine(engine_name="gpt-4o-mini"),
        parameters=[module.instruction]
    )
    
    best_val_mrr = 0.0
    best_instruction = module.instruction.get_value()
    
    # Create checkpoint directory
    ckpt_dir = "examples/pipelines/stark/checkpoints"
    os.makedirs(ckpt_dir, exist_ok=True)
    
    # Try to load checkpoint if resuming
    if start_epoch > 0:
        ckpt_path = osp.join(ckpt_dir, f"checkpoint_{module_name}_epoch_{start_epoch}.json")
        if os.path.exists(ckpt_path):
            with open(ckpt_path, "r") as f:
                checkpoint = json.load(f)
                module.instruction.value = checkpoint["instruction"]
                logger.info(f"Loaded checkpoint from {ckpt_path}")
    
    n_batches = (len(trainset) + batch_size - 1) // batch_size
    
    for epoch in range(start_epoch, num_epochs):
        logger.info(f"\nStarting epoch {epoch + 1}/{num_epochs} for {module_name}")
        random.shuffle(trainset)
        all_losses = []
        
        for b in range(n_batches):
            batch = trainset[b * batch_size:(b + 1) * batch_size]
            
            optimizer.zero_grad()
            
            batch_loss = None
            for example in batch:
                # Forward pass
                try:
                    result = module(**example)
                    
                    logger.info(f"Result keys: {result.keys()}")
                    
                    output = result.get("_textgrad_output")
                    if output is None:
                        logger.warning("No _textgrad_output in result")
                        continue
                    
                    candidate_ids = example.get('candidate_ids', [])
                    answer_ids = example.get('answer_ids', [])
                    
                    if not candidate_ids or not answer_ids:
                        logger.warning(f"Missing candidate_ids or answer_ids: {candidate_ids}, {answer_ids}")
                        continue
                    
                    # Get the appropriate scores
                    if module_name == "relation_scorer":
                        scores_raw = result.get('relation_scores', '')
                        logger.info(f"Relation scores raw: {type(scores_raw)}")
                        if isinstance(scores_raw, list) and len(scores_raw) > 0 and isinstance(scores_raw[0], str):
                            # We have a list containing a string - process it
                            module_scores = extract_numeric_scores(scores_raw)
                        else:
                            module_scores = extract_numeric_scores(scores_raw)
                    elif module_name == "text_scorer":
                        scores_raw = result.get('text_scores', '')
                        logger.info(f"Text scores raw: {type(scores_raw)}")
                        module_scores = extract_numeric_scores(scores_raw)
                    else:  # final_scorer or others
                        module_scores = result.get('final_scores', [0] * 5)
                    
                    # Ensure we have a list of numeric values
                    if not isinstance(module_scores, list) or len(module_scores) != 5:
                        logger.warning(f"Invalid module_scores: {module_scores}")
                        module_scores = [0] * 5
                    
                    # Ensure all scores are numeric
                    module_scores = [float(score) if isinstance(score, (int, float)) else 0.0 for score in module_scores]
                        
                    logger.info(f"Candidate IDs: {candidate_ids}")
                    logger.info(f"Module Scores: {module_scores}")
                    logger.info(f"Answer IDs: {answer_ids}")
                    
                    score = mrr(candidate_ids, module_scores, answer_ids)
                    logger.info(f"MRR Score: {score}")
                    
                    if score < 1.0:  # Not perfect ranking
                        # Create loss based on module type
                        if module_name == "relation_scorer":
                            loss_text = f"""
                            The model predicted relation scores: {result['relation_scores']}
                            The ground truth ranking was: {example['answer_ids']}

                            Please improve the instruction to help the model better score relations.
                            """
                        else:  # text_scorer
                            loss_text = f"""
                            The model predicted text scores: {result['text_scores']}
                            The ground truth ranking was: {example['answer_ids']}

                            Please improve the instruction to help the model better score text properties.
                            """
                        
                        loss = Variable(
                            value=loss_text,
                            role_description=f"{module_name} loss",
                            requires_grad=True,
                            predecessors=[output]
                        )
                        
                        # Backward pass
                        loss.backward()
                        
                        batch_loss = loss if batch_loss is None else (batch_loss + loss)
                        all_losses.append(loss.value)
                except Exception as e:
                    logger.error(f"Error processing example: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    continue
            
            # Step optimizer if we had any losses
            if batch_loss is not None:
                optimizer.step()
        
        # Print sample losses
        logger.info(f"\n=== Epoch {epoch + 1}/{num_epochs} textual loss samples ===")
        for i, txt in enumerate(all_losses[:3]):
            logger.info(f"Batch {i + 1}: {txt}")
        if len(all_losses) > 3:
            logger.info(f"  ... (+ {len(all_losses) - 3} more batches)")
        
        # Save losses to file
        os.makedirs("eval_results", exist_ok=True)
        with open(f"eval_results/loss_{module_name}_epoch_{epoch + 1}.json", "w") as f:
            json.dump(all_losses, f, indent=2)
        
        # Validation step
        logger.info(f"\nRunning validation for {module_name}...")
        try:
            val_metrics = module.evaluate_multiple(valset)
            avg_val_mrr = np.mean(val_metrics)
            logger.info(f"Validation MRR: {avg_val_mrr:.4f}")
            
            # Save best instruction if validation improves
            if avg_val_mrr > best_val_mrr:
                best_val_mrr = avg_val_mrr
                best_instruction = module.instruction.get_value()
                logger.info(f"New best validation MRR: {best_val_mrr:.4f}")
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            avg_val_mrr = 0.0
        
        # Save checkpoint
        ckpt_path = osp.join(ckpt_dir, f"checkpoint_{module_name}_epoch_{epoch + 1}.json")
        with open(ckpt_path, "w") as f:
            json.dump({
                "instruction": module.instruction.get_value(),
                "val_mrr": avg_val_mrr
            }, f, indent=2)
        logger.info(f"Saved checkpoint to {ckpt_path}")
    
    # Restore best instruction
    module.instruction.value = best_instruction
    
    # Final evaluation on test set
    logger.info(f"\nRunning final evaluation for {module_name}...")
    try:
        test_metrics = module.evaluate_multiple(testset)
        avg_test_mrr = np.mean(test_metrics)
        logger.info(f"Test MRR: {avg_test_mrr:.4f}")
    except Exception as e:
        logger.error(f"Error during test evaluation: {e}")
        test_metrics = []
        avg_test_mrr = 0.0
    
    return {
        "best_val_mrr": best_val_mrr,
        "test_mrr": avg_test_mrr,
        "test_metrics": test_metrics
    }

def extract_numeric_scores(text):
    """Extract numerical scores from text that may contain JSON-like structures."""
    logger = setup_logger(__name__)
    logger.info(f"Input to extract_numeric_scores: {type(text)}, {text[:100]}...")
    
    # Handle different input types
    if isinstance(text, list):
        # If we got a list, use the first element
        if len(text) > 0:
            text = text[0]
        else:
            return [0] * 5
    
    if not isinstance(text, str):
        return [0] * 5
    
    # Try to find JSON-like pattern {1: 0.5, 2: 0.7, ...} in the text
    import re
    json_pattern = r'\{(?:\s*\d+\s*:\s*\d+(?:\.\d+)?\s*,?\s*)+\}'
    json_matches = re.findall(json_pattern, text)
    
    if json_matches:
        try:
            # Extract the first JSON-like pattern and parse it
            scores_dict = json.loads(json_matches[0].replace("'", '"'))
            return [float(scores_dict.get(str(i), 0)) for i in range(1, 6)]
        except Exception as e:
            logger.warning(f"Failed to parse JSON: {e}")
    
    # Try to extract scores directly from lines with "Score: X"
    scores = []
    lines = text.split('\n')
    for line in lines:
        if 'Score:' in line or 'Score: ' in line:
            try:
                # Try different patterns for score extraction
                if 'Score:' in line:
                    score_text = line.split('Score:')[-1].strip()
                else:
                    score_text = line.split('Score: ')[-1].strip()
                
                # If the score has additional text after it, try to extract just the number
                if ' ' in score_text:
                    score_text = score_text.split(' ')[0]
                
                score = float(score_text)
                
                # Normalize score to 0-1 range if it's not already
                if score > 1:
                    score = score / 5.0
                scores.append(score)
                logger.info(f"Extracted score: {score} from line: {line}")
            except Exception as e:
                logger.warning(f"Failed to extract score from line: {line}, error: {e}")
                continue
    
    logger.info(f"Extracted scores: {scores}")
    
    # If we failed to extract all 5 scores but found some
    if len(scores) > 0 and len(scores) < 5:
        # Extract any number followed by patterns like /5, out of 5, etc.
        number_pattern = r'(\d+(?:\.\d+)?)\s*(?:\/|out of|of|from)\s*5'
        number_matches = re.findall(number_pattern, text)
        
        # Add any found scores to our list
        for match in number_matches:
            try:
                score = float(match) / 5.0  # Normalize to 0-1
                scores.append(score)
            except:
                continue
    
    # Return the scores if we found exactly 5, otherwise handle partial lists
    if len(scores) == 5:
        return scores
    elif len(scores) > 5:
        return scores[:5]
    else:
        # If we don't have enough scores but the text mentions numbered items
        # Try to extract scores from numerical indicators
        numbered_scores = {}
        
        # Look for numbered items like "1. ... Score: X" or similar patterns
        number_pattern = r'(\d+)\.\s*(.*?)\s*(?:Score:|score:|-\s*Score:|-\s*score:)\s*(\d+(?:\.\d+)?)'
        numbered_matches = re.findall(number_pattern, text)
        
        for num, _, score in numbered_matches:
            try:
                idx = int(num) - 1  # Convert to 0-based index
                if 0 <= idx < 5:
                    score_val = float(score)
                    if score_val > 1:
                        score_val = score_val / 5.0
                    numbered_scores[idx] = score_val
            except:
                continue
        
        # Create a full list of 5 scores
        result = [0] * 5
        
        # Fill in the scores we extracted by position
        for idx, score in numbered_scores.items():
            result[idx] = score
        
        # Use any remaining scores we extracted earlier to fill in missing values
        for i in range(5):
            if result[i] == 0 and scores:
                result[i] = scores.pop(0)
        
        return result

def optimize_with_textgrad(pipeline, trainset, valset, testset, num_epochs=3, batch_size=8, max_eval_workers=4):
    """Optimize the Stark pipeline modules sequentially using TextGrad."""
    logger = setup_logger(__name__)
    
    # Get the TextGrad-enabled modules
    relation_scorer = pipeline.textgrad_modules["relation_scorer"]
    text_scorer = pipeline.textgrad_modules["text_scorer"]
    
    # Optimize relation scorer
    logger.info("\n=== Optimizing Relation Scorer ===")
    relation_metrics = optimize_module_with_textgrad(
        module=relation_scorer,
        module_name="relation_scorer",
        trainset=trainset,
        valset=valset,
        testset=testset,
        num_epochs=num_epochs,
        batch_size=batch_size,
        max_eval_workers=max_eval_workers
    )
    
    # Optimize text scorer
    logger.info("\n=== Optimizing Text Scorer ===")
    text_metrics = optimize_module_with_textgrad(
        module=text_scorer,
        module_name="text_scorer",
        trainset=trainset,
        valset=valset,
        testset=testset,
        num_epochs=num_epochs,
        batch_size=batch_size,
        max_eval_workers=max_eval_workers
    )
    
    return pipeline, {
        "relation_scorer": relation_metrics,
        "text_scorer": text_metrics
    }

def main():
    # Setup paths and environment
    # dotenv_path = osp.expanduser("~/.env")
    # load_dotenv(dotenv_path)
    

    dotenv_path = osp.expanduser("/dfs/project/kgrlm/common/.env")
    load_dotenv(dotenv_path)
    
    
    # Load dataset
    trainset, valset, testset = subdataset_engine()
    
    # Create pipeline
    pipeline = pipeline_engine()
    
    # Print original instructions
    logger = setup_logger(__name__)
    logger.info("Original instructions:")
    logger.info(f"Relation scorer: {pipeline.textgrad_modules['relation_scorer'].instruction.get_value()}")
    logger.info(f"Text scorer: {pipeline.textgrad_modules['text_scorer'].instruction.get_value()}")
    logger.info(f"Final scorer: {pipeline.textgrad_modules['final_scorer'].instruction.get_value()}")
    
    # Optimize with TextGrad
    logger.info("Starting TextGrad optimization...")
    optimized_pipeline, metrics = optimize_with_textgrad(
        pipeline=pipeline,
        trainset=trainset[:50],
        valset=valset[:20],
        testset=testset,
        num_epochs=1,
        batch_size=4,
        max_eval_workers=4
    )
    
    # Save optimized instructions and metrics
    output_dir = "examples/pipelines/stark/checkpoints_test"
    os.makedirs(output_dir, exist_ok=True)
    
    prompt_state = {
        "relation_scorer": {
            "original_instruction": pipeline.textgrad_modules["relation_scorer"].instruction.get_value(),
            "optimized_instruction": optimized_pipeline.textgrad_modules["relation_scorer"].instruction.get_value(),
            "metrics": metrics["relation_scorer"]
        },
        "text_scorer": {
            "original_instruction": pipeline.textgrad_modules["text_scorer"].instruction.get_value(),
            "optimized_instruction": optimized_pipeline.textgrad_modules["text_scorer"].instruction.get_value(),
            "metrics": metrics["text_scorer"]
        }
    }
    
    # Save to JSON file
    with open(osp.join(output_dir, "optimized_prompts.json"), "w") as f:
        json.dump(prompt_state, f, indent=2)
    
    # Also save a simple text file with just the instructions and metrics
    with open(osp.join(output_dir, "optimized_instructions.txt"), "w") as f:
        f.write("Relation Scorer:\n")
        f.write(f"Original: {prompt_state['relation_scorer']['original_instruction']}\n")
        f.write(f"Optimized: {prompt_state['relation_scorer']['optimized_instruction']}\n")
        f.write(f"Best Validation MRR: {metrics['relation_scorer']['best_val_mrr']:.4f}\n")
        f.write(f"Test MRR: {metrics['relation_scorer']['test_mrr']:.4f}\n\n")
        
        f.write("Text Scorer:\n")
        f.write(f"Original: {prompt_state['text_scorer']['original_instruction']}\n")
        f.write(f"Optimized: {prompt_state['text_scorer']['optimized_instruction']}\n")
        f.write(f"Best Validation MRR: {metrics['text_scorer']['best_val_mrr']:.4f}\n")
        f.write(f"Test MRR: {metrics['text_scorer']['test_mrr']:.4f}\n")
    
    logger.info(f"\nInstructions and metrics saved to:")
    logger.info(f"- {osp.join(output_dir, 'optimized_prompts.json')}")
    logger.info(f"- {osp.join(output_dir, 'optimized_instructions.txt')}")

if __name__ == "__main__":
    main()
