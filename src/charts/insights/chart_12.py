"""
Chart 12: Engagement Level Distribution
Type of Chart: Vertical bar chart
Data Points:
  - 3 bars:
    - Low (Q1): pincodes with frequency <= 25th percentile
    - Medium (Q2-Q3): pincodes between 25th-75th percentile
    - High (Q4): pincodes with frequency > 75th percentile
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import EngagementLevelProcessor
import config


@register_chart
class Chart12EngagementLevel(BaseChart):

    @property
    def chart_id(self) -> str:
        return "12"

    @property
    def title(self) -> str:
        return "Engagement Level Distribution"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = EngagementLevelProcessor()
        level_data = processor.process(data)

        fig, ax = plt.subplots(figsize=(10, 8))

        # Color scheme for levels
        colors = ["#d62728", "#ff7f0e", "#2ca02c"]  # Red, Orange, Green
        
        bars = ax.bar(
            level_data["level"],
            level_data["count"],
            color=colors,
            edgecolor="white",
            linewidth=1.5,
            alpha=0.8,
            width=0.6
        )

        # Add value labels on top of bars
        total = level_data["count"].sum()
        for bar, value in zip(bars, level_data["count"]):
            height = bar.get_height()
            percentage = (value / total) * 100
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
        ax.set_xlabel("Engagement Level", fontsize=12)
        ax.set_ylabel("Number of Pincodes", fontsize=12)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e3:.0f}K" if x >= 1000 else f"{x:.0f}"))
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        fig.tight_layout()

        return fig
