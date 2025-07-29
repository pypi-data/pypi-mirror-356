import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from .base import Preprocessing
from ...workflow import Field


class NumericalPreprocessor(Preprocessing):
    """
    Preprocessing step for tabular data with safe handling of datetimes and free-text.

    Applies configurable transformations to numerical and categorical columns,
    automatically skipping datetime and high-cardinality text columns. Skipped
    columns are passed through untouched.

    Inputs
    ------
    X : pd.DataFrame
        Raw input features.
    y : array-like
        Target values (used for supervised encoders like target encoding).

    Outputs
    -------
    X : pd.DataFrame
        Fully transformed DataFrame with flat column names and original passthrough columns.
    """
    name = "numerical-preprocessing"

    inputs = [
        Field('X', 'Input features of the dataset'),
        Field('numerical_features', 'Names of the numerical feature columns'),
    ]
    outputs = [
        Field('X', 'Preprocessed input features'),
    ]
    params = [
        Field('numerical_encoding', 'Encoding method for numerical features [standard, power, none]', default='standard'),
        Field('numerical_imputation', 'Imputation strategy for missing numerical values', default='mean'),
    ]

    def _build_pipeline(self, X, num_feats):
        # Numerical pipeline
        num_pipeline = []
        if self.numerical_imputation is not None:
            num_pipeline.append(('imputer', SimpleImputer(strategy=self.numerical_imputation)))

        if self.numerical_encoding == "standard":
            num_pipeline.append(("scaler", StandardScaler()))
        elif self.numerical_encoding == "power":
            num_pipeline.append(("scaler", PowerTransformer()))
        elif self.numerical_encoding == "none":
            pass
        else:
            raise ValueError(f"Unsupported numerical encoding: {self.numerical_encoding}")

        self.feature_structure = {"num": num_feats}
        pipeline = Pipeline(num_pipeline)
        pipeline.fit(X[num_feats])
        return pipeline


    def _execute(self, inputs: dict):
        X = inputs["X"]
        num_feats = inputs["numerical_features"]
        passthrough_feats = [col for col in X.columns if col not in num_feats]

        if not num_feats:
            self.output("X", X)
            return

        pipeline = self._build_pipeline(X, num_feats)

        # Transform numerical features
        X_num = pipeline.transform(X[num_feats])
        X_num = pd.DataFrame(X_num, columns=pipeline.get_feature_names_out(), index=X.index)
        X_num = X_num.astype(np.float64)

        # Concatenate with untouched passthrough features
        X_passthrough = X[passthrough_feats]
        df_transformed = pd.concat([X_num, X_passthrough], axis=1)

        self.output("X", df_transformed)
