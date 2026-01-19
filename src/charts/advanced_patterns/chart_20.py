"""
Chart 20: Engagement Type by Cluster
Type of Chart: Grouped bar chart
Data Points:
  - Average demo_ratio, bio_ratio, enroll_ratio per cluster
"""
import matplotlib.pyplot as plt
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor
import config


@register_chart
class Chart20ClusterComposition(BaseChart):

    @property
    def chart_id(self) -> str:
        return "20"

    @property
    def title(self) -> str:
        return "Engagement Type by Cluster"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        features_df, _ = processor.process_clusters(data, k=5)

        # Calculate average ratios per cluster
        means = features_df.groupby("cluster")[["demo_ratio", "bio_ratio", "enroll_ratio"]].mean()

        fig, ax = plt.subplots(figsize=(12, 8))

        clusters = means.index
        x = np.arange(len(clusters))
        width = 0.25

        ax.bar(x - width, means["demo_ratio"], width, label="Demographic", color=config.COLORS["demographic"])
        ax.bar(x, means["bio_ratio"], width, label="Biometric", color=config.COLORS["biometric"])
        ax.bar(x + width, means["enroll_ratio"], width, label="Enrollment", color=config.COLORS["enrollment"])

        self._apply_common_style(ax)
        ax.set_xlabel("Cluster ID", fontsize=12)
        ax.set_ylabel("Average Ratio", fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([str(c) for c in clusters])
        ax.legend(title="Engagement Type")
        ax.set_ylim(0, 1.1)  # Ratios are 0-1
        ax.grid(axis="y", alpha=0.3)
        
        fig.tight_layout()

        return fig
