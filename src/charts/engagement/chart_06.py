"""
Chart 6: Pincodes by Engagement Diversity
Type of Chart: Vertical bar chart
Data Points:
  - All 3 datasets aggregated by pincode
  - X-axis: Number of engagement types (0, 1, 2, or 3)
  - Y-axis: Count of pincodes
  - Shows how many pincodes have 1, 2, or 3 different types of engagement
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import EngagementDiversityProcessor
import config


@register_chart
class Chart06EngagementDiversity(BaseChart):

    @property
    def chart_id(self) -> str:
        return "06"

    @property
    def title(self) -> str:
        return "Pincodes by Engagement Diversity"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = EngagementDiversityProcessor()
        diversity_data = processor.process(data)

        fig, ax = plt.subplots(figsize=(10, 8))

        # Create labels for x-axis
        labels = [f"{int(count)} Type{'s' if count != 1 else ''}" 
                  for count in diversity_data["type_count"]]
        
        # Create bars
        bars = ax.bar(
            labels,
            diversity_data["pincode_count"],
            color=config.COLORS["primary"],
            edgecolor="white",
            linewidth=1.5,
            alpha=0.8
        )

        # Add value labels on top of bars and percentage
        total_pincodes = diversity_data["pincode_count"].sum()
        for bar, value in zip(bars, diversity_data["pincode_count"]):
            height = bar.get_height()
            percentage = (value / total_pincodes) * 100
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{value:,}\n({percentage:.1f}%)",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold"
            )

        self._apply_common_style(ax)
        ax.set_xlabel("Number of Engagement Types", fontsize=12)
        ax.set_ylabel("Number of Pincodes", fontsize=12)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e3:.0f}K" if x >= 1000 else f"{x:.0f}"))
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        # Add a note about what this means
        note_text = "Engagement types: Demographic, Biometric, Enrollment"
        ax.text(
            0.5, -0.12,
            note_text,
            transform=ax.transAxes,
            fontsize=9,
            ha="center",
            style="italic",
            color="gray"
        )
        
        fig.tight_layout()

        return fig
