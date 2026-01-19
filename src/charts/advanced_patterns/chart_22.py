"""
Chart 22: Activity Intensity by Cluster
Type of Chart: Grouped bar chart
Data Points:
  - Average intensity per visit per cluster
  - Bar 1: Demo/Visit
  - Bar 2: Bio/Visit
  - Bar 3: Enroll/Visit
  - Capped at 95th percentile per column to avoid outlier skew
"""
import matplotlib.pyplot as plt
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor
import config


@register_chart
class Chart22ActivityIntensity(BaseChart):

    @property
    def chart_id(self) -> str:
        return "22"

    @property
    def title(self) -> str:
        return "Activity Intensity by Cluster"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        features_df, _ = processor.process_clusters(data, k=5)

        # Cap at 95th percentile to avoid skewing averages with extreme outliers
        for col in ["demo_intensity", "bio_intensity", "enroll_intensity"]:
            p95 = features_df[col].quantile(0.95)
            # Clip inplace
            features_df[col] = features_df[col].clip(upper=p95)

        # Calculate means per cluster
        means = features_df.groupby("cluster")[
            ["demo_intensity", "bio_intensity", "enroll_intensity"]
        ].mean()

        fig, ax = plt.subplots(figsize=(12, 8))

        clusters = means.index
        x = np.arange(len(clusters))
        width = 0.25

        ax.bar(x - width, means["demo_intensity"], width, label="Demo/Visit", color=config.COLORS["demographic"])
        ax.bar(x, means["bio_intensity"], width, label="Bio/Visit", color=config.COLORS["biometric"])
        ax.bar(x + width, means["enroll_intensity"], width, label="Enroll/Visit", color=config.COLORS["enrollment"])

        self._apply_common_style(ax)
        ax.set_xlabel("Cluster ID", fontsize=12)
        ax.set_ylabel("Average Interactions per Visit", fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([str(c) for c in clusters])
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
        
        fig.tight_layout()

        return fig
