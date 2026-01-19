"""
Daily Aggregator
Output columns: date, demo_total, bio_total, enroll_total
Data Points:
  - demo_total = SUM(demo_age_5_17 + demo_age_17_) per day
  - bio_total = SUM(bio_age_5_17 + bio_age_17_) per day
  - enroll_total = SUM(age_0_5 + age_5_17 + age_18_greater) per day
"""
from typing import Dict

import pandas as pd

from .base import BaseProcessor


class DailyAggregator(BaseProcessor):

    @property
    def name(self) -> str:
        return "daily_aggregator"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        demo = data["demographic"]
        bio = data["biometric"]
        enroll = data["enrollment"]

        demo_daily = (
            demo
            .assign(demo_total=lambda x: x["demo_age_5_17"] + x["demo_age_17_"])
            .groupby("date", as_index=False)["demo_total"]
            .sum()
        )

        bio_daily = (
            bio
            .assign(bio_total=lambda x: x["bio_age_5_17"] + x["bio_age_17_"])
            .groupby("date", as_index=False)["bio_total"]
            .sum()
        )

        enroll_daily = (
            enroll
            .assign(enroll_total=lambda x: x["age_0_5"] + x["age_5_17"] + x["age_18_greater"])
            .groupby("date", as_index=False)["enroll_total"]
            .sum()
        )

        merged = (
            demo_daily
            .merge(bio_daily, on="date", how="outer")
            .merge(enroll_daily, on="date", how="outer")
            .fillna(0)
            .sort_values("date")
        )

        return merged
