"""
State Aggregator
Aggregates data by state for ranking charts.
Data Points:
  - demographic: SUM(demo_age_5_17 + demo_age_17_) GROUP BY state
  - biometric: SUM(bio_age_5_17 + bio_age_17_) GROUP BY state
  - enrollment: SUM(age_0_5 + age_5_17 + age_18_greater) GROUP BY state
"""
from typing import Dict

import pandas as pd

from .base import BaseProcessor


class StateAggregator(BaseProcessor):

    @property
    def name(self) -> str:
        return "state_aggregator"

    def process(self, data: Dict[str, pd.DataFrame], dataset: str = "demographic", top_n: int = 15) -> pd.DataFrame:
        df = data[dataset]

        if dataset == "demographic":
            result = (
                df
                .assign(total=lambda x: x["demo_age_5_17"] + x["demo_age_17_"])
                .groupby("state", as_index=False)["total"]
                .sum()
            )
        elif dataset == "biometric":
            result = (
                df
                .assign(total=lambda x: x["bio_age_5_17"] + x["bio_age_17_"])
                .groupby("state", as_index=False)["total"]
                .sum()
            )
        elif dataset == "enrollment":
            result = (
                df
                .assign(total=lambda x: x["age_0_5"] + x["age_5_17"] + x["age_18_greater"])
                .groupby("state", as_index=False)["total"]
                .sum()
            )
        else:
            raise ValueError(f"Unknown dataset: {dataset}")

        return result.nlargest(top_n, "total").sort_values("total", ascending=True)
