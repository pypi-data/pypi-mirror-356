import pandas as pd
import numpy as np
from neuralk_foundry_ce.models.classifier import MLPClassifier  # adjust as needed
from neuralk_foundry_ce.utils.splitting import Split


def test_mlp_unknown_category_handling():
    # Create toy dataset with categorical features
    df_train = pd.DataFrame({
        'color': ['red', 'blue', 'green', 'blue', 'red'],
        'shape': ['circle', 'square', 'triangle', 'square', 'circle'],
        'value': [1.2, 3.4, 2.1, 3.3, 1.1],
        'target': [0, 1, 0, 1, 0],
    })

    df_test = pd.DataFrame({
        'color': ['red', 'yellow'],  # yellow is unseen
        'shape': ['circle', 'triangle'],  # all seen
        'value': [1.0, 2.2],
    })

    df_all = pd.concat([df_train, df_test], ignore_index=True)
    categorical_features = ['color', 'shape']
    for col in categorical_features:
        df_all[col] = df_all[col].astype('category')

    # Simulate split mask
    split_mask = np.array([Split.TRAIN] * len(df_train) + [Split.TEST] * len(df_test))

    model = MLPClassifier()
    model.extras = {}
    config = {
        'categorical_features': categorical_features,
        'activation': 'relu',
        'dropout': 0.0,
        'batchnorm': False,
        'n_hidden_layers': 1,
        'optimizer': 'adamw',
        'lr': 1e-3,
        'epochs': 5,
        'use_unknown_category': True,
        'simulate_unknowns': 0.5,  # high to test easily
    }

    inputs = {
        'X': df_all.drop(columns='target', errors='ignore'),
        'y': df_all['target'].fillna(0).astype(int),
    }

    config.update(model.get_fixed_params(inputs))
    model.init_model(config)

    model.train(inputs['X'], inputs['y'], split_mask, splits=[Split.TRAIN])

    # Check that only 'color' uses unknown category (has unseen value "yellow")
    assert model.include_unknown_index['color'] is True
    assert model.include_unknown_index['shape'] is False

    # Forward pass (on test set)
    y_pred = model.forward(inputs['X'], split_mask=split_mask, splits=[Split.TEST])
    assert isinstance(y_pred, np.ndarray)
    assert len(y_pred) == len(df_test)

    print("Test passed: unknown category logic behaves as expected.")