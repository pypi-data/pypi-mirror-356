from pathlib import Path
import copy
import json

import joblib
import pandas as pd
import numpy as np
from typing import List
import warnings

from .step import Step
from .utils import make_json_serializable, notebook_display
from ..utils.logging import log


def load_cached_data(cache_dir: Path, step_id: str) -> dict:
    """Load cached data stored by `cache_data`.

    This function reads the cache folder created for a given step and loads:
    - Heavy objects stored as `.parquet`, `.npy`, or `.pkl`
    - Scalar values grouped into `_scalars.json`

    Parameters
    ----------
    cache_dir : Path
        Base directory where cached data was stored.

    step_id : str
        The step name whose cached results should be loaded.

    Returns
    -------
    data_dict : dict
        Dictionary containing all loaded objects and scalar values.

    Raises
    ------
    FileNotFoundError
        If the specified cache directory does not exist.

    ValueError
        If an unsupported file type is encountered during loading.
    """
    step_dir = cache_dir / step_id
    if not step_dir.exists():
        raise FileNotFoundError(f"No cache found for: {step_id}")

    data_dict = {}
    metrics_dict = {}

    for file in step_dir.iterdir():
        if file.name == "_scalars.json":
            with open(file, "r") as f:
                scalars = json.load(f)
                data_dict.update(scalars)
            continue

        if file.name == "_metrics.json":
            with open(file, "r") as f:
                metrics_dict = json.load(f)
            continue

        key = file.stem
        suffix = file.suffix

        if suffix == ".parquet":
            df = pd.read_parquet(file)
            dtype_path = file.with_suffix('')  # removes '.parquet'
            dtype_json_path = dtype_path.with_suffix('.dtypes.json')
            if dtype_json_path.exists():
                meta = pd.read_json(dtype_json_path, typ="series")
                for col, dtype in meta.items():
                    if dtype == "category":
                        df[col] = df[col].astype("category")
            data_dict[key] = df 
        elif suffix == ".npy":
            data_dict[key] = np.load(file, allow_pickle=True)
        elif suffix == ".json":
            with open(file, "r") as f:
                data_dict[key] = json.load(f)
        elif suffix == ".pkl":
            with open(file, "rb") as f:
                data_dict[key] = joblib.load(f)
        else:
            raise ValueError(f"Unsupported file type: {file.name}")

    return data_dict, metrics_dict


def set_seed(seed: int = 42) -> None:
    """
    Set the random seed for reproducibility across numpy, random, and common ML libraries.
    """
    import random
    import os

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass


def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


class WorkFlow:
    """
    Sequence of processing steps.

    This class manages an ordered list of `Step` instances, executing them sequentially.
    It optionally supports caching intermediate results to a specified directory.

    Parameters
    ----------
    steps : list of Step
        An ordered list of `Step` instances that define the workflow.

    cache_dir : pathlib.Path, optional (default=Path('./cache'))
        Directory path where intermediate results or artifacts can be cached.

    Attributes
    ----------
    steps : list of Step
        The sequence of steps to be executed in the workflow.

    cache_dir : pathlib.Path
        The directory used for caching intermediate results.
    """

    def __init__(self, steps, cache_dir=Path('./cache')):
        self.steps = steps
        if isinstance(cache_dir, str):
            cache_dir = Path(cache_dir)
        self.cache_dir = cache_dir

    def check_consistency(self, init_keys: dict = {}):
        """
        Check that a sequence of steps can be executed in order without missing inputs.

        This function verifies that each step in the list has its declared input fields 
        available based on the outputs of previous steps and the initial input keys.

        Parameters
        ----------
        steps : list of Step
            The ordered list of Step instances representing the workflow.

        init_keys : dict, optional (default={})
            A dictionary representing the initial set of available input fields 
            before any steps are run. Only the keys are used.

        Raises
        ------
        KeyError
            If any step requires an input field that is not available at that point in the sequence.

        Returns
        -------
        None
            The function performs checks in-place and raises if an inconsistency is found.
        """
        sane = True
        available = set(init_keys)

        for i, step in enumerate(self.steps):
            if not isinstance(step, Step):
                raise TypeError(f"Step {step.name} is not a PipelineStep.")

            required, outputs = step.get_inputs_outputs()

            unavailable = required - available
            if unavailable:
                warnings.warn(f"Step {i} {step.name} requires unavailable fields: {unavailable}")
                sane = False

            # Update available fields
            available.update(outputs)
        
        return sane


    def cache_data(self, step_id: str, data_dict: dict, metrics_dict: dict):
        """Cache a dictionary of mixed data types into a structured folder.

        Heavy objects are stored individually with a suitable format, while scalars are grouped into a JSON file.

        Parameters
        ----------
        step_id : str
            Unique name for the current step; used to create a subdirectory inside `cache_dir`.

        data_dict : dict
            Dictionary where keys are names (str) and values are the data to be cached.

        Returns
        -------
        None
        """
        if self.cache_dir is None:
            return
        step_dir = self.cache_dir / step_id
        step_dir.mkdir(parents=True, exist_ok=True)

        scalar_dict = {}

        for key, value in data_dict.items():
            file_path = step_dir / key

            if isinstance(value, pd.DataFrame):
                meta = {col: dtype.name for col, dtype in value.dtypes.items()}
                value.to_parquet(file_path.with_suffix(".parquet"))
                meta = {col: dtype.name for col, dtype in value.dtypes.items()}
                pd.Series(meta).to_json(file_path.with_suffix(".dtypes.json"))
            elif isinstance(value, np.ndarray):
                np.save(file_path.with_suffix(".npy"), value)
            elif isinstance(value, (int, float, str, bool, type(None))):
                scalar_dict[key] = value
            elif isinstance(value, (dict, list)) and is_json_serializable(value):
                with open(file_path.with_suffix(".json"), "w") as f:
                    json.dump(value, f)
            else:
                with open(file_path.with_suffix(".pkl"), "wb") as f:
                    joblib.dump(value, f)

        if scalar_dict:
            with open(step_dir / "_scalars.json", "w") as f:
                scalar_dict = make_json_serializable(scalar_dict)
                json.dump(scalar_dict, f)

        if metrics_dict:
            with open(step_dir / "_metrics.json", "w") as f:
                metrics_dict = make_json_serializable(metrics_dict)
                json.dump(metrics_dict, f)


    def run(self, init_data: dict) -> tuple[dict, dict]:
        """
        Execute the workflow sequentially on the provided input data.

        This method runs each step in order, passing the accumulated data forward.
        If a cached result exists for a step, it is loaded instead of recomputing.
        Metrics logged by each step are collected and returned.

        Parameters
        ----------
        init_data : dict
            Initial input data provided to the workflow. Keys must match the required
            inputs for the first step, unless `check_first_step` is disabled.

        Returns
        -------
        data : dict
            Final merged dictionary of all outputs produced throughout the workflow.

        metrics : dict of str to dict
            A dictionary mapping each step name to its logged metrics.

        Raises
        ------
        KeyError
            If any step is missing required input fields at runtime.
        """

        self.check_consistency(init_data.keys())

        data = copy.copy(init_data)
        metrics = {}

        for i_step, step in enumerate(self.steps):
            step_id = f'{i_step}_{step.name}'

            # Check if the output exists which indicates that the step ran successfuly
            if self.cache_dir and (self.cache_dir / step_id).exists():
                new_data, new_metrics = load_cached_data(self.cache_dir, step_id)
            else:
                # In case the seed is not set in the step, best effort to ensure reproducibility
                set_seed(i_step)
                new_data = step.run(data)
                new_metrics = step.logged_metrics
                self.cache_data(step_id, new_data, new_metrics)

            data.update(new_data)
            metrics[step.name] = new_metrics

        return data, metrics
    
    def set_parameter(self, parameter_name, value, set_all=True, verbose=1):
        steps_with_parameter = []
        for step in self.steps:
            for field in step.params:
                if field.name == parameter_name:
                    steps_with_parameter.append(step)
        if len(steps_with_parameter) == 0:
            log(verbose, 1, f"No step in the workflow has parameter {parameter_name}")
            return
        elif len(steps_with_parameter) > 1 and not set_all:
            log(verbose, 1, f"Multiple steps in the workflow have parameter {parameter_name}, stopping.")
        
        log(verbose, 1, f"Setting parameter {parameter_name} for all steps in the workflow")
        for step in steps_with_parameter:
            log(verbose, 2, f"Setting parameter {parameter_name} for step {step.name}")
            step.set_parameter(parameter_name, value)

    def display(self):
        return notebook_display(self.steps)
