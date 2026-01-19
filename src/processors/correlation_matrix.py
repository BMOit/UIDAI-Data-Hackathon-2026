"""
Correlation Matrix Processor
Calculates correlation between engagement metrics aggregated by pincode.
Data Points:
  - 7 metrics: total_demo, total_bio, total_enroll, demo_freq, bio_freq, enroll_freq, total_freq
  - Pearson correlation between all pairs
"""
from typing import Dict

import pandas as pd
import numpy as np

from .base import BaseProcessor


class CorrelationMatrixProcessor(BaseProcessor):

    @property
    def name(self) -> str:
        return "correlation_matrix_processor"

    def process(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Calculate correlation matrix for engagement metrics.
        
        Returns:
            DataFrame: 7x7 correlation matrix
        """
        # Aggregate by pincode
        demo_agg = (
            data["demographic"]
            .assign(total=lambda x: x["demo_age_5_17"] + x["demo_age_17_"])
            .groupby("pincode")
            .agg(
                total_demo_interactions=("total", "sum"),
                demo_interaction_frequency=("total", "count")
            )
            .reset_index()
        )
        
        bio_agg = (
            data["biometric"]
            .assign(total=lambda x: x["bio_age_5_17"] + x["bio_age_17_"])
            .groupby("pincode")
            .agg(
                total_bio_interactions=("total", "sum"),
                bio_interaction_frequency=("total", "count")
            )
            .reset_index()
        )
        
        enroll_agg = (
            data["enrollment"]
            .assign(total=lambda x: x["age_0_5"] + x["age_5_17"] + x["age_18_greater"])
            .groupby("pincode")
            .agg(
                total_enrollments=("total", "sum"),
                enrollment_frequency=("total", "count")
            )
            .reset_index()
        )
        
        # Get all unique pincodes
        all_pincodes = pd.concat([
            demo_agg[["pincode"]],
            bio_agg[["pincode"]],
            enroll_agg[["pincode"]]
        ]).drop_duplicates()
        
        # Merge all metrics
        metrics = all_pincodes.copy()
        metrics = metrics.merge(demo_agg, on="pincode", how="left")
        metrics = metrics.merge(bio_agg, on="pincode", how="left")
        metrics = metrics.merge(enroll_agg, on="pincode", how="left")
        
        # Fill NaN with 0
        metrics = metrics.fillna(0)
        
        # Calculate total engagement frequency
        metrics["total_engagement_frequency"] = (
            metrics["demo_interaction_frequency"] +
            metrics["bio_interaction_frequency"] +
            metrics["enrollment_frequency"]
        )
        
        # Select the 7 metrics for correlation
        metric_columns = [
            "total_demo_interactions",
            "total_bio_interactions",
            "total_enrollments",
            "demo_interaction_frequency",
            "bio_interaction_frequency",
            "enrollment_frequency",
            "total_engagement_frequency"
        ]
        
        # Calculate correlation matrix
        corr_matrix = metrics[metric_columns].corr()
        
        # Rename for better display
        display_names = {
            "total_demo_interactions": "Demo\nInteractions",
            "total_bio_interactions": "Bio\nInteractions",
            "total_enrollments": "Enrollments",
            "demo_interaction_frequency": "Demo\nFrequency",
            "bio_interaction_frequency": "Bio\nFrequency",
            "enrollment_frequency": "Enroll\nFrequency",
            "total_engagement_frequency": "Total\nFrequency"
        }
        
        corr_matrix.index = [display_names[col] for col in corr_matrix.index]
        corr_matrix.columns = [display_names[col] for col in corr_matrix.columns]
        
        return corr_matrix
