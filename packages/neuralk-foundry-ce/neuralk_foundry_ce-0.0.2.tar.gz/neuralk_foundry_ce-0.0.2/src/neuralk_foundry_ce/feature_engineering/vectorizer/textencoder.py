from .base import BaseVectorizer
import pandas as pd
import numpy as np


class TextVectorizer(BaseVectorizer):
    """
    Encode textual columns in a DataFrame using e5-small-v2.

    Attributes
    ----------
    name : str
        Identifier of the transformer, set to `"text-vectorizer"`.

    Methods
    -------
    forward(X, y=None):
        Fit and transform the textual columns of `X` using `TextEncoder`, and
        concatenate the result with the untouched non-text columns.
    """
    name = "text-vectorizer"

    def __init__(self):
        super().__init__()

    def forward(self, X: pd.DataFrame, y=None):
        from skrub import TextEncoder as _TextEncoder

        text_columns = [
            col for col in X.columns
            if X[col].dtype == 'object' and X[col].apply(lambda x: isinstance(x, str)).any()
        ]

        non_text_columns = [col for col in X.columns if col not in text_columns]
        df_parts = []

        # Transform text columns
        for col in text_columns:
            X[col] = X[col].fillna("")
            vec = _TextEncoder(max_features=20)
            X_col_trans = vec.fit_transform(X[col])
            col_names = [f"{col}__{name}" for name in vec.get_feature_names_out()]
            df_col = pd.DataFrame(X_col_trans.toarray(), columns=col_names, index=X.index)
            df_parts.append(df_col)

        # Append non-text columns as-is
        df_parts.append(X[non_text_columns].reset_index(drop=True))
        X = pd.concat(df_parts, axis=1)
        return X