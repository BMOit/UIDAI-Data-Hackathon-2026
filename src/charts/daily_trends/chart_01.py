"""
Chart 1: Daily Aadhaar Engagement Trends
Type of Chart: Line chart
Data Points:
  - demographic.csv: date, demo_age_5_17, demo_age_17_
  - biometric.csv: date, bio_age_5_17, bio_age_17_
  - enrollment.csv: date, age_0_5, age_5_17, age_18_greater
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import DailyAggregator
import config


@register_chart
class Chart01DailyTrends(BaseChart):

    @property
    def chart_id(self) -> str:
        return "01"

    @property
    def title(self) -> str:
        return "Daily Aadhaar Engagement Trends"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = DailyAggregator()
        daily_data = processor.process(data)

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.plot(
            daily_data["date"],
            daily_data["demo_total"],
            color=config.COLORS["demographic"],
            linewidth=2,
            label="Demographic Updates",
            marker="o",
            markersize=3,
            alpha=0.8
        )

        ax.plot(
            daily_data["date"],
            daily_data["bio_total"],
            color=config.COLORS["biometric"],
            linewidth=2,
            label="Biometric Updates",
            marker="s",
            markersize=3,
            alpha=0.8
        )

        ax.plot(
            daily_data["date"],
            daily_data["enroll_total"],
            color=config.COLORS["enrollment"],
            linewidth=2,
            label="New Enrollments",
            marker="^",
            markersize=3,
            alpha=0.8
        )

        self._apply_common_style(ax)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Total Count", fontsize=12)
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
        ax.legend(loc="upper right", frameon=True, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:,.0f}"))
        fig.tight_layout()

        return fig
