"""
Chart 25: High-Value User Analysis
Type of Chart: Dual-axis bar chart
Data Points:
  - 3 user types:
    1. High Frequency (>= 95th percentile frequency)
    2. Balanced Engagers (>= 90th percentile balance)
    3. All Pincodes
  - Left Y-axis (blue bars): Count of pincodes
  - Right Y-axis (red bars/line): Average Engagement Score
"""
import matplotlib.pyplot as plt
import numpy as np

from src.charts import register_chart
from src.charts.base import BaseChart
from src.processors import ClusteringProcessor


@register_chart
class Chart25HighValueUsers(BaseChart):

    @property
    def chart_id(self) -> str:
        return "25"

    @property
    def title(self) -> str:
        return "High-Value User Analysis"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        processor = ClusteringProcessor()
        features_df, _ = processor.process_clusters(data, k=5)

        # Define segments
        freq_p95 = features_df["total_freq"].quantile(0.95)
        bal_p90 = features_df["balance_score"].quantile(0.90)

        high_freq = features_df[features_df["total_freq"] >= freq_p95]
        balanced = features_df[features_df["balance_score"] >= bal_p90]
        all_pincodes = features_df

        datasets = [high_freq, balanced, all_pincodes]
        labels = ["High Frequency\n(Top 5%)", "Balanced\n(Top 10%)", "All Pincodes"]

        counts = [len(d) for d in datasets]
        scores = [d["engagement_score"].mean() for d in datasets]

        fig, ax1 = plt.subplots(figsize=(10, 8))
        ax2 = ax1.twinx()

        x = np.arange(len(labels))
        width = 0.4

        # Bar chart for counts (Left Axis)
        bars = ax1.bar(
            x - width/2,
            counts,
            width,
            color="#1f77b4",
            alpha=0.7,
            label="Pincode Count"
        )

        # Bar chart for scores (Right Axis) - aligned right
        bars2 = ax2.bar(
            x + width/2,
            scores,
            width,
            color="#d62728",
            alpha=0.7,
            label="Avg Engagement Score"
        )

        # Value labels for counts
        for bar, value in zip(bars, counts):
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:,}",
                ha="center",
                va="bottom",
                color="#1f77b4",
                fontweight="bold"
            )

        # Value labels for scores
        for bar, value in zip(bars2, scores):
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:.1f}",
                ha="center",
                va="bottom",
                color="#d62728",
                fontweight="bold"
            )

        self._apply_common_style(ax1)
        ax1.set_xlabel("User Segment", fontsize=12)
        ax1.set_ylabel("Number of Pincodes", color="#1f77b4", fontsize=12)
        ax1.tick_params(axis='y', labelcolor="#1f77b4")
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels)
        
        ax2.set_ylabel("Average Engagement Score", color="#d62728", fontsize=12)
        ax2.tick_params(axis='y', labelcolor="#d62728")
        ax2.spines["right"].set_visible(True) # Make right spine visible for right axis

        # Combined legend
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper center")

        fig.tight_layout()

        return fig
