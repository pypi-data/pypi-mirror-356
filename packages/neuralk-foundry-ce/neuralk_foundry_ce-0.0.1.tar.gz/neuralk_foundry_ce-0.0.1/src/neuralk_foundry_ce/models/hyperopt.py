from typing import List
import numpy as np
import optuna
from ..utils.splitting import Split


def objective(
    trial: int,
    model,
    X: np.array,
    y: np.array,
    splits: List,
    metrics: List,
    inputs
):
    """
    Objective function for hyperparameter optimization using Optuna.

    This function applies preprocessing (if provided), trains the model on
    multiple train/validation splits, and evaluates it using the provided metrics.
    It returns the average validation score used to guide the optimization.

    Parameters
    ----------
    trial : int
        The current trial object provided by Optuna, used to sample hyperparameters.
    model : BasePredictModel
        The predictive model to be optimized.
    X : np.array
        Input feature matrix.
    y : np.array
        Target labels.
    splits : list
        List of dictionaries containing boolean masks for train and validation splits.
    metrics : list
        List of scoring functions to evaluate model performance.
    inputs : dict
        Additional inputs passed to the model (e.g., metadata, configuration).

    Returns
    -------
    float
        The validation metric to be optimized (e.g., R-squared for regression or ROC-AUC
        for classification). Returns negative infinity for failed trials in classification
        tasks and positive infinity for failed trials in regression tasks.
    Notes
    -----
    - Metrics are computed for each fold and averaged to obtain the final validation metric.
    - If an exception occurs during training or evaluation, the trial is marked as failed.
    """    """Objective function for Optuna hyperparameter optimization, including preprocessing."""
    
    model_params = model.get_model_params(trial, inputs) | model.get_fixed_params(inputs)
    model.init_model(model_params)
    metric_to_optimize = inputs['metric_to_optimize']

    metric_results_val_list = {metric_name: [] for metric_name in metrics.keys()}

    for split_mask in splits:
        model.train(X, y=y, split_mask=split_mask, splits=[Split.TRAIN])

        y_val = y[np.isin(np.array(split_mask), [Split.VAL])]
        y_pred = model.forward(X, split_mask=split_mask, splits=[Split.VAL])
        outputs = {}
        outputs['y_pred'] = y_pred
        outputs['y_true'] = y_val
        if 'y_score' in model.extras:
            outputs['y_score'] = model.extras['y_score']
        if 'y_classes' in inputs:
            outputs['labels'] = np.arange(len(inputs['y_classes']))

        for metric_name, metric in metrics.items():
            metric_results_val_list[metric_name].append(metric(**outputs))
        
        if hasattr(model, 'clean_model'):
            model.clean_model()

    
    metric_results_val = {}
    for metric_name, values in metric_results_val_list.items():
        metric_results_val[metric_name] = np.mean(values)

    validation_metric = metric_results_val[metric_to_optimize]
    trial.set_user_attr("metric_results", metric_results_val)
    
    return validation_metric


def hyperoptimize(optuna_kwargs, model, X, y, splits, metrics, inputs, verbose=0):

    metric_to_optimize = inputs['metric_to_optimize']

    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study(
        direction="maximize"
        if metrics[metric_to_optimize].maximize
        else "minimize"
    )
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    study.optimize(
        lambda trial: objective(
            trial,
            model,
            X, y,
            splits,
            metrics,
            inputs,
        ),
        **optuna_kwargs
    )

    best_trial = study.best_trial
    return best_trial
