"""Singleton data loader with caching for CSV datasets."""
from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional

import config


class DataLoader:

    _instance: Optional[DataLoader] = None

    def __new__(cls) -> DataLoader:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._demographic: Optional[pd.DataFrame] = None
        self._biometric: Optional[pd.DataFrame] = None
        self._enrollment: Optional[pd.DataFrame] = None
        self._initialized = True

    @property
    def demographic(self) -> pd.DataFrame:
        if self._demographic is None:
            files = sorted(config.DEMOGRAPHIC_DIR.glob("demographic-*.csv"))
            self._demographic = self._load_dataset(files)
        return self._demographic

    @property
    def biometric(self) -> pd.DataFrame:
        if self._biometric is None:
            files = sorted(config.BIOMETRIC_DIR.glob("biometric-*.csv"))
            self._biometric = self._load_dataset(files)
        return self._biometric

    @property
    def enrollment(self) -> pd.DataFrame:
        if self._enrollment is None:
            files = sorted(config.ENROLLMENT_DIR.glob("enrollment-*.csv"))
            self._enrollment = self._load_dataset(files)
        return self._enrollment

    def _load_dataset(self, file_paths: List[Path]) -> pd.DataFrame:
        dfs = []
        for path in file_paths:
            df = pd.read_csv(path, parse_dates=["date"], dayfirst=True)
            dfs.append(df)

        if not dfs:
            raise FileNotFoundError(f"No CSV files found: {file_paths}")

        return pd.concat(dfs, ignore_index=True)

    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        return {
            "demographic": self.demographic,
            "biometric": self.biometric,
            "enrollment": self.enrollment,
        }

    def clear_cache(self):
        self._demographic = None
        self._biometric = None
        self._enrollment = None
