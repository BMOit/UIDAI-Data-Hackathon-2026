"""
Chart 11: Monthly Engagement Comparison
Type of Chart: Grouped bar chart
Data Points:
  - All 3 datasets
  - For each month (March-December 2025):
    - Bar 1: Demographic total
    - Bar 2: Biometric total
    - Bar 3: Enrollment total
"""
import matplotlib.pyplot as plt
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import MonthlyAggregator
import config


@register_chart
class Chart11MonthlyComparison(BaseChart):

    @property
    def chart_id(self) -> str:
        return "11"

    @property
    def title(self) -> str:
        return "Monthly Engagement Comparison"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = MonthlyAggregator()
        monthly_data = processor.process(data)

        fig, ax = plt.subplots(figsize=(14, 8))

        # Set up bar positions
        x = np.arange(len(monthly_data))
        width = 0.25

        # Create grouped bars
        bars1 = ax.bar(
            x - width,
            monthly_data["demographic"],
            width,
            label="Demographic",
            color=config.COLORS["demographic"],
            edgecolor="white",
            linewidth=0.5
        )
        
        bars2 = ax.bar(
            x,
            monthly_data["biometric"],
            width,
            label="Biometric",
            color=config.COLORS["biometric"],
            edgecolor="white",
            linewidth=0.5
        )
        
        bars3 = ax.bar(
            x + width,
            monthly_data["enrollment"],
            width,
            label="Enrollment",
            color=config.COLORS["enrollment"],
            edgecolor="white",
            linewidth=0.5
        )

        self._apply_common_style(ax)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Total Engagements", fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(monthly_data["month_str"], rotation=45, ha="right")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e6:.1f}M"))
        ax.legend(loc="upper left", fontsize=10)
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        fig.tight_layout()

        return fig
