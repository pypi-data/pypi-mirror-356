from pathlib import Path
from sklearn.model_selection import train_test_split
from scipy.stats import entropy
import numpy as np
import pandas as pd

from .base import BaseSplitter


def stratified_group_shuffle_split(
    groups, test_size=0.2, n_splits=1, random_state=None, n_bins=50
):
    """
    Yields train/test indices with group integrity and stratification based on binned group sizes.

    Parameters
    ----------
    groups : array-like, shape (n_samples,)
    test_size : float
    n_splits : int
    random_state : int or None
    n_bins : int, optional
        Number of bins to discretize group sizes into for stratification
    """
    df = pd.DataFrame({"group": groups})
    group_sizes = df.groupby("group").size().rename("group_size").reset_index()

    # Bin group sizes into discrete bins for stratification
    try:
        group_sizes["stratify_bin"] = pd.qcut(group_sizes["group_size"], q=n_bins, duplicates="drop")
    except ValueError:
        # Fallback: if not enough unique group sizes, use uniform bins
        group_sizes["stratify_bin"] = pd.cut(group_sizes["group_size"], bins=min(n_bins, group_sizes["group_size"].nunique()))

    rng = np.random.RandomState(random_state)
    for _ in range(n_splits):
        train_groups, test_groups = train_test_split(
            group_sizes["group"],
            test_size=test_size,
            stratify=group_sizes["stratify_bin"],
            random_state=rng.randint(0, 1e6)
        )

        train_mask = np.isin(np.array(groups), train_groups)
        test_mask = np.isin(np.array(groups), test_groups)

        train_idx = np.where(train_mask)[0]
        test_idx = np.where(test_mask)[0]

        yield train_idx, test_idx


class StratifiedGroupShuffleSplitter(BaseSplitter):
    """
    Stratified group shuffle-based splitter for record linkage and group-based tasks.

    This splitter preserves group integrity while maintaining a stratified distribution
    of group sizes across splits. It is especially useful when working with grouped data
    such as entities, patients, or records with known duplicates.

    Inputs
    ------
    - X : Feature matrix.
    - y : Group labels indicating entity membership for each sample.

    Outputs
    -------
    - splits : List of masks for each fold.

    Parameters
    ----------
    n_splits : int, default=5
        Number of re-shuffling and splitting iterations.
    test_size : float, default=0.2
        Proportion of the dataset to include in the test split.
    random_state : int, default=0
        Controls the randomness of the train/test splits.

    """
    name = "stratified-group-shuffle-split"

    def __init__(self):
        super().__init__()
        self.metric_to_optimize = "roc_auc"
        
    def _split_indices(self, X, y, n_splits=5, test_size=0.2, random_state=0):
        cv = stratified_group_shuffle_split(y, n_splits=n_splits, test_size=test_size, random_state=random_state)
        splits = []
        for train_index, test_index in cv:
            splits.append((train_index, test_index))
        return splits

   