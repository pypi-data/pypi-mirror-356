import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, PowerTransformer, OneHotEncoder, TargetEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from .base import Preprocessing
from ...workflow import Field


def fix_categoricals(df: pd.DataFrame, categorical_features: list) -> pd.DataFrame:
    for col in categorical_features:
        if col in df.columns:
            df[col] = df[col].astype('category')

            categories = df[col].cat.categories

            try:
                # Try converting categories to numeric
                numeric = pd.to_numeric(categories, errors="raise")

                # Check if all are integer-like and no collision
                if np.allclose(numeric, numeric.astype(int)):
                    if len(np.unique(numeric.astype(int))) == len(numeric):
                        df[col] = df[col].astype(int)
                    else:
                        df[col] = df[col].astype(str)
                else:
                    df[col] = df[col].astype(str)

            except Exception:
                df[col] = df[col].astype(str)

    return df


class CategoricalPreprocessor(Preprocessing):
    """
    Preprocessing step for categorical features in tabular data.

    This step applies configurable encoding and imputation strategies to categorical columns.
    It can optionally use the target variable for supervised encoders such as target encoding.
    Date and high-cardinality text features are automatically excluded from transformation
    and passed through unchanged.

    Parameters
    ----------
    categorical_encoding : {'onehot', 'target', 'integer', 'none'}, default='onehot'
        Encoding method used for categorical features.

    categorical_imputation : str, default='most_frequent'
        Strategy used to impute missing values in categorical columns.

    Inputs
    ------
    X : pandas.DataFrame
        Input feature table containing raw categorical, numerical, and other columns.

    y : array-like of shape (n_samples,)
        Target variable, required for encoders such as target encoding.

    categorical_features : list of str, optional
        Names of columns to treat as categorical. If not provided, they are inferred automatically.

    Outputs
    -------
    X : pandas.DataFrame
        Transformed dataset with encoded categorical features and untouched passthrough columns (e.g., text, date).
    """
    name = "categorical-preprocessing"

    inputs = [
        Field('X', 'Input features of the dataset'),
        Field('y', 'Target variable to predict'),
        Field('categorical_features', 'Names of the categorical feature columns', required=False),
    ]
    outputs = [
        Field('X', 'Preprocessed input features'),
    ]
    params = [
        Field('categorical_encoding', 'Encoding method for categorical features [onehot, target, integer, none]', default='onehot'),
        Field('categorical_imputation', 'Imputation strategy for missing categorical values', default='most_frequent'),        
    ]


    def _build_pipeline(self, X, y, cat_feats):

        # Categorical pipeline
        cat_pipeline = []
        if self.categorical_imputation is not None:
            cat_pipeline.append(('imputer', SimpleImputer(strategy=self.categorical_imputation)))
        if self.categorical_encoding == "onehot":
            cat_pipeline.append(("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)))
        elif self.categorical_encoding == "target":
            cat_pipeline.append(("encoder", TargetEncoder()))            
        elif self.categorical_encoding == "integer":
            cat_pipeline.append(("encoder", OrdinalEncoder()))            
        elif self.categorical_encoding == "none":
            pass
        else:
            raise ValueError(f"Unsupported categorical encoding: {self.categorical_encoding}")

        self.feature_structure = {"cat": cat_feats}
        pipeline = ColumnTransformer(
            transformers=[
                ("cat", Pipeline(cat_pipeline), cat_feats),
            ],
            remainder="drop",  # passthrough handled manually
            verbose_feature_names_out=False
        )

        pipeline.fit(X, y)
        return pipeline

    def _execute(self, inputs: dict):
        X = inputs["X"]
        y = inputs["y"]
        categorical_features = inputs['categorical_features']

        if not categorical_features:
            self.output('X', X)
            return

        pipeline = self._build_pipeline(X, y, categorical_features)
        passthrough = set(X.columns) - set(categorical_features)

        X_transformed = pipeline.transform(X)
        columns = pipeline.get_feature_names_out()
        df_transformed = pd.DataFrame(X_transformed, columns=columns, index=X.index)

        # Restore categorical dtype if using integer or no encoding
        if self.categorical_encoding in ['integer', 'none']:
            df_transformed = fix_categoricals(df_transformed, categorical_features)

        # Reattach untouched passthrough columns
        df_final = pd.concat([df_transformed, X[list(passthrough)]], axis=1)
        print(df_final.dtypes)

        self.output("X", df_final)
