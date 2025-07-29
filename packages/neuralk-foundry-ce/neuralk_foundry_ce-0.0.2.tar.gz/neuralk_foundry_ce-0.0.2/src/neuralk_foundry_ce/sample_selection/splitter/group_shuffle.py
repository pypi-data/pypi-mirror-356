from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit
from scipy.stats import entropy
import numpy as np

from .base import BaseSplitter


class GroupShuffleSplitter(BaseSplitter):
    """
    Group shuffle-based splitter for record linkage and grouped data tasks.

    This splitter ensures that all samples from the same group are assigned to the same
    split (train or test), without enforcing stratification over group sizes. It is useful
    for scenarios where group leakage must be avoided, such as deduplication or entity resolution.

    Inputs
    ------
    - X : Feature matrix.
    - y : Group labels indicating entity membership for each sample.

    Outputs
    -------
    - splits : List of (train_index, test_index) tuples for each fold.

    Parameters
    ----------
    n_splits : int, default=5
        Number of re-shuffling and splitting iterations.
    test_size : float, default=0.2
        Proportion of the dataset to include in the test split.
    random_state : int, default=0
        Controls the randomness of the train/test splits.
    """
    name = "group-shuffle-split"

    def __init__(self):
        super().__init__()
        self.metric_to_optimize = "roc_auc"
        
    def _split_indices(self, X, y, n_splits=5, test_size=0.2, random_state=0):
        cv = GroupShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=random_state)
        splits = []
        for train_index, test_index in cv.split(X, y, y):
            splits.append((train_index, test_index))
        return splits