from dataclasses import dataclass
import numpy as np
from sklearn.impute import SimpleImputer

from .base import BaseVectorizer


class TableVectorizer(BaseVectorizer):
    """
    Vectorizer based on `skrub`'s TableVectorizer for automatic preprocessing
    of heterogeneous tabular data.

    This step performs automatic encoding of categorical variables, imputation,
    and scaling using a pipeline built by `skrub.TableVectorizer`. It expects
    a target `y` during the first call to fit the encoder in a supervised manner.

    Attributes
    ----------
    name : str
        Name of the step, set to "table_vectorizer".
    vectorizer : skrub.TableVectorizer
        The underlying vectorization pipeline.
    imputer : sklearn.impute.SimpleImputer
        Imputer used to fill missing values in the transformed features.
    is_fitted : bool
        Flag indicating whether the vectorizer has been fitted.

    Methods
    -------
    forward(X, y=None):
        Transform the input features using the fitted pipeline.
    """
    name = "table_vectorizer"

    def __init__(self):
        super().__init__()
        from skrub import TableVectorizer as _TableVectorizer
        self.vectorizer = _TableVectorizer()
        self.is_fitted = False

    def forward(self, X, y=None):
        """
        Preprocess and vectorize the input tabular data.

        Parameters
        ----------
        X : DataFrame or array-like
            The input feature matrix.
        y : array-like, optional
            Target values. Required the first time to fit the vectorizer.

        Returns
        -------
        X_transformed : ndarray
            The transformed, imputed feature matrix.

        Raises
        ------
        ValueError
            If the vectorizer has not been fitted and `y` is not provided.
        """
        
        if not self.is_fitted:
            if y is None:
                raise "Model is not fitted. User need to provide with target feature y for model fitting."
            self.vectorizer.fit(X, y)  # Fit and transform on training data
            self.is_fitted = True
        X_transformed = self.vectorizer.transform(X)
        return X_transformed
