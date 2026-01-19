"""
District Aggregator
Aggregates data by district for ranking charts.
Data Points:
  - demographic: SUM(demo_age_5_17 + demo_age_17_) GROUP BY (state, district)
"""
from typing import Dict

import pandas as pd

from .base import BaseProcessor


class DistrictAggregator(BaseProcessor):

    @property
    def name(self) -> str:
        return "district_aggregator"

    def process(self, data: Dict[str, pd.DataFrame], dataset: str = "demographic", top_n: int = 20) -> pd.DataFrame:
        """
        Aggregate data by district.
        
        Returns:
            DataFrame with columns: district_label, total
        """
        df = data[dataset]

        if dataset == "demographic":
            result = (
                df
                .assign(total=lambda x: x["demo_age_5_17"] + x["demo_age_17_"])
                .groupby(["state", "district"], as_index=False)["total"]
                .sum()
            )
        elif dataset == "biometric":
            result = (
                df
                .assign(total=lambda x: x["bio_age_5_17"] + x["bio_age_17_"])
                .groupby(["state", "district"], as_index=False)["total"]
                .sum()
            )
        elif dataset == "enrollment":
            result = (
                df
                .assign(total=lambda x: x["age_0_5"] + x["age_5_17"] + x["age_18_greater"])
                .groupby(["state", "district"], as_index=False)["total"]
                .sum()
            )
        else:
            raise ValueError(f"Unknown dataset: {dataset}")

        # Create state abbreviations (first 2-3 letters)
        def abbreviate_state(state):
            abbrev = {
                "Andhra Pradesh": "AP",
                "Arunachal Pradesh": "AR",
                "Assam": "AS",
                "Bihar": "BR",
                "Chhattisgarh": "CG",
                "Goa": "GA",
                "Gujarat": "GJ",
                "Haryana": "HR",
                "Himachal Pradesh": "HP",
                "Jharkhand": "JH",
                "Karnataka": "KA",
                "Kerala": "KL",
                "Madhya Pradesh": "MP",
                "Maharashtra": "MH",
                "Manipur": "MN",
                "Meghalaya": "ML",
                "Mizoram": "MZ",
                "Nagaland": "NL",
                "Odisha": "OD",
                "Punjab": "PB",
                "Rajasthan": "RJ",
                "Sikkim": "SK",
                "Tamil Nadu": "TN",
                "Telangana": "TG",
                "Tripura": "TR",
                "Uttar Pradesh": "UP",
                "Uttarakhand": "UK",
                "West Bengal": "WB",
            }
            return abbrev.get(state, state[:2].upper())
        
        result["state_abbr"] = result["state"].apply(abbreviate_state)
        result["district_label"] = result["district"] + ", " + result["state_abbr"]
        
        return result.nlargest(top_n, "total").sort_values("total", ascending=True)
