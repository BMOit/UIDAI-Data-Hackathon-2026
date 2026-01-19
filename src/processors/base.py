"""Base class for data processors."""
from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd


class BaseProcessor(ABC):

    @abstractmethod
    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass
