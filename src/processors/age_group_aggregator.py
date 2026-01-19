"""
Age Group Aggregator
Aggregates data by age groups for interaction and enrollment analysis.
Data Points:
  - demographic: demo_age_5_17, demo_age_17_
  - biometric: bio_age_5_17, bio_age_17_
  - enrollment: age_0_5, age_5_17, age_18_greater
"""
from typing import Dict

import pandas as pd

from .base import BaseProcessor


class AgeGroupAggregator(BaseProcessor):

    @property
    def name(self) -> str:
        return "age_group_aggregator"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Default process method - returns interaction data."""
        return self.process_interactions(data)

    def process_interactions(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Process age group data for interactions (demographic + biometric).
        
        Returns:
            DataFrame with columns: category, total, percentage
        """
        demo_df = data["demographic"]
        bio_df = data["biometric"]
        
        results = {
            "5-17 (Demo)": demo_df["demo_age_5_17"].sum(),
            "18+ (Demo)": demo_df["demo_age_17_"].sum(),
            "5-17 (Bio)": bio_df["bio_age_5_17"].sum(),
            "18+ (Bio)": bio_df["bio_age_17_"].sum(),
        }
        
        # Calculate percentages within each type
        demo_total = results["5-17 (Demo)"] + results["18+ (Demo)"]
        bio_total = results["5-17 (Bio)"] + results["18+ (Bio)"]
        
        result_df = pd.DataFrame([
            {
                "category": "5-17 (Demo)",
                "total": results["5-17 (Demo)"],
                "percentage": (results["5-17 (Demo)"] / demo_total * 100) if demo_total > 0 else 0
            },
            {
                "category": "18+ (Demo)",
                "total": results["18+ (Demo)"],
                "percentage": (results["18+ (Demo)"] / demo_total * 100) if demo_total > 0 else 0
            },
            {
                "category": "5-17 (Bio)",
                "total": results["5-17 (Bio)"],
                "percentage": (results["5-17 (Bio)"] / bio_total * 100) if bio_total > 0 else 0
            },
            {
                "category": "18+ (Bio)",
                "total": results["18+ (Bio)"],
                "percentage": (results["18+ (Bio)"] / bio_total * 100) if bio_total > 0 else 0
            },
        ])
        
        return result_df

    def process_enrollments(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Process age group data for enrollments.
        
        Returns:
            DataFrame with columns: age_group, total, percentage
        """
        enroll_df = data["enrollment"]
        
        age_0_5 = enroll_df["age_0_5"].sum()
        age_5_17 = enroll_df["age_5_17"].sum()
        age_18_plus = enroll_df["age_18_greater"].sum()
        
        total = age_0_5 + age_5_17 + age_18_plus
        
        result_df = pd.DataFrame([
            {
                "age_group": "0-5",
                "total": age_0_5,
                "percentage": (age_0_5 / total * 100) if total > 0 else 0
            },
            {
                "age_group": "5-17",
                "total": age_5_17,
                "percentage": (age_5_17 / total * 100) if total > 0 else 0
            },
            {
                "age_group": "18+",
                "total": age_18_plus,
                "percentage": (age_18_plus / total * 100) if total > 0 else 0
            },
        ])
        
        return result_df
