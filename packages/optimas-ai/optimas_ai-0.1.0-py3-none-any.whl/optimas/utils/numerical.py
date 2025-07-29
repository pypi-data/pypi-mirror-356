import numpy as np


def normalization(scores): 
    """
    Normalize the scores to [0, 1] range.
    """
    scores = np.array(scores)
    mean, std = np.mean(scores), np.std(scores) + np.finfo(scores.dtype).eps
    return ((scores - mean) / std).tolist()