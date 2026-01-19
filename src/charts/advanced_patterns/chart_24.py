"""
Chart 24: Engagement Specialists
Type of Chart: Vertical bar chart
Data Points:
  - Count of pincodes specializing in one type (> 70% ratio)
  - Bar 1: Demo Specialists (demo_ratio > 0.7)
  - Bar 2: Bio Specialists (bio_ratio > 0.7)
  - Bar 3: Enroll Specialists (enroll_ratio > 0.7)
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor
import config


@register_chart
class Chart24Specialists(BaseChart):

    @property
    def chart_id(self) -> str:
        return "24"

    @property
    def title(self) -> str:
        return "Engagement Specialists"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        features_df, _ = processor.process_clusters(data, k=5)

        # Count specialists
        demo_specs = (features_df["demo_ratio"] > 0.7).sum()
        bio_specs = (features_df["bio_ratio"] > 0.7).sum()
        enroll_specs = (features_df["enroll_ratio"] > 0.7).sum()

        counts = [demo_specs, bio_specs, enroll_specs]
        labels = ["Demo\nSpecialists", "Bio\nSpecialists", "Enroll\nSpecialists"]
        colors = [config.COLORS["demographic"], config.COLORS["biometric"], config.COLORS["enrollment"]]

        fig, ax = plt.subplots(figsize=(10, 8))

        bars = ax.bar(
            labels,
            counts,
            color=colors,
            edgecolor="white",
            linewidth=1.5,
            width=0.6,
            alpha=0.9
        )

        # Labels
        for bar, value in zip(bars, counts):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:,}",
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold"
            )

        self._apply_common_style(ax)
        ax.set_ylabel("Number of Pincodes", fontsize=12)
        ax.set_ylim(0, max(counts) * 1.15)
        ax.grid(axis="y", alpha=0.3)
        
        # Note
        note = "Specialist defined as >70% of total interactions from a single type"
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
