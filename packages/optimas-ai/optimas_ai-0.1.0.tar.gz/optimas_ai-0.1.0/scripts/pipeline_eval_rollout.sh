# Usage: source scripts/pipeline_eval_rollout.sh <dataset>
# Parameters
DATASET=$1

# Load configurations
source scripts/config.sh
set_dataset_config $DATASET
echo "Dataset: $DATASET"
echo "Pipeline name: $PIPELINE_NAME"
echo "State dict path: $STATE_DICT_PATH"

# ================================================================

NUM_REPEAT=2
OPTIMIZE_PROMPT=False
OUTPUT_DIR=$OUTER_DIR/optim

# ================================================================
# ------- MODEL FROM REWARD_MODEL_TRAIN -------
# STATE_DICT_PATH=$OUTER_DIR/output/reward_model_train/hotpotqa_four_agents_pipeline/preference_scorer/official_multihead_bs32_2e-6/full-2632/state_dict.pth
# STATE_DICT_PATH=$OUTER_DIR/output_parth/reward_model_train/pubmed_pipeline/preference_scorer/parth_test/full-best/state_dict.pth

# STATE_DICT_PATH_FOR_SAMPLING=$OUTER_DIR/output_parth/reward_model_train/pubmed_pipeline/preference_scorer/parth_test/full-best/state_dict.pth
# STATE_DICT_PATH=$OUTER_DIR/output_parth/reward_model_train/pubmed_pipeline/preference_scorer/iterative_2_loaded_pipeline/full-best/state_dict.pth
# PIPELINE_STATE_DICT_PATH=$OUTER_DIR/output_parth/optim/pubmed/pubmed_pipeline/opro-preference_scorer-trainsize50-n10-repeat1/pipeline_state_dict.pth
# ================================================================
METHOD=preference_scorer
# ------------- FOR ROLLOUTS --------------
MODULES_TO_APPLY=all
# ================================================================
SAMPLE_SIZE=5
RUN_NAME=$METHOD-rollout-n$SAMPLE_SIZE-m_$MODULES_TO_APPLY-repeat$NUM_REPEAT-iter1-loaded-pipeline
FLAG=--reward_model_for_rollout

CUDA_VISIBLE_DEVICES=5 python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --sample_size $SAMPLE_SIZE \
    --modules_to_apply $MODULES_TO_APPLY \
    --num_repeat $NUM_REPEAT ${FLAG} \
    --state_dict_path $STATE_DICT_PATH \
    --lora_r $LORA_R \
    --lora_alpha $LORA_ALPHA \
    --lora_dropout $LORA_DROPOUT 
    # --pipeline_state_dict_path $PIPELINE_STATE_DICT_PATH \
    # --state_dict_path_for_sampling $STATE_DICT_PATH_FOR_SAMPLING



