"""
Chart 8: Age Group Distribution - Enrollments
Type of Chart: Vertical bar chart
Data Points:
  - enrollment.csv: age_0_5, age_5_17, age_18_greater
  - 3 bars: 0-5, 5-17, 18+
"""
import matplotlib.pyplot as plt
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import AgeGroupAggregator
import config


@register_chart
class Chart08AgeGroupEnrollments(BaseChart):

    @property
    def chart_id(self) -> str:
        return "08"

    @property
    def title(self) -> str:
        return "Age Group Distribution - Enrollments"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = AgeGroupAggregator()
        age_data = processor.process_enrollments(data)

        fig, ax = plt.subplots(figsize=(10, 8))

        # Create bars
        bars = ax.bar(
            age_data["age_group"],
            age_data["total"],
            color=config.COLORS["enrollment"],
            edgecolor="white",
            linewidth=1.5,
            alpha=0.8,
            width=0.6
        )

        # Add value labels on top of bars
        for bar, row in zip(bars, age_data.itertuples()):
            height = bar.get_height()
            # Format in thousands or millions
            if row.total >= 1e6:
                value_text = f"{row.total/1e6:.2f}M"
            else:
                value_text = f"{row.total/1e3:.0f}K"
            
            percentage_text = f"({row.percentage:.1f}%)"
            
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{value_text}\n{percentage_text}",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold"
            )

        self._apply_common_style(ax)
        ax.set_xlabel("Age Group", fontsize=12)
        ax.set_ylabel("Total Enrollments", fontsize=12)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e6:.1f}M" if x >= 1e6 else f"{x/1e3:.0f}K"))
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        fig.tight_layout()

        return fig
