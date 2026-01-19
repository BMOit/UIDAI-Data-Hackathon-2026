"""
Chart 5: Engagement Frequency Distribution
Type of Chart: Histogram
Data Points:
  - All 3 datasets aggregated by pincode
  - X-axis: Total engagement frequency (binned into 50 bins)
  - Y-axis: Count of pincodes
  - Filter: <= 95th percentile to remove extreme outliers
"""
import matplotlib.pyplot as plt
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import EngagementFrequencyProcessor
import config


@register_chart
class Chart05EngagementFrequency(BaseChart):

    @property
    def chart_id(self) -> str:
        return "05"

    @property
    def title(self) -> str:
        return "Engagement Frequency Distribution"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = EngagementFrequencyProcessor()
        freq_data = processor.process(data)

        fig, ax = plt.subplots(figsize=(12, 8))

        # Create histogram with 50 bins
        n, bins, patches = ax.hist(
            freq_data["total_frequency"],
            bins=50,
            color=config.COLORS["primary"],
            edgecolor="white",
            linewidth=0.5,
            alpha=0.8
        )

        # Add statistics text
        mean_freq = freq_data["total_frequency"].mean()
        median_freq = freq_data["total_frequency"].median()
        percentile_95 = freq_data["total_frequency"].max()  # Already filtered to 95th
        
        stats_text = (
            f"Mean: {mean_freq:.1f}\n"
            f"Median: {median_freq:.0f}\n"
            f"95th %ile: {percentile_95:.0f}"
        )
        
        ax.text(
            0.97, 0.97,
            stats_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray")
        )

        self._apply_common_style(ax)
        ax.set_xlabel("Total Engagement Frequency", fontsize=12)
        ax.set_ylabel("Number of Pincodes", fontsize=12)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        fig.tight_layout()

        return fig
