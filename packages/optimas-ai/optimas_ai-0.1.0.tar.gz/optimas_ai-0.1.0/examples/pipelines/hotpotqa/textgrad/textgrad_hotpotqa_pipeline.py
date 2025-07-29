"""
Evaluation‑time pipeline that loads the merged TextGrad prompts.

NUM_REPEAT=3
OUTPUT_DIR=examples/pipelines/hotpotqa/eval/textgrad_hotpoqa
DATASET=hotpotqa
PIPELINE_NAME=textgrad_hotpotqa_pipeline
RUN_NAME=textgrad-repeat$NUM_REPEAT

CUDA_VISIBLE_DEVICES=0 caffeinate python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --num_repeat $NUM_REPEAT \
    --dotenv_path /Users/aaronlee/Documents/Research/preference-prompter/.env \
    --requires_permission_to_run=False
"""
import os, torch, pandas as pd, os.path as osp
from optimas.arch.pipeline import CompoundAgentPipeline
from examples.metrics.f1_score import f1_score
from examples.pipelines.hotpotqa.textgrad.textgrad_modules import (
    TextGradQuestionRewriter, TextGradInfoExtractor, WikipediaRetriever,
    TextGradHintGenerator, TextGradAnswerGenerator
)
from optimas.utils.example import Example


SCRIPT_DIR = osp.dirname(osp.realpath(__file__))
CKPT_DIR   = osp.join(SCRIPT_DIR, "checkpoints")

class TextGradHotpotQAPipeline(CompoundAgentPipeline):
    def __init__(self, log_dir=None, max_sample_workers=4, max_eval_workers=4):
        super().__init__(log_dir=log_dir)
        self.register_modules({
            "question_rewriter": TextGradQuestionRewriter(),
            "info_extractor":   TextGradInfoExtractor(),
            "wikipedia_retriever": WikipediaRetriever(search_space=(1, 5, 10, 25)),
            "hint_generator":   TextGradHintGenerator(),
            "answer_generator": TextGradAnswerGenerator()
        })
        self.modules["wikipedia_retriever"].context(
            randomize_search_variable=True,
            apply=True
        )
        self.modules["wikipedia_retriever"].randomize_search_variable = True
        
        self.construct_pipeline(
            module_order=[
                "question_rewriter", "info_extractor", "wikipedia_retriever",
                "hint_generator", "answer_generator"
            ],
            final_output_fields=["answer"],
            ground_fields=["gd_answer"],
            eval_func=f1_score
        )
        # merged = osp.join(CKPT_DIR, "combined_textgrad_prompts.pth")
        merged = "examples/pipelines/hotpotqa/textgrad/checkpoints/run_20250515_192650/combined_textgrad_prompts.pth"
        if os.path.exists(merged):
            self.load_state_dict(torch.load(merged, map_location="cpu"))
            print(f"[HotpotQAPipeline] loaded prompts from {merged}")
        else:
            print("[HotpotQAPipeline] using default prompts – none trained yet")

    # state serialization for pipeline_eval.py
    def state_dict(self):
        return {
            "rewriter_prompt": self.modules["question_rewriter"].prompt.value,
            "extractor_prompt": self.modules["info_extractor"].prompt.value,
            "retriever_k": self.modules["wikipedia_retriever"].variable["k"],
            "retriever_randomize": True,
            "hint_prompt": self.modules["hint_generator"].prompt.value,
            "answer_prompt": self.modules["answer_generator"].prompt.value
        }

    def load_state_dict(self, sd):
        self.modules["question_rewriter"].prompt.value = sd["rewriter_prompt"]
        self.modules["info_extractor"].prompt.value = sd["extractor_prompt"]
        self.modules["wikipedia_retriever"].update({"k": sd["retriever_k"]})
        if sd.get("retriever_randomize", False):
            self.modules["wikipedia_retriever"].context(randomize_search_variable=True, apply=True)
        self.modules["hint_generator"].prompt.value = sd["hint_prompt"]
        self.modules["answer_generator"].prompt.value = sd["answer_prompt"]

    # optional report (not run off pure pipeline_eval.py)
    def report_by_model(self, testset):
        records = []
        for ex in testset:
            # Run with randomized k value to test different retrieval depths
            with self.modules["wikipedia_retriever"].context(randomize_search_variable=True):
                pred = self(question=ex.question)
                traj = pred.traj
                
                # F1 score
                f1, _, _ = f1_score(pred.answer, ex.gd_answer)
                
                records.append({
                    "rewriter": traj["question_rewriter"]["output"]["rewriter_model"],
                    "extractor": traj["info_extractor"]["output"]["extractor_model"],
                    "retriever_k": self.modules["wikipedia_retriever"].variable["k"],
                    "hint": traj["hint_generator"]["output"]["hint_model"],
                    "answer": traj["answer_generator"]["output"]["answer_model"],
                    "prediction": pred.answer,
                    "groundtruth": ex.gd_answer,
                    "f1_score": f1
                })
                
        df = pd.DataFrame(records)
        
        print("=== Overall Performance ===")
        print(f"Average F1 Score: {df.f1_score.mean():.4f}")
        
        # Performance by model type (wip)
        print("\n=== Performance by Model Type ===")
        for col in ["rewriter", "extractor", "hint", "answer"]:
            print(f"\n--- By {col} model ---")
            for model in sorted(df[col].unique()):
                subset = df[df[col] == model]
                print(f"Model {model} ({len(subset)} examples): F1 = {subset.f1_score.mean():.4f}")
        
        print("\n=== Performance by k value ===")
        for k in sorted(df.retriever_k.unique()):
            subset = df[df.retriever_k == k]
            print(f"k = {k} ({len(subset)} examples): F1 = {subset.f1_score.mean():.4f}")
        
        return df

# factory for pipeline_eval.py
def pipeline_engine(*args, **kwargs):
    return TextGradHotpotQAPipeline(*args, **kwargs)

# --- Added for direct evaluation demonstration ---
if __name__ == "__main__":
    import dspy
    from examples.datasets import registered_dataset  # Assuming this is where datasets are registered
    from optimas.utils.logging import setup_logger

    logger = setup_logger(__name__)

    # --- Configuration for direct evaluation ---
    DATASET_NAME = "hotpotqa"  # Or "hotpotqa_dev", "hotpotqa_test" if specific splits are registered
    EVAL_SUBSET_SIZE = 20       # Number of examples to evaluate from the dataset
    # --- End Configuration ---

    logger.info(f"Initiating direct evaluation for TextGradHotpotQAPipeline.")

    # 1. Load the dataset
    logger.info(f"Loading dataset: {DATASET_NAME}")
    try:
        # Attempt to get a dev or specific split if available and registered that way
        # This part might need adjustment based on how 'hotpotqa' is registered in your setup.
        # If registered_dataset.get("hotpotqa") returns a dict with 'dev' or 'test':
        full_dataset = registered_dataset.get(DATASET_NAME)
        if isinstance(full_dataset, dict) and 'dev' in full_dataset:
            dataset_to_eval = full_dataset['dev']
            logger.info(f"Using 'dev' split of {DATASET_NAME}.")
        elif isinstance(full_dataset, dict) and 'test' in full_dataset:
            dataset_to_eval = full_dataset['test']
            logger.info(f"Using 'test' split of {DATASET_NAME}.")
        elif isinstance(full_dataset, list): # If it's a list of examples
            dataset_to_eval = full_dataset
            logger.info(f"Using full list from {DATASET_NAME}.")
        else:
            raise ValueError(f"Dataset format for '{DATASET_NAME}' not a list or dict with dev/test splits.")

    except Exception as e:
        logger.error(f"Failed to load dataset '{DATASET_NAME}': {e}")
        logger.error("Please ensure the dataset is correctly registered and accessible.")
        logger.error("For HotpotQA, you might typically use a dev set like 'hotpotqa_dev'.")
        exit()

    if not dataset_to_eval:
        logger.error(f"No examples found in the loaded dataset: {DATASET_NAME}.")
        exit()

    # 2. Prepare a subset for evaluation
    if EVAL_SUBSET_SIZE > 0 and len(dataset_to_eval) > EVAL_SUBSET_SIZE:
        eval_subset = dataset_to_eval[:EVAL_SUBSET_SIZE]
        logger.info(f"Using subset of the dataset for evaluation: {len(eval_subset)} examples.")
    else:
        eval_subset = dataset_to_eval
        logger.info(f"Using full loaded dataset for evaluation: {len(eval_subset)} examples.")

    # Ensure examples are Example instances (important for pipeline.evaluate_multiple)
    # This step depends on how your dataset is structured. If they are already Examples, this is fine.
    # If they are dicts, they might need conversion: eval_subset = [Example(**ex) for ex in eval_subset]
    # For now, we assume they are in the correct format or pipeline.evaluate_multiple handles it.
    # Check the first item to provide a hint if it's not a Example
    if eval_subset and not isinstance(eval_subset[0], Example):
        logger.warning("Dataset examples may not be Example instances. Trying to convert.")
        try:
            eval_subset = [Example(**ex) if isinstance(ex, dict) else ex for ex in eval_subset]
            if not isinstance(eval_subset[0], Example):
                 raise ValueError("Conversion to Example failed or was not applicable.")
            logger.info("Successfully converted dataset examples to Example instances.")
        except Exception as e:
            logger.error(f"Failed to convert dataset to Example instances: {e}")
            logger.error("pipeline.evaluate_multiple expects a List[Example]. Please ensure your dataset provides this.")
            exit()
            
    # 3. Instantiate the pipeline (it will load its pre-trained prompts)
    logger.info("Instantiating TextGradHotpotQAPipeline...")
    pipeline = TextGradHotpotQAPipeline()
    # The pipeline automatically loads prompts from CKPT_DIR/combined_textgrad_prompts.pth upon init.

    # 4. Run evaluation
    logger.info(f"Calling pipeline.evaluate_multiple with {len(eval_subset)} examples...")
    if eval_subset: # Proceed only if there's data to evaluate
        # The ground_fields for HotpotQA are ["gd_answer"], and eval_func is f1_score (defined in construct_pipeline)
        evaluation_scores = pipeline.evaluate_multiple(examples=eval_subset)
        
        if evaluation_scores:
            average_score = sum(evaluation_scores) / len(evaluation_scores)
            logger.info(f"pipeline.evaluate_multiple results (scores): {evaluation_scores}")
            logger.info(f"Average score from pipeline.evaluate_multiple on {len(eval_subset)} examples: {average_score:.4f} (metric: f1_score)")
        else:
            logger.warning("pipeline.evaluate_multiple returned no scores.")
    else:
        logger.warning("No data in eval_subset to evaluate.")

    logger.info("Direct evaluation demonstration finished.")
    logger.info("Note: This evaluates the pipeline with its currently saved TextGrad prompts. To retrain/re-optimize prompts, you need to run the separate TextGrad training script for HotpotQA.")

    # Print final results
    print("\nFinal Results:")
    print(f"Average score: {average_score:.4f}")
    
    # Scale results to full dataset size
    full_dataset_size = 1000  # Total training examples in HotpotQA dataset
    scaled_score = average_score * (full_dataset_size / EVAL_SUBSET_SIZE)
    print(f"\nScaled Results (projected to full dataset size of {full_dataset_size}):")
    print(f"Projected average score: {scaled_score:.4f}")
    print(f"Number of iterations: {EVAL_SUBSET_SIZE}")
    print(f"Batch size per iteration: {EVAL_SUBSET_SIZE}")
    print(f"Total examples processed: {EVAL_SUBSET_SIZE}")