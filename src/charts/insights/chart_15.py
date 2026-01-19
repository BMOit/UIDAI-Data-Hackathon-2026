"""
Chart 15: Engagement Trends Over Time (Area)
Type of Chart: Area chart (3 overlapping areas)
Data Points:
  - Same as Chart 1 but with filled areas instead of lines
  - Area 1: demo_daily total over time
  - Area 2: bio_daily total over time
  - Area 3: enroll_daily total over time
"""
import matplotlib.pyplot as plt
import pandas as pd

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import DailyAggregator
import config


@register_chart
class Chart15EngagementTrendsArea(BaseChart):

    @property
    def chart_id(self) -> str:
        return "15"

    @property
    def title(self) -> str:
        return "Engagement Trends Over Time"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = DailyAggregator()
        
        # DailyAggregator returns a single dataframe with all metrics
        daily_data = processor.process(data)
        
        # Ensure date is datetime for plotting
        daily_data["date"] = pd.to_datetime(daily_data["date"], format="%d-%m-%Y")
        daily_data = daily_data.sort_values("date")

        fig, ax = plt.subplots(figsize=(14, 8))

        # Create area charts with transparency
        ax.fill_between(
            daily_data["date"],
            daily_data["demo_total"],
            alpha=0.4,
            label="Demographic",
            color=config.COLORS["demographic"]
        )
        
        ax.fill_between(
            daily_data["date"],
            daily_data["bio_total"],
            alpha=0.4,
            label="Biometric",
            color=config.COLORS["biometric"]
        )
        
        ax.fill_between(
            daily_data["date"],
            daily_data["enroll_total"],
            alpha=0.4,
            label="Enrollment",
            color=config.COLORS["enrollment"]
        )

        self._apply_common_style(ax)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Daily Engagements", fontsize=12)
        ax.legend(loc="upper left", fontsize=10)
        ax.grid(axis="both", alpha=0.3, linestyle="--")
        
        # Format x-axis dates
        ax.tick_params(axis='x', rotation=45)
        fig.autofmt_xdate()
        
        # Format y-axis
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e3:.0f}K"))
        
        fig.tight_layout()

        return fig
