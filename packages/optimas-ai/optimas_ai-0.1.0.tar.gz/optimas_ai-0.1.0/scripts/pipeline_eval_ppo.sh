# Serve the base vllm model in another shell
# export VLLM_ALLOW_RUNTIME_LORA_UPDATING=True
# CUDA_VISIBLE_DEVICES=5 python -m vllm.entrypoints.openai.api_server     --trust-remote-code --enable-lora   --port 8001  --host localhost   --max-lora-rank 32     --max-loras 2     --model /dfs/project/kgrlm/multiagent_reward/trl/local_lm/qwen-1_5b/base

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


NUM_REPEAT=1
OUTPUT_DIR=/dfs/project/kgrlm/multiagent_reward/trl/local_lm/qwen-1_5b

# ======================== FOR PROMPT OPTIMIZATION ========================================
RUN_NAME=/dfs/project/kgrlm/multiagent_reward/trl/local_lm/qwen-1_5b/amazon/amazon_next_item_selection_local_pipeline/PPO-trainsize400-official-final-0.25epoch-new-reward-3-384-6
NUM_CANDIDATES=20
PER_MODULE_TRAIN_SIZE=50
PROMPT_OPTIMIZER=opro
# ======================== FOR PPO========================================
PPO_BASE_MODEL_NAME=Qwen/Qwen2.5-1.5B-Instruct
MODULES_TO_APPLY=all
# MODULES_TO_APPLY=unit_test_generator

export VLLM_HOST=localhost
export VLLM_PORT=8001
export VLLM_BASE_MODEL=/dfs/project/kgrlm/multiagent_reward/trl/local_lm/qwen-1_5b/base

# Specify the path to the lora adapters here
SESSION_ADAPTER_NAME=session_lora
SESSION_ADAPTER_PATH=/dfs/project/kgrlm/multiagent_reward/trl/local_lm/qwen-1_5b/amazon/amazon_next_item_selection_local_pipeline/PPO-trainsize400-official-final-0.25epoch-new-reward-3-384-5/ppo/session_analyzer/step_3

PROFILER_ADAPTER_NAME=profiler_lora
PROFILER_ADAPTER_PATH=/dfs/project/kgrlm/multiagent_reward/trl/local_lm/qwen-1_5b/amazon/amazon_next_item_selection_local_pipeline/PPO-trainsize400-official-final-0.25epoch-new-reward-3-384-5/ppo/candidate_profiler/step_3


CUDA_VISIBLE_DEVICES=7 python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --sample_size 1 \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --state_dict_path $STATE_DICT_PATH \
    --modules_to_apply $MODULES_TO_APPLY \
    --hf_repo_or_local_dir $HF_REPO_OR_LOCAL_DIR \
    --num_repeat $NUM_REPEAT ${FLAG} \
    --weight_optimizer PPO \
    --ppo_epochs 0 \
    --ppo_batch_size 16 \
    --ppo_base_model_name $PPO_BASE_MODEL_NAME \
    --session_adapter session_lora \
    --profiler_adapter profiler_lora \
    --mode val\
    --val_name step96-trial1\
    --max_sample_workers 1 \
    --max_eval_workers 16 \
    --session_adapter $SESSION_ADAPTER_NAME \
    --session_adapter_path $SESSION_ADAPTER_PATH \
    --profiler_adapter $PROFILER_ADAPTER_NAME \
    --profiler_adapter_path $PROFILER_ADAPTER_PATH
