import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from typing import List
from importlib import import_module
from collections import defaultdict
import openml

from ..utils.data import load_dataframe, get_dataset_dir
from ..workflow import Step, Field


class LoadDataset(Step):
    """
        Loads a dataset and insert it in the pipeline.

    Parameters
    ----------
    dataset : str
        Name of the dataset. The dataset configuration must be registered.
    """
    name='load-dataset'
    outputs = [
        Field('X', 'Input features of the dataset'),
        Field('y', 'Target variable to predict'),
        Field('task', 'Type of prediction task'),
        Field('target', 'Name of the target column to predict')
    ]
    params = [
        Field('dataset', 'Name of the dataset to load')
    ]

    def _execute(self, inputs):
        config = get_data_config(self.dataset)()
        data, target_col = config.load()

        y = data[config.target].to_numpy()
        X = data.drop(columns=config.target)

        if not isinstance(X, pd.DataFrame):
            raise ValueError('Dataset must be a pandas dataFrame')

        self.output('X', X)
        self.output('y', y)
        self.output('task', config.task)
        self.output('target', config.target)


class BaseDataConfigMeta(type):
    registry = {}                    # name -> class
    subclass_map = defaultdict(set)  # parent_name -> {subclass_name}
    root_path = {}                   # name -> [path]

    def __new__(cls, name, bases, namespace):
        new_cls = super().__new__(cls, name, bases, namespace)
        step_name = namespace.get("name")
        if step_name:
            if step_name in cls.registry:
                raise ValueError(f"Duplicate dataset name: {step_name}")
            cls.registry[step_name] = new_cls

        return new_cls
    
    @classmethod
    def get_data_config(cls, name):
        if name not in cls.registry:
            return None
        return cls.registry[name]


@dataclass
class BaseDataConfig(metaclass=BaseDataConfigMeta):
    """
    Config class for Datasets.
    All datasets should have a specific config that implements:
        - custom initialization [Optional]
        - information for data loading

    Attributes
    ----------
    name : str
        Name of the dataset.
    task : str
        Task for which the dataset is made.
    target : str
        Name of the target column in the input data.
    """

    name: str = field(default=None)
    task: str = field(default=None)
    target: str = field(default=None)


def get_data_config(name):
    """
    Retrieve a dataset configuration by name.

    This function looks up the dataset configuration in the predefined set
    of neuralk's data configurations and the set of configurations
    registered externally.

    Parameters
    ----------
    name : str
        The name of the dataset configuration to retrieve.

    Returns
    -------
    config : DataConfig
        The configuration object associated with the dataset.

    Raises
    ------
    ValueError
        If the dataset configuration cannot be found.
    """
    data_config = BaseDataConfigMeta.get_data_config(name)
    if data_config is not None:
        return data_config
    for top_module in ['openml', 'industrial']:
        try:
            module = import_module(f"neuralk_foundry_ce.datasets.{top_module}.{name}")
            config = getattr(module, "DataConfig", None)
            if config is None:
                raise ValueError(f"DataConfig not found in {name}.")
            return config
        except ModuleNotFoundError as e:
            pass
    raise ValueError(f'Could not find dataset {name} in predefined or custom data configurations')


class OpenMLDataConfig(BaseDataConfig):
    """
    Dataset configuration for OpenML datasets.

    This class includes an OpenML-specific identifier,
    allowing datasets to be loaded directly from the OpenML repository.

    Attributes
    ----------
    openml_id : int
        The OpenML dataset ID used to retrieve the dataset.

    Methods
    -------
    load():
        Load the dataset from OpenML using the specified OpenML ID.
    """
    openml_id: int = field(default=None)

    def load(self):
        """
        Load the dataset from OpenML.

        Downloads and returns the dataset corresponding to the provided
        OpenML ID. This method relies on an internet connection and the
        `openml` Python package.

        Returns
        -------
        data : tuple of pandas Dataframe and str
            The dataset loaded from OpenML and the target column of the task.

        Raises
        ------
        ValueError
            If `openml_id` is not provided or is invalid.

        openml.exceptions.OpenMLException
            If there is a problem retrieving the dataset from OpenML.
        """
        if self.openml_id is None:
            raise ValueError(f'No OpenML ID was specified for dataset {self.name}')
        try:
            dataset = openml.datasets.get_dataset(self.openml_id)
            df, self.target_columns, _, _ = dataset.get_data()
            data = df

            if hasattr(self, 'target'):
                target_col = self.target
            elif dataset.default_target_attribute:
                target_col = dataset.default_target_attribute  # Assuming single target
            else:
                raise ValueError(f"Target column not specified and not found in OpenML metadata for dataset ID {self.dataset_id}. Please provide target_col in constructor.")

        except openml.exceptions.OpenMLCacheException:
            print(f"Dataset ID {self.openml_id} not found on OpenML.")
        except Exception as e:
            print(f"Error loading dataset {self.openml_id} from OpenML: {e}")

        return data, target_col


class LocalDataConfig(BaseDataConfig):
    """
    Dataset configuration for loading local datasets from a file path.

    This class extends `BaseDataConfig` to support loading datasets stored
    locally, typically as CSV, Parquet, or similar tabular file formats.

    Attributes
    ----------
    file_path : Path or str
        The path to the local file containing the dataset.

    Methods
    -------
    load():
        Load the dataset from the local file and return features and target.
    """
    file_path: Path | str = field(default=None)

    def load(self):
        """
        Load the dataset from a local file.

        This method loads a dataset from a local path using the `load_dataframe`
        utility function and returns both the data and the target column name.

        Returns
        -------
        data : pandas.DataFrame
            The dataset loaded from the local file.

        target : str
            The name of the target column as defined in the config.

        Raises
        ------
        AssertionError
            If the configuration does not define a 'target' attribute.
        """
        assert(hasattr(self.config, 'target'))
        data = load_dataframe(Path(self.file_path))
        return data, self.config['target']


class DownloadDataConfig(BaseDataConfig):
    """
    Dataset configuration for downloading and loading external datasets.

    This class supports downloading datasets from a remote source to a local
    directory if they are not already present. It then loads the dataset into
    memory.

    Attributes
    ----------
    file_name : str
        The expected name of the dataset file once downloaded.

    Methods
    -------
    load():
        Download the dataset if needed and load it into memory.

    download_data(target_folder):
        Implemented in the subclass, it downloads the file and stores
        it in the specified target folder.
    """
    file_name: str = field(default=None)
    
    def download_data(self, target_folder: Path):
        """
        Download the dataset to the specified directory.

        Must be implemented by subclasses.

        Parameters
        ----------
        target_folder : Path
            The directory where the dataset should be saved.
        """
        raise NotImplementedError('Method must be implemented in subclass')

    def load(self):
        """
        Download and load the dataset.

        If the dataset file does not exist in the expected directory, it will
        be downloaded using the `download_data` method, which must be implemented
        by the subclass. Once the file is available locally, it is loaded into
        a DataFrame.

        Returns
        -------
        data : pandas.DataFrame
            The loaded dataset.

        target : str
            The name of the target column.
        """
        if self.file_name is None:
            raise ValueError('DataConfig.file_name must specify the name of the dataset file.')

        dataset_dir = get_dataset_dir() / self.name
        dataset_path = dataset_dir / self.file_name
        if not dataset_path.exists():
            dataset_dir.mkdir(parents=True, exist_ok=True)
            self.download_data(dataset_dir)
        return load_dataframe(dataset_path), self.target
