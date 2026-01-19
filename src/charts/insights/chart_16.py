"""
Chart 16: Engagement Intensity Distribution
Type of Chart: Histogram
Data Points:
  - Processed engagement data
  - X-axis: Intensity score (binned)
  - Y-axis: Count of pincodes
  - Intensity score = (total_demo * 0.3 + total_bio * 0.4 + total_enroll * 0.3) / total_frequency
  - Filter: <= 95th percentile
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import IntensityProcessor
import config


@register_chart
class Chart16EngagementIntensity(BaseChart):

    @property
    def chart_id(self) -> str:
        return "16"

    @property
    def title(self) -> str:
        return "Engagement Intensity Distribution"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = IntensityProcessor()
        intensity_data = processor.process(data)

        fig, ax = plt.subplots(figsize=(12, 8))

        # Create histogram
        n, bins, patches = ax.hist(
            intensity_data["intensity_score"],
            bins=50,
            color=config.COLORS.get("primary", "#9467bd"), # Fallback to purple if not set
            edgecolor="white",
            linewidth=0.5,
            alpha=0.8
        )

        # Add stats
        mean_val = intensity_data["intensity_score"].mean()
        median_val = intensity_data["intensity_score"].median()
        p95 = intensity_data["intensity_score"].max()

        stats_text = (
            f"Mean: {mean_val:.2f}\n"
            f"Median: {median_val:.2f}\n"
            f"95th %ile: {p95:.2f}"
        )
        
        ax.text(
            0.95, 0.95,
            stats_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray")
        )

        self._apply_common_style(ax)
        ax.set_xlabel("Engagement Intensity Score", fontsize=12)
        ax.set_ylabel("Number of Pincodes", fontsize=12)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        # Explain formula
        note = "Score = (0.3×Demo + 0.4×Bio + 0.3×Enroll) / Frequency"
        ax.text(
            0.5, -0.12,
            note,
            transform=ax.transAxes,
            fontsize=9,
            ha="center",
            style="italic",
            color="gray"
        )
        
        fig.tight_layout()

        return fig
