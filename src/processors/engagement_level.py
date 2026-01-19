"""
Engagement Level Processor
Categorizes pincodes by engagement level (Low, Medium, High).
Data Points:
  - Calculate total engagement frequency per pincode
  - Categorize by quartiles: Q1 (Low), Q2-Q3 (Medium), Q4 (High)
"""
from typing import Dict

import pandas as pd

from .base import BaseProcessor


class EngagementLevelProcessor(BaseProcessor):

    @property
    def name(self) -> str:
        return "engagement_level_processor"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate engagement level distribution.
        
        Returns:
            DataFrame with columns: level, count
        """
        # Count frequency per pincode in each dataset
        demo_freq = data["demographic"].groupby("pincode").size().reset_index(name="demo_freq")
        bio_freq = data["biometric"].groupby("pincode").size().reset_index(name="bio_freq")
        enroll_freq = data["enrollment"].groupby("pincode").size().reset_index(name="enroll_freq")
        
        # Get all unique pincodes
        all_pincodes = pd.concat([
            demo_freq[["pincode"]],
            bio_freq[["pincode"]],
            enroll_freq[["pincode"]]
        ]).drop_duplicates()
        
        # Merge all frequencies
        result = all_pincodes.copy()
        result = result.merge(demo_freq, on="pincode", how="left")
        result = result.merge(bio_freq, on="pincode", how="left")
        result = result.merge(enroll_freq, on="pincode", how="left")
        result = result.fillna(0)
        
        # Calculate total frequency
        result["total_frequency"] = (
            result["demo_freq"] + 
            result["bio_freq"] + 
            result["enroll_freq"]
        )
        
        # Calculate quartiles
        q1 = result["total_frequency"].quantile(0.25)
        q3 = result["total_frequency"].quantile(0.75)
        
        # Categorize
        def categorize(freq):
            if freq <= q1:
                return "Low (Q1)"
            elif freq <= q3:
                return "Medium (Q2-Q3)"
            else:
                return "High (Q4)"
        
        result["level"] = result["total_frequency"].apply(categorize)
        
        # Count by level
        level_counts = result.groupby("level").size().reset_index(name="count")
        
        # Ensure proper order
        level_order = ["Low (Q1)", "Medium (Q2-Q3)", "High (Q4)"]
        level_counts["level"] = pd.Categorical(level_counts["level"], categories=level_order, ordered=True)
        level_counts = level_counts.sort_values("level")
        
        return level_counts
