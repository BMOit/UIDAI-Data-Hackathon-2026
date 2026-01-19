"""
Chart 10: Engagement Metrics Correlation
Type of Chart: Heatmap (7x7 matrix)
Data Points:
  - All 3 datasets aggregated by pincode
  - 7 metrics correlated:
    1. total_demo_interactions
    2. total_bio_interactions
    3. total_enrollments
    4. demo_interaction_frequency
    5. bio_interaction_frequency
    6. enrollment_frequency
    7. total_engagement_frequency
  - Pearson correlation between all pairs
"""
import matplotlib.pyplot as plt
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import CorrelationMatrixProcessor
import config


@register_chart
class Chart10CorrelationMatrix(BaseChart):

    @property
    def chart_id(self) -> str:
        return "10"

    @property
    def title(self) -> str:
        return "Engagement Metrics Correlation"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = CorrelationMatrixProcessor()
        corr_matrix = processor.process(data)

        fig, ax = plt.subplots(figsize=(12, 10))

        # Create heatmap
        im = ax.imshow(
            corr_matrix.values,
            cmap="RdBu_r",  # Red-Blue reversed (blue=negative, red=positive)
            aspect="auto",
            vmin=-1,
            vmax=1
        )

        # Set ticks and labels
        ax.set_xticks(np.arange(len(corr_matrix.columns)))
        ax.set_yticks(np.arange(len(corr_matrix.index)))
        ax.set_xticklabels(corr_matrix.columns, fontsize=9)
        ax.set_yticklabels(corr_matrix.index, fontsize=9)

        # Rotate the x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Add correlation values in each cell
        for i in range(len(corr_matrix.index)):
            for j in range(len(corr_matrix.columns)):
                value = corr_matrix.iloc[i, j]
                # Choose text color based on background
                text_color = "white" if abs(value) > 0.5 else "black"
                text = ax.text(
                    j, i, f"{value:.2f}",
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=9,
                    fontweight="bold"
                )

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("Correlation Coefficient", rotation=270, labelpad=20, fontsize=10)
        cbar.ax.tick_params(labelsize=9)

        # Apply common style (but adjust title)
        ax.set_title(self.title, fontsize=14, fontweight="bold", pad=15)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        
        # Add grid
        ax.set_xticks(np.arange(len(corr_matrix.columns)) - 0.5, minor=True)
        ax.set_yticks(np.arange(len(corr_matrix.index)) - 0.5, minor=True)
        ax.grid(which="minor", color="white", linestyle="-", linewidth=2)
        ax.tick_params(which="minor", size=0)

        fig.tight_layout()

        return fig
