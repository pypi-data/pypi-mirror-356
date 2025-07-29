import numpy as np
import pandas as pd

from ...workflow import Step, Field


class PairFeatureGenerator(Step):
    """
    Feature generator for sample pairs.

    This step takes a feature matrix `X` and a list of index pairs, and generates
    new features for each pair. For each pair `(i, j)`, it computes:
    - `X[i]` (original features of the first sample)
    - `X[j]` (original features of the second sample)
    - `(X[i] - X[j]) ** 2` (squared difference)
    - `X[i] * X[j]` (element-wise product)

    These components are concatenated along the feature axis to produce a combined
    feature representation for the pair.

    Inputs
    ------
    X_pairs : np.ndarray of shape (n_samples, 2 * n_features)
        Pairs of concatenated samples.

    Outputs
    -------
    X_pairs : np.ndarray of shape (n_pairs, 4 * n_features)
        The combined features for all input pairs, stacked vertically.
    """
    name = 'pair-feature-generator'
    inputs = [Field('X_pairs', 'Pairs of concatenated input features')]
    outputs = [
        Field('X_pairs', 'Pairs of features with difference and product augmentations'),
        Field('categorical_features_pairs', 'Column names of categorical features'),
    ]

    def _execute(self, inputs: dict):
        """
        Generate features for input index pairs.

        For each pair of indices `(i, j)` in `index_pairs`, this method retrieves
        the corresponding rows from `X` (i.e., `X[i]` and `X[j]`) and computes:

        - The original features of the first sample (`X[i]`)
        - The original features of the second sample (`X[j]`)
        - The squared difference: `(X[i] - X[j]) ** 2`
        - The element-wise product: `X[i] * X[j]`

        These four components are concatenated horizontally to form a new feature
        vector for the pair. All vectors are stacked vertically to create the
        output array.

        Parameters
        ----------
        inputs : dict
            Dictionary containing:
            - 'X_pairs': np.ndarray of shape (n_samples, n_features)

        Outputs
        -------
        X_pairs : np.ndarray of shape (n_pairs, 4 * n_features)
            The transformed features for all index pairs.
        """
        X = inputs['X_pairs']
        n_cols = X.shape[1]
        assert n_cols % 2 == 0, "Number of columns must be even to split in two."
        mid = n_cols // 2

        colnames = X.columns.tolist()
        colnames1 = colnames[:mid]

        X1 = X.iloc[:, :mid]
        X2 = X.iloc[:, mid:]

        diff = (X1.values - X2.values) ** 2
        diff_df = pd.DataFrame(diff, columns=[f"{col}_diff2" for col in colnames1], index=X.index)

        product = X1.values * X2.values
        product_df = pd.DataFrame(product, columns=[f"{col}_prod" for col in colnames1], index=X.index)

        result_df = pd.concat([X1, X2, diff_df, product_df], axis=1)
        self.output("X_pairs", result_df)
        self.output("categorical_features_pairs", [])
