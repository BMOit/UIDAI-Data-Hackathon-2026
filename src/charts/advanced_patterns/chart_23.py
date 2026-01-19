"""
Chart 23: Engagement Balance Distribution
Type of Chart: Histogram
Data Points:
  - X-axis: Balance score (0 to 1, binned)
  - Y-axis: Count of pincodes
  - Balance score = 1 - std_dev([demo_ratio, bio_ratio, enroll_ratio])
  - Vertical line at 90th percentile
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor
import config


@register_chart
class Chart23BalanceDistribution(BaseChart):

    @property
    def chart_id(self) -> str:
        return "23"

    @property
    def title(self) -> str:
        return "Engagement Balance Distribution"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        # We don't strictly need clusters but the processor provides the comprehensive dataframe
        features_df, _ = processor.process_clusters(data, k=5)

        fig, ax = plt.subplots(figsize=(10, 8))

        # Histogram
        ax.hist(
            features_df["balance_score"],
            bins=50,
            range=(0, 1),
            color=config.COLORS.get("primary", "#9467bd"),
            edgecolor="white",
            linewidth=0.5,
            alpha=0.8
        )

        # 90th percentile line
        p90 = features_df["balance_score"].quantile(0.90)
        ax.axvline(x=p90, color="red", linestyle="--", linewidth=1.5, label=f"90th %ile ({p90:.2f})")
        
        ax.annotate(
            "Balanced Engagers Threshold",
            xy=(p90, ax.get_ylim()[1]*0.8),
            xytext=(p90 - 0.2, ax.get_ylim()[1]*0.8),
            arrowprops=dict(arrowstyle="->", color="black"),
            fontsize=10
        )

        self._apply_common_style(ax)
        ax.set_xlabel("Balance Score (Higher = More Balanced)", fontsize=12)
        ax.set_ylabel("Number of Pincodes", fontsize=12)
        ax.legend(loc="upper left")
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        
        # Note
        note = "Balance = 1 - Standard Deviation of Engagement Ratios"
        ax.text(
            0.5, -0.12,
            note,
            transform=ax.transAxes,
            fontsize=9,
            ha="center",
            style="italic",
            color="gray"
        )

        fig.tight_layout()

        return fig
