from .base import BaseVectorizer
import pandas as pd


class IdentityVectorizer(BaseVectorizer):
    """
    A no-op vectorizer that returns the input data unchanged.

    This vectorizer can be used when the input features are already in a
    numerical format suitable for downstream models. It also ensures compatibility
    with pipeline interfaces that expect a vectorizer.

    Attributes
    ----------
    name : str
        Name of the step, set to 'identity_vectorizer'.
    is_fitted : bool
        Always True, as no fitting is required.

    Methods
    -------
    forward(X, y=None):
        Returns the input X as-is, converting from DataFrame to ndarray if needed.
    """

    name = "identity_vectorizer"

    def __init__(self):
        super().__init__()
        self.is_fitted = True

    def forward(self, X, y=None):
        """
        Return the input data unchanged.

        Parameters
        ----------
        X : array-like or pandas.DataFrame
            The input features.

        y : array-like, optional
            Ignored.

        Returns
        -------
        X : ndarray
            The unchanged input data.
        """
        return X