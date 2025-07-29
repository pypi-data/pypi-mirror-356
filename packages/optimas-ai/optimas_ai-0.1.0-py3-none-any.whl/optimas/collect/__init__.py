
from .preference_scorer import generate_trainset_preference_scorer

def generate_reward_model_trainset(method: str, pipeline, dataset, **kwargs):
    if method == 'preference_scorer':
        return generate_trainset_preference_scorer(pipeline, dataset, **kwargs)
    else:
        raise ValueError(f"Method {method} not supported.")