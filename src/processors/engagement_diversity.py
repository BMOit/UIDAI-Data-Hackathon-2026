"""
Engagement Diversity Processor
Calculates how many different engagement types each pincode has.
Data Points:
  - For each pincode: count how many of the 3 engagement types (demo, bio, enroll) have activity
  - Returns count of pincodes for each diversity level (0, 1, 2, or 3 types)
"""
from typing import Dict

import pandas as pd

from .base import BaseProcessor


class EngagementDiversityProcessor(BaseProcessor):

    @property
    def name(self) -> str:
        return "engagement_diversity_processor"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate engagement diversity for each pincode.
        
        Returns:
            DataFrame with columns: type_count, pincode_count
        """
        # Calculate total interactions per pincode for each dataset
        demo_totals = (
            data["demographic"]
            .assign(total=lambda x: x["demo_age_5_17"] + x["demo_age_17_"])
            .groupby("pincode", as_index=False)["total"]
            .sum()
            .rename(columns={"total": "demo_total"})
        )
        
        bio_totals = (
            data["biometric"]
            .assign(total=lambda x: x["bio_age_5_17"] + x["bio_age_17_"])
            .groupby("pincode", as_index=False)["total"]
            .sum()
            .rename(columns={"total": "bio_total"})
        )
        
        enroll_totals = (
            data["enrollment"]
            .assign(total=lambda x: x["age_0_5"] + x["age_5_17"] + x["age_18_greater"])
            .groupby("pincode", as_index=False)["total"]
            .sum()
            .rename(columns={"total": "enroll_total"})
        )
        
        # Get all unique pincodes
        all_pincodes = pd.concat([
            demo_totals[["pincode"]],
            bio_totals[["pincode"]],
            enroll_totals[["pincode"]]
        ]).drop_duplicates()
        
        # Merge all totals
        result = all_pincodes.copy()
        result = result.merge(demo_totals, on="pincode", how="left")
        result = result.merge(bio_totals, on="pincode", how="left")
        result = result.merge(enroll_totals, on="pincode", how="left")
        
        # Fill NaN with 0
        result = result.fillna(0)
        
        # Calculate type count (how many types have activity > 0)
        result["has_demo"] = (result["demo_total"] > 0).astype(int)
        result["has_bio"] = (result["bio_total"] > 0).astype(int)
        result["has_enroll"] = (result["enroll_total"] > 0).astype(int)
        result["type_count"] = result["has_demo"] + result["has_bio"] + result["has_enroll"]
        
        # Group by type_count and count pincodes
        diversity_summary = (
            result
            .groupby("type_count", as_index=False)
            .size()
            .rename(columns={"size": "pincode_count"})
        )
        
        return diversity_summary
