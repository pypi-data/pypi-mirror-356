from pathlib import Path
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder
from scipy.stats import entropy


from .base import BaseSplitter
from ...utils.splitting import RareClassSafeSplitter


class StratifiedShuffleSplitter(BaseSplitter):
    """
    Stratified shuffle-based data splitter for classification tasks.

    This splitter maintains class distribution across splits by using
    stratified random sampling. It handles rare classes of 1 sample
    by putting it in the train split.

    Inputs
    ------
    - X : Feature matrix.
    - y : Target labels.

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
    name = "stratified-shuffle-split"

    def __init__(self):
        super().__init__()

    def _split_indices(self, X, y, n_splits=5, test_size=0.2, random_state=0):
        cv = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=random_state)
        cv = RareClassSafeSplitter(cv)
        splits = []
        for train_index, test_index in cv.split(X, y):
            splits.append((train_index, test_index))
        return splits
