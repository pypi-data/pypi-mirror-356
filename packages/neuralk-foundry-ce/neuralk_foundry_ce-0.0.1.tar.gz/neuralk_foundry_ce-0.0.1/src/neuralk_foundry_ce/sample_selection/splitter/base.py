import numpy as np
import pandas as pd
from pathlib import Path

from ...workflow import Step, Field
from ...utils.splitting import Split


class BaseSplitter(Step):
    """
    Base class for splitting steps.

    Parameters
    ----------
    name : str
        Name of the task.
    """
    name = 'task'
    inputs = [
        Field('X', 'Input features of the dataset'),
        Field('y', 'Target variable to predict'),
        Field('fold_index', 'Index of the train/test split', default=0, required=False),
    ]
    outputs = [
        Field('splits', 'Masks for train, validation, and test sets'),
    ]

    def _split_indices(self, X, y, n_splits=5, test_size=0.2, random_state=0):
        raise NotImplementedError("This method should be implemented in subclasses to provide a cross-validation splitter.")
    
    def _get_metrics(self, X, y):

        num_rows, num_cols = X.shape
        num_cat = X.select_dtypes(include=['object', 'category']).shape[1]
        num_num = X.select_dtypes(include=[np.number]).shape[1]
        num_bool = X.select_dtypes(include=['bool']).shape[1]
        num_datetime = X.select_dtypes(include=['datetime']).shape[1]
        
        missing_ratio = X.isnull().mean().mean()
        cols_with_missing = X.isnull().any().sum()
        
        unique_counts = X.nunique(dropna=False)
        high_cardinality_cols = (unique_counts > 50).sum()
        constant_cols = (unique_counts <= 1).sum()

        return {
            'num_samples': num_rows,
            'num_columns': num_cols,
            'num_categorical': num_cat,
            'num_numerical': num_num,
            'num_boolean': num_bool,
            'num_datetime': num_datetime,
            'missing_values_ratio': missing_ratio,
            'columns_with_missing': cols_with_missing,
            'high_cardinality_columns': high_cardinality_cols,
            'constant_columns': constant_cols,
        }


    def get_cv_for_data(self, X: pd.DataFrame, y: np.ndarray):
        """Generate and save cross-validation splits for the dataset.

        Parameters
        ----------
        X : pd.DataFrame
            Feature matrix.

        y : np.array
            Target labels.

        Returns
        -------
        list of dict
            A list of dictionaries containing train, validation, and test splits.
        """

        fold_masks = []

        splits = self._split_indices(X, y, random_state=0)
        for i, (learn_index, test_index) in enumerate(splits):
            mask = np.full(len(X), Split.TRAIN, dtype=np.int8)
            mask[test_index] = Split.TEST

            # Further split learn_index into train/val
            X_learn, y_learn = X.loc[learn_index], y[learn_index]
            learn_splits = self._split_indices(
                X_learn, y_learn, n_splits=self.n_splits, test_size=self.test_size,
                random_state=self.random_seed)

            iter_masks = []

            for train_index, val_index in learn_splits:
                inner_mask = mask.copy()
                inner_mask[learn_index[train_index]] = Split.TRAIN
                inner_mask[learn_index[val_index]] = Split.VAL
                iter_masks.append(inner_mask.tolist())
            fold_masks.append(iter_masks)

        return fold_masks
    
    def _execute(self, inputs, data_cache_dir: str=None,
                 n_splits: int=5, test_size: float=0.2, random_seed: int=0):
        if data_cache_dir is not None and isinstance(data_cache_dir, str):
            data_cache_dir = Path(data_cache_dir)

        self.n_splits = n_splits
        self.test_size = test_size
        self.random_seed = random_seed
        
        X, y, fold_index = inputs['X'], inputs['y'], inputs['fold_index']
        splits = self.get_cv_for_data(X, y)

        self.output('splits', splits[fold_index])

        metrics = self._get_metrics(X, y)
        for metric, value in metrics.items():
            self.log_metric(metric, value)


