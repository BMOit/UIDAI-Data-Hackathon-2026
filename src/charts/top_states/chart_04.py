"""
Chart 4: Top 15 States - New Enrollments
Type of Chart: Horizontal bar chart
Data Points:
  - enrollment.csv: state, age_0_5, age_5_17, age_18_greater
  - Calculation: SUM(age_0_5 + age_5_17 + age_18_greater) GROUP BY state, TOP 15
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import StateAggregator
import config


@register_chart
class Chart04TopStatesEnrollment(BaseChart):

    @property
    def chart_id(self) -> str:
        return "04"

    @property
    def title(self) -> str:
        return "Top 15 States - New Enrollments"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = StateAggregator()
        state_data = processor.process(data, dataset="enrollment", top_n=15)

        fig, ax = plt.subplots(figsize=(12, 8))

        bars = ax.barh(
            state_data["state"],
            state_data["total"],
            color=config.COLORS["enrollment"],
            edgecolor="white",
            linewidth=0.5
        )

        for bar, value in zip(bars, state_data["total"]):
            ax.text(
                value + state_data["total"].max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{value:,.0f}",
                va="center",
                fontsize=9
            )

        self._apply_common_style(ax)
        ax.set_xlabel("Total New Enrollments", fontsize=12)
        ax.set_ylabel("State", fontsize=12)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e3:.0f}K"))
        ax.set_xlim(0, state_data["total"].max() * 1.15)
        fig.tight_layout()

        return fig
