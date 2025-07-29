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

# --------------------------
# METHOD=preference_modular_model_prior
# METHOD=abs_value_llm_judge
METHOD=preference_scorer
# --------------------------
TRAINSIZE=1000

python scripts/trainset_generate.py \
    --pipeline $PIPELINE_NAME \
    --method $METHOD \
    --dataset $DATASET \
    --train_size $TRAINSIZE \
    --max_workers 4 \
    --num_per_instance 1 \
    --num_repeat_samples 4 \
    --num_forward_estimate 4 \
    --push_to_hub 

