"""
Chart 9: Weekly Pattern - Demographic Interactions
Type of Chart: Vertical bar chart
Data Points:
  - demographic.csv: date, demo_age_5_17, demo_age_17_
  - Extract weekday from date
  - Calculate average daily interactions per weekday
  - 7 bars (Monday through Sunday)
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import WeeklyPatternProcessor
import config


@register_chart
class Chart09WeeklyPattern(BaseChart):

    @property
    def chart_id(self) -> str:
        return "09"

    @property
    def title(self) -> str:
        return "Weekly Pattern - Demographic Interactions"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = WeeklyPatternProcessor()
        weekly_data = processor.process(data)

        fig, ax = plt.subplots(figsize=(12, 8))

        # Create bars with gradient color (darker on weekdays, lighter on weekends)
        colors = [
            config.COLORS["demographic"],  # Monday
            config.COLORS["demographic"],  # Tuesday
            config.COLORS["demographic"],  # Wednesday
            config.COLORS["demographic"],  # Thursday
            config.COLORS["demographic"],  # Friday
            "#7fb3d5",  # Saturday (lighter)
            "#7fb3d5",  # Sunday (lighter)
        ]
        
        bars = ax.bar(
            weekly_data["weekday_name"],
            weekly_data["avg_interactions"],
            color=colors,
            edgecolor="white",
            linewidth=1.5,
            alpha=0.8,
            width=0.7
        )

        # Add value labels on top of bars
        for bar, value in zip(bars, weekly_data["avg_interactions"]):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{value:,.0f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            )

        self._apply_common_style(ax)
        ax.set_xlabel("Day of Week", fontsize=12)
        ax.set_ylabel("Average Daily Interactions", fontsize=12)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e3:.0f}K" if x >= 1000 else f"{x:.0f}"))
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        # Rotate x-axis labels slightly for better readability
        ax.tick_params(axis='x', rotation=0)
        
        # Add note about weekend pattern
        max_val = weekly_data["avg_interactions"].max()
        min_val = weekly_data["avg_interactions"].min()
        variation = ((max_val - min_val) / max_val * 100)
        
        note_text = f"Weekend activity is {variation:.0f}% lower than peak weekday"
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
