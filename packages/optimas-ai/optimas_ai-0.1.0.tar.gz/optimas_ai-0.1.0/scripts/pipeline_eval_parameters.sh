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
PER_MODULE_TRAIN_SIZE=50
METHOD=preference_scorer
# ================================================================
# ------------- FOR PROMPT OPTIMIZATION --------------
NUM_CANDIDATES=20
PROMPT_OPTIMIZER=opro
RUN_NAME=$PROMPT_OPTIMIZER-$METHOD-trainsize$PER_MODULE_TRAIN_SIZE-n$NUM_CANDIDATES-repeat$NUM_REPEAT
FLAG=--reward_model_for_optimization
MODULES_TO_APPLY=unit_test_generator

# ----------- UNCOMMENT FOR VANILLA EVALUATION ----------------
# RUN_NAME=original-repeat$NUM_REPEAT
# FLAG= 
# --------- UNCOMMENT FOR DEBUGGING
# PER_MODULE_TRAIN_SIZE=5
# NUM_CANDIDATES=5

CUDA_VISIBLE_DEVICES=6 python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --state_dict_path $STATE_DICT_PATH \
    --per_module_train_size $PER_MODULE_TRAIN_SIZE \
    --prompt_optimizer $PROMPT_OPTIMIZER \
    --num_prompt_candidates $NUM_CANDIDATES \
    --modules_to_apply $MODULES_TO_APPLY \
    --hf_repo_or_local_dir $HF_REPO_OR_LOCAL_DIR \
    --num_repeat $NUM_REPEAT ${FLAG} \
    --lora_r $LORA_R \
    --lora_alpha $LORA_ALPHA \
    --lora_dropout $LORA_DROPOUT 

