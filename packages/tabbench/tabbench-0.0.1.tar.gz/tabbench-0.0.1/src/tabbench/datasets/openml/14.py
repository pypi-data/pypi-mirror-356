from dataclasses import dataclass

from neuralk_foundry_ce.datasets.base import OpenMLDataConfig


@dataclass
class DataConfig(OpenMLDataConfig):
    name: str  = "openml-14"
    task: str  = "classification"
    target: str = "class"
    openml_id: int = 14
    openml_name = "mfeat-fourier"
