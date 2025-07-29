from dataclasses import dataclass
import pandas as pd

from ..base import DownloadDataConfig


@dataclass
class DataConfig(DownloadDataConfig):
    name: str  = "best_buy_simple_categ"
    task: str  = "classification"
    target: str = "type"
    file_name: str = 'data.parquet'

    def download_data(self, dataset_dir):
        ds_url = 'https://raw.githubusercontent.com/BestBuyAPIs/open-data-set/refs/heads/master/products.json'
        df = pd.read_json(ds_url)[['name', 'type', 'price', 'manufacturer']]
        df = df[df.type.isin(['HardGood', 'Game', 'Software'])]
        df = df.reset_index(drop=True)
        df.to_parquet(dataset_dir / self.file_name)
