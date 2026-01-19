"""
Chart 7: Age Group Distribution - Interactions
Type of Chart: Grouped vertical bar chart
Data Points:
  - demographic.csv: demo_age_5_17, demo_age_17_
  - biometric.csv: bio_age_5_17, bio_age_17_
  - 4 bars: 5-17 (Demo), 18+ (Demo), 5-17 (Bio), 18+ (Bio)
"""
import matplotlib.pyplot as plt
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import AgeGroupAggregator
import config


@register_chart
class Chart07AgeGroupInteractions(BaseChart):

    @property
    def chart_id(self) -> str:
        return "07"

    @property
    def title(self) -> str:
        return "Age Group Distribution - Interactions"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = AgeGroupAggregator()
        age_data = processor.process_interactions(data)

        fig, ax = plt.subplots(figsize=(12, 8))

        # Set up bar positions
        x = np.arange(len(age_data))
        width = 0.6

        # Create bars with different colors for demo vs bio
        colors = [
            config.COLORS["demographic"],  # 5-17 (Demo)
            config.COLORS["demographic"],  # 18+ (Demo)
            config.COLORS["biometric"],    # 5-17 (Bio)
            config.COLORS["biometric"],    # 18+ (Bio)
        ]
        
        bars = ax.bar(
            x,
            age_data["total"],
            width,
            color=colors,
            edgecolor="white",
            linewidth=1.5,
            alpha=0.8
        )

        # Add value labels on top of bars
        for i, (bar, row) in enumerate(zip(bars, age_data.itertuples())):
            height = bar.get_height()
            # Format in millions
            value_text = f"{row.total/1e6:.1f}M"
            percentage_text = f"({row.percentage:.1f}%)"
            
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{value_text}\n{percentage_text}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            )

        self._apply_common_style(ax)
        ax.set_xlabel("Age Group by Service Type", fontsize=12)
        ax.set_ylabel("Total Interactions", fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(age_data["category"], fontsize=10)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x/1e6:.0f}M"))
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=config.COLORS["demographic"], label="Demographic", alpha=0.8),
            Patch(facecolor=config.COLORS["biometric"], label="Biometric", alpha=0.8)
        ]
        ax.legend(handles=legend_elements, loc="upper right", fontsize=10)
        
        fig.tight_layout()

        return fig
