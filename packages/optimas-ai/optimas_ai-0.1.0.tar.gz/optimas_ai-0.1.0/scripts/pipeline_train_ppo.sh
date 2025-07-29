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

OPTIMIZE_PROMPT=True
NUM_REPEAT=1
PER_MODULE_TRAIN_SIZE=400
TRAIN_STEP=3
# set the output directory for base and ppo models
OUTPUT_DIR=$OUTER_DIR/local_lm/qwen-1_5b

# ============================ Method ====================================
METHOD=PPO
# ======================== FOR PROMPT OPTIMIZATION ========================================
RUN_NAME=$METHOD-trainsize$PER_MODULE_TRAIN_SIZE-official-final-0.25epoch-new-reward-$TRAIN_STEP-384-5
reward_model_for_optimization=true
# ======================== FOR PPO========================================
PPO_BASE_MODEL_NAME=Qwen/Qwen2.5-1.5B-Instruct
MODULES_TO_APPLY=all
# MODULES_TO_APPLY=unit_test_generator

export VLLM_HOST=localhost
export VLLM_PORT=8001

# 4: 0,1 7: 6,7 1:6,7
CUDA_VISIBLE_DEVICES=6,7 python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --sample_size 1 \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --state_dict_path $STATE_DICT_PATH \
    --per_module_train_size $PER_MODULE_TRAIN_SIZE \
    --modules_to_apply $MODULES_TO_APPLY \
    --hf_repo_or_local_dir $HF_REPO_OR_LOCAL_DIR \
    --num_repeat $NUM_REPEAT ${FLAG} \
    --weight_optimizer PPO \
    --ppo_train_steps $TRAIN_STEP \
    --ppo_epochs 3 \
    --ppo_batch_size 16 \
    --ppo_save_epoch_ratio 1 \
    --max_sample_workers 1 \
    --ppo_base_model_name $PPO_BASE_MODEL_NAME \
    --reward_model_for_optimization $reward_model_for_optimization \
    --mode train \
    --reward_device cuda:0 \
    --policy_device cuda:1


