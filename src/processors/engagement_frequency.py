"""
Engagement Frequency Processor
Aggregates engagement frequency data by pincode across all datasets.
Data Points:
  - For each pincode: COUNT(rows in demo) + COUNT(rows in bio) + COUNT(rows in enroll)
  - Filters to <= 95th percentile to remove extreme outliers
"""
from typing import Dict

import pandas as pd
import numpy as np

from .base import BaseProcessor


class EngagementFrequencyProcessor(BaseProcessor):

    @property
    def name(self) -> str:
        return "engagement_frequency_processor"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate engagement frequency for each pincode.
        
        Returns:
            DataFrame with columns: pincode, total_frequency
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
        
        # Fill NaN with 0
        result = result.fillna(0)
        
        # Calculate total frequency
        result["total_frequency"] = (
            result["demo_freq"] + 
            result["bio_freq"] + 
            result["enroll_freq"]
        )
        
        # Filter to 95th percentile
        percentile_95 = result["total_frequency"].quantile(0.95)
        result = result[result["total_frequency"] <= percentile_95]
        
        return result[["pincode", "total_frequency"]]
