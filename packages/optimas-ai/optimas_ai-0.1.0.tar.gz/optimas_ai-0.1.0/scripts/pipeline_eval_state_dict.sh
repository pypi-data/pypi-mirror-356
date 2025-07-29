# Usage: source scripts/pipeline_eval_state_dict.sh <dataset>
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


NUM_REPEAT=3
OUTPUT_DIR=$OUTER_DIR/optim
# ================================================================
# PIPELINE_STATE_DICT_PATH=/dfs/project/kgrlm/multiagent_reward/trl/on_policy/hotpotqa/hotpotqa_four_agents_pipeline/run_global_answer_gen_only-iter3-valsize20-trainsize50-searchsize50-inputsize20-repeat1/final_optimized_pipeline.pth
# STATE_DICT_PATH=$OUTER_DIR/output/reward_model_train/hotpotqa_four_agents_pipeline/preference_scorer/official_multihead_bs32_2e-6/full-2632/state_dict.pth
# STATE_DICT_PATH=$OUTER_DIR/optim/hotpotqa/hotpotqa_four_agents_pipeline/opro-preference_scorer-trainsize100-n20-repeat3/pipeline_state_dict.pth

PIPELINE_STATE_DICT_PATH="/dfs/project/kgrlm/shirwu/optimas/github/examples/pipelines/bigcodebench/checkpoints/train_size=20/combined_textgrad_prompts_consistent.pth"
#/dfs/project/kgrlm/multiagent_reward/trl/on_policy/hotpotqa/hotpotqa_four_agents_pipeline/run_global-iter100-valsize20-trainsize20-searchsize20-inputsize20-repeat1/final_optimized_pipeline.pth
RUN_NAME=combined_textgrad_prompts_consistent
#run_global-iter100-valsize20-trainsize20-searchsize20-inputsize20-repeat1


CUDA_VISIBLE_DEVICES=0 python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --num_repeat $NUM_REPEAT \
    --lora_r $LORA_R \
    --lora_alpha $LORA_ALPHA \
    --lora_dropout $LORA_DROPOUT \
    --pipeline_state_dict_path $PIPELINE_STATE_DICT_PATH 
    # \
    # --state_dict_path $STATE_DICT_PATH \

