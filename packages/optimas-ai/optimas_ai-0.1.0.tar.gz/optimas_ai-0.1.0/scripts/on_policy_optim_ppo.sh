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

# ============================
NUM_ITERATIONS=5
NUM_SAMPLES=20
OUTPUT_DIR=$OUTER_DIR/on_policy
# ============================

OUTPUT_DIR=$OUTER_DIR/local_lm/qwen-1_5b
CUDA_VISIBLE_DEVICES=5 python scripts/on_policy_optim.py \
    --dataset $DATASET \
    --samples $NUM_SAMPLES \
    --pipeline $PIPELINE_NAME \
    --preference_dataset $HF_REPO_OR_LOCAL_DIR \
    --output_dir $OUTPUT_DIR \
    --state_dict_path $STATE_DICT_PATH \
    --iterations $NUM_ITERATIONS \
    --weight_optimizer ppo \
    --ppo_train_steps 4 \
    --ppo_epochs 1 \
    --ppo_batch_size 16 \
    --per_module_train_size 15 \
    --run_name PPO-trainsize2-iter3-ppo4-fast-test \
    --iterations 3 \
    --reward_train_size 10 \
    --quiet \
    --no_prompts_opt

