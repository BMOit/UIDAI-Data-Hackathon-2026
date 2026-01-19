"""
Weekly Pattern Processor
Analyzes weekly patterns in demographic interactions.
Data Points:
  - Extract weekday from date
  - Calculate average daily interactions per weekday
"""
from typing import Dict

import pandas as pd

from .base import BaseProcessor


class WeeklyPatternProcessor(BaseProcessor):

    @property
    def name(self) -> str:
        return "weekly_pattern_processor"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate average interactions by day of week.
        
        Returns:
            DataFrame with columns: weekday, avg_interactions
        """
        demo_df = data["demographic"].copy()
        
        # Calculate total interactions per row
        demo_df["total"] = demo_df["demo_age_5_17"] + demo_df["demo_age_17_"]
        
        # Extract weekday (0=Monday, 6=Sunday)
        demo_df["weekday"] = pd.to_datetime(demo_df["date"], format="%d-%m-%Y").dt.dayofweek
        
        # Calculate average by weekday
        weekday_avg = (
            demo_df
            .groupby("weekday", as_index=False)["total"]
            .mean()
            .rename(columns={"total": "avg_interactions"})
        )
        
        # Map weekday numbers to names
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_avg["weekday_name"] = weekday_avg["weekday"].map(lambda x: weekday_names[x])
        
        return weekday_avg[["weekday_name", "avg_interactions"]]
