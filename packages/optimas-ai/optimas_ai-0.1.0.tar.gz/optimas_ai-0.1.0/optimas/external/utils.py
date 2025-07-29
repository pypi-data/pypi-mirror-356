"""
Utility functions for TRL compatibility with older versions.
This module provides implementations of functions that might not be available in older TRL versions.
"""

import os
import warnings
from typing import Optional, Union, Any, Dict, List

# Check if comet_ml is available
try:
    import comet_ml
    _has_comet_ml = True
except ImportError:
    _has_comet_ml = False


def generate_model_card(
    base_model: Optional[str] = None,
    model_name: Optional[str] = None,
    hub_model_id: Optional[str] = None,
    dataset_name: Optional[str] = None,
    tags: Optional[Union[str, List[str]]] = None,
    wandb_url: Optional[str] = None,
    comet_url: Optional[str] = None,
    trainer_name: str = "Reward"
):
    """
    Generate a model card for the trained model.

    Args:
        base_model (`str`, *optional*): Base model name or path
        model_name (`str`, *optional*): Name of the model
        hub_model_id (`str`, *optional*): Hub model ID
        dataset_name (`str`, *optional*): Name of the dataset used for training
        tags (`list[str]`, *optional*): Tags to be associated with the model card
        wandb_url (`str`, *optional*): URL of the W&B run
        comet_url (`str`, *optional*): URL of the Comet ML experiment
        trainer_name (`str`, *optional*): Name of the trainer

    Returns:
        `ModelCard`: A ModelCard object containing the model card information
    """
    from transformers.modelcard import ModelCard

    # Default values
    tags = tags or []
    if isinstance(tags, str):
        tags = [tags]

    model_name = model_name or hub_model_id or f"{trainer_name} Model"

    # Create model card content
    model_card_content = f"""
# {model_name}

This is a model trained with TRL's `{trainer_name}Trainer`.

## Model Details

* **Model Type:** {trainer_name} Model
"""

    if base_model:
        model_card_content += f"* **Base Model:** {base_model}\n"

    if dataset_name:
        model_card_content += f"* **Training Dataset:** {dataset_name}\n"

    # Add links section if there are any URLs
    if any([wandb_url, comet_url]):
        model_card_content += "\n## Training and Evaluation\n\n"

        if wandb_url:
            model_card_content += f"* **Weights & Biases:** [Run]({wandb_url})\n"

        if comet_url:
            model_card_content += f"* **Comet ML:** [Experiment]({comet_url})\n"

    # Create ModelCard object
    return ModelCard(model_card_content, card_data={"tags": tags})


def get_comet_experiment_url() -> Optional[str]:
    """
    Get the URL of the current Comet ML experiment.

    Returns:
        str or None: URL of the current Comet ML experiment or None if not available.
    """
    if not _has_comet_ml:
        return None

    try:
        experiment = comet_ml.config.get_global_experiment()
        if experiment is not None:
            return experiment.url
    except Exception as e:
        warnings.warn(f"Failed to get Comet ML experiment URL: {e}")

    return None


def log_table_to_comet_experiment(
    name: str,
    table: Any,
    experiment: Optional["comet_ml.Experiment"] = None,
    table_type: str = "dataframe"
):
    """
    Log a table to a Comet ML experiment.

    Args:
        name (str): Name of the table.
        table (Any): Table to log, can be a DataFrame or other tabular data.
        experiment (comet_ml.Experiment, optional): Comet ML experiment to log to.
            If None, will try to get the global experiment.
        table_type (str, optional): Type of table. Default is "dataframe".
    """
    if not _has_comet_ml:
        warnings.warn("Comet ML is not installed. Cannot log table.")
        return

    try:
        if experiment is None:
            experiment = comet_ml.config.get_global_experiment()

        if experiment is None:
            warnings.warn("No active Comet ML experiment found.")
            return

        # Log the table based on the table_type
        if table_type == "dataframe":
            experiment.log_table(name, table)
        else:
            warnings.warn(f"Unsupported table type: {table_type}")
    except Exception as e:
        warnings.warn(f"Failed to log table to Comet ML: {e}")


