from dataclasses import dataclass

from neuralk_foundry_ce.datasets.base import OpenMLDataConfig


@dataclass
class DataConfig(OpenMLDataConfig):
    name: str  = "openml-1462"
    task: str  = "classification"
    target: str = "Class"
    openml_id: int = 1462
    openml_name = "banknote-authentication"
