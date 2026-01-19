"""
Chart 21: Engagement Score by Cluster
Type of Chart: Overlapping histograms
Data Points:
  - 5 overlapping histograms (one per cluster)
  - X-axis: Engagement score (binned)
  - Y-axis: Frequency
  - Filter: <= 95th percentile
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor


@register_chart
class Chart21EngagementScore(BaseChart):

    @property
    def chart_id(self) -> str:
        return "21"

    @property
    def title(self) -> str:
        return "Engagement Score by Cluster"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        # k=5 matches Chart 19/20
        features_df, _ = processor.process_clusters(data, k=5)

        # Filter to 95th percentile to remove outliers
        p95 = features_df["engagement_score"].quantile(0.95)
        filtered_df = features_df[features_df["engagement_score"] <= p95]

        fig, ax = plt.subplots(figsize=(12, 8))

        # Colors
        colors = cm.viridis(np.linspace(0, 1, 5))

        # Plot histogram for each cluster
        bins = np.linspace(0, p95, 40)
        
        for cluster_id in sorted(filtered_df["cluster"].unique()):
            cluster_data = filtered_df[filtered_df["cluster"] == cluster_id]
            
            ax.hist(
                cluster_data["engagement_score"],
                bins=bins,
                alpha=0.5,
                label=f"Cluster {cluster_id}",
                color=colors[cluster_id],
                edgecolor="white",
                linewidth=0.5
            )

        self._apply_common_style(ax)
        ax.set_xlabel("Engagement Score", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.legend(title="Cluster ID")
        ax.grid(axis="y", alpha=0.3)
        
        # Add formula note
        note = "Score = (0.2×Demo + 0.4×Bio + 0.4×Enroll)"
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
