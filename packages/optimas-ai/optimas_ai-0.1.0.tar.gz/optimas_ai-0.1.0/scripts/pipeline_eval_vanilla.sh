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
NUM_REPEAT=3
RUN_NAME=single-repeat$NUM_REPEAT


CUDA_VISIBLE_DEVICES=1 python scripts/pipeline_eval.py \
    --run_name $RUN_NAME \
    --dataset $DATASET \
    --pipeline_name $PIPELINE_NAME \
    --output_dir $OUTPUT_DIR \
    --num_repeat $NUM_REPEAT \
    --max_eval_workers 1 \
    --lora_r $LORA_R \
    --lora_alpha $LORA_ALPHA \
    --lora_dropout $LORA_DROPOUT 

