# Usage: source ./evaluate.sh <dataset>
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dataset>"
    exit 1
fi

# Parameters
DATASET=$1

# Load configurations
source scripts/config.sh
set_dataset_config $DATASET
echo "Dataset: $DATASET"
echo "Pipeline name: $PIPELINE_NAME"
echo "State dict path: $STATE_DICT_PATH"

# ================================================================
OUTPUT_DIR=$OUTER_DIR/optim
OPTIMIZE_PROMPT=True
NUM_REPEAT=3
PER_MODULE_TRAIN_SIZE=20

# ============================ Method ====================================
METHOD=preference_scorer
# ======================== FOR PROMPT OPTIMIZATION ========================================
NUM_PROMPT_CANDIDATES=10
PROMPT_OPTIMIZER=opro
RUN_NAME=$PROMPT_OPTIMIZER-$METHOD-trainsize$PER_MODULE_TRAIN_SIZE-n$NUM_PROMPT_CANDIDATES-repeat$NUM_REPEAT-siruis-official-final
FLAG=--reward_model_for_optimization
# ================================================================
MODULES_TO_APPLY=all
# MODULES_TO_APPLY=unit_test_generator


export VLLM_HOST=localhost
export VLLM_PORT=8006


CUDA_VISIBLE_DEVICES=6 python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --sample_size 1 \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --state_dict_path $STATE_DICT_PATH \
    --per_module_train_size $PER_MODULE_TRAIN_SIZE \
    --prompt_optimizer $PROMPT_OPTIMIZER \
    --num_prompt_candidates $NUM_PROMPT_CANDIDATES \
    --modules_to_apply $MODULES_TO_APPLY \
    --hf_repo_or_local_dir $HF_REPO_OR_LOCAL_DIR \
    --num_repeat $NUM_REPEAT ${FLAG} \
    --emb_sim_reward \
    --mode test \
    --verbose false \
    --max_eval_workers 16 \
    --reward_model_for_optimization true \

