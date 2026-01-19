"""
Intensity Processor
Calculates engagement intensity score for pincodes.
Data Points:
  - Intensity score = (total_demo * 0.3 + total_bio * 0.4 + total_enroll * 0.3) / total_frequency
  - Filter: <= 95th percentile
"""
from typing import Dict

import pandas as pd
import numpy as np

from .base import BaseProcessor


class IntensityProcessor(BaseProcessor):

    @property
    def name(self) -> str:
        return "intensity_processor"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate engagement intensity score.
        
        Returns:
            DataFrame with columns: pincode, intensity_score
        """
        # Aggregate totals per pincode
        demo_agg = (
            data["demographic"]
            .assign(total=lambda x: x["demo_age_5_17"] + x["demo_age_17_"])
            .groupby("pincode")["total"]
            .sum()
            .reset_index(name="demo_total")
        )
        
        bio_agg = (
            data["biometric"]
            .assign(total=lambda x: x["bio_age_5_17"] + x["bio_age_17_"])
            .groupby("pincode")["total"]
            .sum()
            .reset_index(name="bio_total")
        )
        
        enroll_agg = (
            data["enrollment"]
            .assign(total=lambda x: x["age_0_5"] + x["age_5_17"] + x["age_18_greater"])
            .groupby("pincode")["total"]
            .sum()
            .reset_index(name="enroll_total")
        )

        # Get frequencies (number of update events/rows)
        demo_freq = data["demographic"].groupby("pincode").size().reset_index(name="demo_freq")
        bio_freq = data["biometric"].groupby("pincode").size().reset_index(name="bio_freq")
        enroll_freq = data["enrollment"].groupby("pincode").size().reset_index(name="enroll_freq")

        # Merge everything
        result = demo_agg.merge(bio_agg, on="pincode", how="outer")
        result = result.merge(enroll_agg, on="pincode", how="outer")
        result = result.merge(demo_freq, on="pincode", how="outer")
        result = result.merge(bio_freq, on="pincode", how="outer")
        result = result.merge(enroll_freq, on="pincode", how="outer")
        result = result.fillna(0)

        # Calculate total frequency
        result["total_frequency"] = result["demo_freq"] + result["bio_freq"] + result["enroll_freq"]
        
        # Filter 0 frequency to avoid division by zero (should not happen if data exists, but good safety)
        result = result[result["total_frequency"] > 0]

        # Calculate Intensity Score
        result["weighted_sum"] = (
            result["demo_total"] * 0.3 +
            result["bio_total"] * 0.4 +
            result["enroll_total"] * 0.3
        )
        result["intensity_score"] = result["weighted_sum"] / result["total_frequency"]

        # Filter <= 95th percentile
        percentile_95 = result["intensity_score"].quantile(0.95)
        result = result[result["intensity_score"] <= percentile_95]

        return result[["pincode", "intensity_score"]]
