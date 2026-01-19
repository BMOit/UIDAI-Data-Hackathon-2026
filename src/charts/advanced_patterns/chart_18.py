"""
Chart 18: Engagement Personas (PCA)
Type of Chart: 2D scatter plot
Data Points:
  - Processed features reduced to 2D
  - X-axis: PC1
  - Y-axis: PC2
  - Color: Cluster ID
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor
import config


@register_chart
class Chart18EngagementPersonas(BaseChart):

    @property
    def chart_id(self) -> str:
        return "18"

    @property
    def title(self) -> str:
        return "Engagement Personas (PCA)"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        _, pca_data = processor.process_clusters(data, k=5)

        fig, ax = plt.subplots(figsize=(12, 10))

        # Scatter plot
        scatter = ax.scatter(
            pca_data["PC1"],
            pca_data["PC2"],
            c=pca_data["cluster"],
            cmap="viridis",
            alpha=0.6,
            edgecolor="none",
            s=20
        )

        # Legend
        legend1 = ax.legend(*scatter.legend_elements(), title="Clusters", loc="upper right")
        ax.add_artist(legend1)

        self._apply_common_style(ax)
        ax.set_xlabel("Principal Component 1 (~45% Variance)", fontsize=12)
        ax.set_ylabel("Principal Component 2 (~25% Variance)", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()

        return fig
