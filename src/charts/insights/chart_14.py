"""
Chart 14: Top 20 Districts - Demographic Interactions
Type of Chart: Horizontal bar chart
Data Points:
  - demographic.csv: state, district, demo_age_5_17, demo_age_17_
  - Calculation: SUM(demo_age_5_17 + demo_age_17_) GROUP BY (state, district), TOP 20
  - Label format: "District, StateAbbr"
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import DistrictAggregator
import config


@register_chart
class Chart14TopDistricts(BaseChart):

    @property
    def chart_id(self) -> str:
        return "14"

    @property
    def title(self) -> str:
        return "Top 20 Districts - Demographic Interactions"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = DistrictAggregator()
        district_data = processor.process(data, dataset="demographic", top_n=20)

        fig, ax = plt.subplots(figsize=(12, 10))

        bars = ax.barh(
            district_data["district_label"],
            district_data["total"],
            color=config.COLORS["demographic"],
            edgecolor="white",
            linewidth=0.5
        )

        # Add value labels
        for bar, value in zip(bars, district_data["total"]):
            ax.text(
                value + district_data["total"].max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{value:,.0f}",
                va="center",
                fontsize=8
            )

        self._apply_common_style(ax)
        ax.set_xlabel("Total Demographic Interactions", fontsize=12)
        ax.set_ylabel("District", fontsize=12)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e3:.0f}K"))
        ax.set_xlim(0, district_data["total"].max() * 1.15)
        ax.tick_params(axis='y', labelsize=9)
        
        fig.tight_layout()

        return fig
