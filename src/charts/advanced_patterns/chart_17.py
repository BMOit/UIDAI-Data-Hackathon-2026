"""
Chart 17: Elbow Method for Optimal Clusters
Type of Chart: Line chart
Data Points:
  - Processed engagement features
  - X-axis: Number of clusters (k = 2 to 10)
  - Y-axis: Inertia (within-cluster sum of squares)
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor


@register_chart
class Chart17ElbowMethod(BaseChart):

    @property
    def chart_id(self) -> str:
        return "17"

    @property
    def title(self) -> str:
        return "Elbow Method for Optimal Clusters"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        elbow_data = processor.process_elbow(data)

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(
            elbow_data["k"],
            elbow_data["inertia"],
            marker="o",
            linestyle="-",
            color="black",
            linewidth=2,
            markersize=8
        )

        # Highlight k=5
        k_opt = 5
        inertia_opt = elbow_data.loc[elbow_data["k"] == k_opt, "inertia"].values[0]
        
        ax.plot([k_opt], [inertia_opt], marker="o", color="red", markersize=10)
        ax.axvline(x=k_opt, color="red", linestyle="--", alpha=0.5)
        
        ax.annotate(
            f"Selected k={k_opt}",
            xy=(k_opt, inertia_opt),
            xytext=(k_opt + 1, inertia_opt * 1.1),
            arrowprops=dict(arrowstyle="->", color="red"),
            color="red",
            fontsize=11
        )

        self._apply_common_style(ax)
        ax.set_xlabel("Number of Clusters (k)", fontsize=12)
        ax.set_ylabel("Inertia", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()

        return fig
