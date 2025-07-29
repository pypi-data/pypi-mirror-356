# Usage: source scripts/on_policy_optim.sh <dataset>
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

# ============================
RUN_NAME=on_policy_ppo_integrated
# _global
#_local_fresh
USE_GLOB=--global_hyper_param_search
# ============================
OUTPUT_DIR=$OUTER_DIR/on_policy_parth
ITERATIONS=100
MAX_SAMPLE_WORKERS=4
NUM_REPEAT=1
# USE_REPLAY_BUFFER=TRUE
REPLAY_BUFFER_SIZE=200

# ========== OPTIMIZATION MODULE USING RM ==================
PER_MODULE_TRAIN_SIZE=300
PER_MODULE_SEARCH_SIZE=$PER_MODULE_TRAIN_SIZE
NUM_PROMPT_CANDIDATES=3

# ================ TRAIN RM ============
PER_ITERATION_INPUT_SIZE=50
PER_ITERATION_RM_TRAIN_SIZE=-1
VAL_SIZE=20

# ================ PPO Configuration ============
PPO_EPOCHS=3
PPO_TRAIN_STEPS=3
PPO_BATCH_SIZE=16
PPO_LEARNING_RATE=1e-4
PPO_SAVE_EPOCH_RATIO=0.25
PPO_BASE_MODEL_NAME=Qwen/Qwen2.5-1.5B-Instruct

# ================ vLLM Configuration ============
export VLLM_HOST=localhost
export VLLM_PORT=8001
export VLLM_ALLOW_RUNTIME_LORA_UPDATING=True

# # Set the base model path for vLLM
export VLLM_BASE_MODEL=/dfs/project/kgrlm/multiagent_reward/trl/local_lm/qwen-1_5b/base

RUN_NAME=$RUN_NAME-iter$ITERATIONS-valsize$VAL_SIZE-trainsize$PER_MODULE_TRAIN_SIZE-searchsize$PER_MODULE_SEARCH_SIZE-inputsize$PER_ITERATION_INPUT_SIZE-repeat$NUM_REPEAT-ppo$PPO_EPOCHS

# echo "Starting vLLM server in background..."
# echo "Base model: $VLLM_BASE_MODEL"
# echo "Host: $VLLM_HOST"
# echo "Port: $VLLM_PORT"

# # Start vLLM server in background if not already running
# if ! nc -z $VLLM_HOST $VLLM_PORT; then
#     echo "Starting vLLM server..."
#     CUDA_VISIBLE_DEVICES=5 python -m vllm.entrypoints.openai.api_server \
#         --trust-remote-code \
#         --enable-lora \
#         --port $VLLM_PORT \
#         --host $VLLM_HOST \
#         --max-lora-rank 32 \
#         --max-loras 4 \
#         --model $VLLM_BASE_MODEL &

#     VLLM_PID=$!
#     echo "vLLM server started with PID: $VLLM_PID"

#     # Wait for server to be ready
#     echo "Waiting for vLLM server to be ready..."
#     for i in {1..60}; do
#         if nc -z $VLLM_HOST $VLLM_PORT; then
#             echo "vLLM server is ready!"
#             break
#         fi
#         echo "Waiting... ($i/60)"
#         sleep 5
#     done

#     if ! nc -z $VLLM_HOST $VLLM_PORT; then
#         echo "Error: vLLM server failed to start or is not responding"
#         exit 1
#     fi
# else
#     echo "vLLM server is already running on $VLLM_HOST:$VLLM_PORT"
#     VLLM_PID=""
# fi

# # Function to cleanup on exit
# cleanup() {
#     echo "Cleaning up..."
#     if [ ! -z "$VLLM_PID" ]; then
#         echo "Stopping vLLM server (PID: $VLLM_PID)..."
#         kill $VLLM_PID 2>/dev/null || true
#         wait $VLLM_PID 2>/dev/null || true
#     fi
# }

# # Set trap to cleanup on script exit
# trap cleanup EXIT

echo "Starting on-policy optimization..."

CUDA_VISIBLE_DEVICES=7 python scripts/on_policy_optim.py \
    --dataset $DATASET \
    --pipeline $PIPELINE_NAME \
    --iterations $ITERATIONS \
    --per_iteration_input_size $PER_ITERATION_INPUT_SIZE \
    --per_iteration_rm_train_size $PER_ITERATION_RM_TRAIN_SIZE \
    --per_module_search_size $PER_MODULE_SEARCH_SIZE \
    --per_module_train_size $PER_MODULE_TRAIN_SIZE \
    --num_prompt_candidates $NUM_PROMPT_CANDIDATES \
    --output_dir $OUTPUT_DIR \
    --state_dict_path $STATE_DICT_PATH \
    --preference_dataset $HF_REPO_OR_LOCAL_DIR \
    --lora_r $LORA_R \
    --lora_alpha $LORA_ALPHA \
    --lora_dropout $LORA_DROPOUT \
    --max_sample_workers $MAX_SAMPLE_WORKERS \
    --val_size $VAL_SIZE \
    --num_repeat $NUM_REPEAT \
    --run_name $RUN_NAME \
    --vllm_host $VLLM_HOST \
    --vllm_port $VLLM_PORT \
    --use_replay_buffer \
    --replay_buffer_size $REPLAY_BUFFER_SIZE \
    --weight_optimizer ppo \
    --ppo_epochs $PPO_EPOCHS \
    --ppo_train_steps $PPO_TRAIN_STEPS \
    --ppo_batch_size $PPO_BATCH_SIZE \
    --ppo_learning_rate $PPO_LEARNING_RATE \
    --ppo_save_epoch_ratio $PPO_SAVE_EPOCH_RATIO \
    --ppo_base_model_name $PPO_BASE_MODEL_NAME \
    $USE_GLOB

echo "On-policy optimization completed!"
