"""
Monthly Aggregator
Aggregates data by month for engagement comparison.
Data Points:
  - Extract month from date
  - Calculate total interactions per month for each dataset
"""
from typing import Dict

import pandas as pd

from .base import BaseProcessor


class MonthlyAggregator(BaseProcessor):

    @property
    def name(self) -> str:
        return "monthly_aggregator"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate monthly engagement for all three datasets.
        
        Returns:
            DataFrame with columns: month, demographic, biometric, enrollment
        """
        # Process demographic data
        demo_df = data["demographic"].copy()
        demo_df["total"] = demo_df["demo_age_5_17"] + demo_df["demo_age_17_"]
        demo_df["date"] = pd.to_datetime(demo_df["date"], format="%d-%m-%Y")
        demo_df["month"] = demo_df["date"].dt.to_period("M")
        demo_monthly = demo_df.groupby("month", as_index=False)["total"].sum().rename(columns={"total": "demographic"})
        
        # Process biometric data
        bio_df = data["biometric"].copy()
        bio_df["total"] = bio_df["bio_age_5_17"] + bio_df["bio_age_17_"]
        bio_df["date"] = pd.to_datetime(bio_df["date"], format="%d-%m-%Y")
        bio_df["month"] = bio_df["date"].dt.to_period("M")
        bio_monthly = bio_df.groupby("month", as_index=False)["total"].sum().rename(columns={"total": "biometric"})
        
        # Process enrollment data
        enroll_df = data["enrollment"].copy()
        enroll_df["total"] = enroll_df["age_0_5"] + enroll_df["age_5_17"] + enroll_df["age_18_greater"]
        enroll_df["date"] = pd.to_datetime(enroll_df["date"], format="%d-%m-%Y")
        enroll_df["month"] = enroll_df["date"].dt.to_period("M")
        enroll_monthly = enroll_df.groupby("month", as_index=False)["total"].sum().rename(columns={"total": "enrollment"})
        
        # Merge all months
        result = demo_monthly.merge(bio_monthly, on="month", how="outer")
        result = result.merge(enroll_monthly, on="month", how="outer")
        result = result.fillna(0)
        
        # Convert period to string for display
        result["month_str"] = result["month"].astype(str)
        
        return result.sort_values("month")
