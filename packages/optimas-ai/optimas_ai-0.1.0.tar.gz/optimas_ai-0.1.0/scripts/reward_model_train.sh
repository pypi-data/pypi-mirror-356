# Usage: source scripts/reward_model_train.sh <dataset>
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
echo "Lora r: $LORA_R"
echo "Lora alpha: $LORA_ALPHA"
echo "Lora dropout: $LORA_DROPOUT"
echo "Max length: $MAX_LENGTH"
# ================================================================

RANDOM_SEED=$$
PORT=$((56780 + RANDOM_SEED % 100))
# --------------------------
RUN_NAME=submit_multihead_bs8_1e-6_bad_models_small
# --------------------------
BASE_MODEL_NAME=Qwen/Qwen2.5-Coder-7B-Instruct
BASE_MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
# --------------------------
METHOD=preference_scorer
# METHOD=preference_modular_model_prior
# METHOD=abs_value_llm_judge
# --------------------------
DATASET_FORMAT=implicit_preference
METRIC_FOR_BEST_MODEL=eval_loss

# DATASET_FORMAT=value_based
# METRIC_FOR_BEST_MODEL=eval_loss
# --------------------------
HF_DATASET_NAME=$PIPELINE_NAME-$METHOD
# HF_DATASET_NAME=preference_iterative_hard
# --------------------------
STATIC_DS_SET=$OUTER_DIR/data/static_test/$PIPELINE_NAME.json
STATIC_DS_SET=None
# ---------------------------
USE_LORA=True
# ---------------------------

WANDB_PROJECT=optimas
WANDB_ENTITY=dsp-team
HF_ENTITY=snap-stanford
TRAIN_MULTI_HEAD=True
NUM_TRAIN_EPOCHS=1
LEARNING_RATE=1e-6
PER_DEVICE_TRAIN_BATCH_SIZE=1
GRADIENT_ACCUMULATION_STEPS=4
PER_DEVICE_EVAL_BATCH_SIZE=1
EVAL_STEPS=4
SAVE_STEPS=4
MAX_STEPS=-1
LOGGING_STEPS=1
SAVE_TOTAL_LIMIT=50
EVAL_RATIO=0.10
REPORT_TO=wandb
EVAL_STRATEGY=steps
LOAD_IN_4BIT=False
LOAD_IN_8BIT=False
PUSH_TO_HUB=False
ADD_MARGIN=True
USE_SCORE_NORM=False
USE_SCORE_SCALING=False
TEST_BEST_MODEL_ONLY=False
SAVE_MODEL_PER_MODULE=True
# --------------------------
TEST_STATIC_ROLLOUTS_PER_MODULE=True
TEST_STATIC_ROLLOUTS_PER_MODULE=False
# --------------------------

# --------- UNCOMMENT FOR DEBUGGING
# RUN_NAME=debug
# BASE_MODEL_NAME=meta-llama/Llama-3.2-1B-Instruct
# LOAD_IN_4BIT=True
# PUSH_TO_HUB=False
# EVAL_STEPS=1
# SAVE_STEPS=1
# MAX_STEPS=3
# SAVE_TOTAL_LIMIT=2
# LEARNING_RATE=1e-3
# NPROC_PER_NODES=1
# export CUDA_VISIBLE_DEVICES=7
# --------------------------
WARMUP_STEPS=0
NPROC_PER_NODES=2
export CUDA_VISIBLE_DEVICES=0,1

OUTPUT_DIR=$OUTER_DIR/output/reward_model_train/$PIPELINE_NAME/$METHOD/$RUN_NAME
LOGGING_DIR=$OUTER_DIR/logs/reward_model_train/$PIPELINE_NAME/$METHOD/$RUN_NAME
STATIC_ROLLOUTS_CACHE_PATH=$OUTER_DIR/data/static_test/cache/$PIPELINE_NAME.json

WANDB__SERVICE_WAIT=300 torchrun --master_port=$PORT --nnodes=1 --nproc_per_node=$NPROC_PER_NODES scripts/reward_model_train.py \
    --base_model_name $BASE_MODEL_NAME \
    --dataset $DATASET \
    --static_rollouts_path $STATIC_DS_SET \
    --dataset_format $DATASET_FORMAT \
    --hf_repo_or_local_dir $HF_REPO_OR_LOCAL_DIR \
    --pipeline_name $PIPELINE_NAME \
    --train_multi_head $TRAIN_MULTI_HEAD \
    --output_dir $OUTPUT_DIR \
    --logging_dir $LOGGING_DIR \
    --wandb_run_name RM-$RUN_NAME-$PIPELINE_NAME-$METHOD \
    --wandb_project $WANDB_PROJECT \
    --wandb_entity $WANDB_ENTITY \
    --per_device_train_batch_size $PER_DEVICE_TRAIN_BATCH_SIZE \
    --per_device_eval_batch_size $PER_DEVICE_EVAL_BATCH_SIZE \
    --gradient_accumulation_steps $GRADIENT_ACCUMULATION_STEPS \
    --learning_rate $LEARNING_RATE \
    --num_train_epochs $NUM_TRAIN_EPOCHS \
    --max_length $MAX_LENGTH \
    --logging_steps $LOGGING_STEPS \
    --eval_steps $EVAL_STEPS \
    --save_steps $SAVE_STEPS \
    --eval_strategy $EVAL_STRATEGY \
    --push_to_hub $PUSH_TO_HUB \
    --lora_r $LORA_R \
    --lora_alpha $LORA_ALPHA \
    --lora_dropout $LORA_DROPOUT \
    --eval_ratio $EVAL_RATIO \
    --report_to $REPORT_TO \
    --max_steps $MAX_STEPS \
    --save_steps $SAVE_STEPS \
    --save_total_limit $SAVE_TOTAL_LIMIT \
    --load_in_4bit $LOAD_IN_4BIT \
    --load_in_8bit $LOAD_IN_8BIT \
    --use_score_scaling $USE_SCORE_SCALING \
    --use_score_norm $USE_SCORE_NORM \
    --metric_for_best_model $METRIC_FOR_BEST_MODEL \
    --add_margin $ADD_MARGIN \
    --warmup_steps $WARMUP_STEPS \
    --use_lora $USE_LORA \
    --static_rollouts_cache_path $STATIC_ROLLOUTS_CACHE_PATH \
    --test_best_model_only $TEST_BEST_MODEL_ONLY \
    --save_model_per_module $SAVE_MODEL_PER_MODULE \
    --test_static_rollouts_per_module $TEST_STATIC_ROLLOUTS_PER_MODULE 
