from neuralk_foundry_ce.feature_engineering.pairwise import PairFeatureGenerator
from neuralk_foundry_ce.feature_engineering.preprocessing import LabelEncoder
from neuralk_foundry_ce.feature_engineering.preprocessing import NumericalPreprocessor, CategoricalPreprocessor
import pandas as pd
import numpy as np
import pytest
import pandas as pd
import numpy as np
from sklearn.utils.validation import check_is_fitted


def test_pair_feature_generator_execute():
    # Create dummy data with even number of columns
    X_dummy = pd.DataFrame(np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]))

    step = PairFeatureGenerator()
    step._execute({'X_pairs': X_dummy})

    # Check shape: we expect vstack([X1, X2, diff, product]) => (3, 2 * 4)
    out = step._returned_outputs["X_pairs"]
    assert out.shape == (3, 8)


def test_preprocessing_with_text_passthrough():
    n_samples = 60
    df = pd.DataFrame({
        "num1": np.random.randn(n_samples),
        "num2": np.random.choice([1.0, 2.0, np.nan], size=n_samples),
        "cat1": np.random.choice(["a", "b", "c"], size=n_samples),
        "long_text": [f"text example {i}" for i in range(n_samples)],  # >50 unique values
        "date": pd.date_range("2020-01-01", periods=n_samples, freq="D"),
    })
    y = np.random.choice(["yes", "no"], size=n_samples)

    inputs = {"X": df, "y": y, 'numerical_features': ['num1', 'num2'], 'categorical_features': ['cat1']}

    # Apply numerical preprocessing
    num_step = NumericalPreprocessor()
    num_out = num_step.run(inputs)
    inputs['X'] = num_out['X']

    # Apply categorical preprocessing
    cat_step = CategoricalPreprocessor()
    cat_out = cat_step.run(inputs)
    inputs['X'] = cat_out['X']

    result = inputs['X']

    # Basic shape check
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == n_samples

    # Ensure no missing values after imputation
    assert not result.isnull().values.any()


def test_label_encoding_step():
    y_input = ["dog", "cat", "dog", "bird", "cat", "bird"]
    expected_classes = sorted(set(y_input))  # ['bird', 'cat', 'dog']

    step = LabelEncoder()
    step._execute({"y": y_input})
    y_encoded = step._returned_outputs['y']

    # Assert output type and shape
    assert isinstance(y_encoded, np.ndarray)
    assert y_encoded.shape == (len(y_input),)

    # Check that encoded values are within range
    assert set(y_encoded) == set(range(len(expected_classes)))