"""
Chart 19: Cluster Size Distribution
Type of Chart: Vertical bar chart
Data Points:
  - Cluster assignments
  - 5 bars (one per cluster)
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor


@register_chart
class Chart19ClusterSize(BaseChart):

    @property
    def chart_id(self) -> str:
        return "19"

    @property
    def title(self) -> str:
        return "Cluster Size Distribution"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        features_df, _ = processor.process_clusters(data, k=5)

        cluster_counts = features_df["cluster"].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(10, 8))

        # Colors from viridis to match PCA
        colors = cm.viridis(np.linspace(0, 1, 5))

        bars = ax.bar(
            cluster_counts.index.astype(str),
            cluster_counts.values,
            color=colors,
            edgecolor="white",
            linewidth=1.0,
            alpha=0.9
        )

        # Labels
        total = cluster_counts.sum()
        for bar, value in zip(bars, cluster_counts.values):
            pct = value / total * 100
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:,}\n({pct:.1f}%)",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold"
            )

        self._apply_common_style(ax)
        ax.set_xlabel("Cluster ID", fontsize=12)
        ax.set_ylabel("Number of Pincodes", fontsize=12)
        ax.grid(axis="y", alpha=0.3)
        
        fig.tight_layout()

        return fig
