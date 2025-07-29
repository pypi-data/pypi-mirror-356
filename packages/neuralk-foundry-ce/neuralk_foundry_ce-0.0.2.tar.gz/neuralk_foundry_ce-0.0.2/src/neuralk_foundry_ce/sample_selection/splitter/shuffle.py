from pathlib import Path
import numpy as np
from sklearn.model_selection import ShuffleSplit
from scipy.stats import entropy


from .base import BaseSplitter


class ShuffleSplitter(BaseSplitter):
    """
    Shuffle-based data splitter for train/test evaluation.

    This splitter randomly shuffles and splits the dataset into train and test sets,
    repeating the process for multiple splits. It is suitable for both classification
    and regression tasks when stratification is not required.

    Inputs
    ------
    - X : Feature matrix.
    - y : Target labels.

    Outputs
    -------
    - splits : List of masks for each fold.

    Parameters
    ----------
    n_splits : int, default=5
        Number of re-shuffling & splitting iterations.
    test_size : float, default=0.2
        Proportion of the dataset to include in the test split.
    random_state : int, default=0
        Controls the randomness of the training and testing indices produced.

    Notes
    -----
    This splitter wraps scikit-learn’s `ShuffleSplit` strategy.
    Target labels `y` are automatically forwarded for downstream use.
    """    
    name = "shuffle-split"

    def __init__(self):
        super().__init__()

    def _split_indices(self, X, y, n_splits=5, test_size=0.2, random_state=0):
        cv = ShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=random_state)
        splits = []
        for train_index, test_index in cv.split(X, y):
            splits.append((train_index, test_index))
        return splits
