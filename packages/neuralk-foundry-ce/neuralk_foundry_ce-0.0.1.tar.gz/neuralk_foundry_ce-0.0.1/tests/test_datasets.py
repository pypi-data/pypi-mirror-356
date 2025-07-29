from neuralk_foundry_ce.datasets import get_data_config, LocalDataConfig
from dataclasses import dataclass


@dataclass
class DataConfig(LocalDataConfig):
    name: str='fake_dataset'
    task: str = 'classification'
    target: str = 'target'
    data_path: str = "./my_dataset.parquet"


def test_registration_dataset():
    # Check that the dataset is well imported
    get_data_config('fake_dataset').name