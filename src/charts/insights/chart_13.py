"""
Chart 13: Overall Engagement Distribution
Type of Chart: Pie chart
Data Points:
  - 3 slices:
    - Demographic Interactions: SUM(all demo_age_5_17 + demo_age_17_)
    - Biometric Interactions: SUM(all bio_age_5_17 + bio_age_17_)
    - New Enrollments: SUM(all age_0_5 + age_5_17 + age_18_greater)
"""
import matplotlib.pyplot as plt

from src.charts import register_chart
from src.charts.base import BaseChart
import config


@register_chart
class Chart13OverallDistribution(BaseChart):

    @property
    def chart_id(self) -> str:
        return "13"

    @property
    def title(self) -> str:
        return "Overall Engagement Distribution"

    def generate(self) -> plt.Figure:
        data = self.data_loader.get_all_data()
        
        # Calculate totals
        demo_total = (
            data["demographic"]["demo_age_5_17"].sum() + 
            data["demographic"]["demo_age_17_"].sum()
        )
        
        bio_total = (
            data["biometric"]["bio_age_5_17"].sum() + 
            data["biometric"]["bio_age_17_"].sum()
        )
        
        enroll_total = (
            data["enrollment"]["age_0_5"].sum() + 
            data["enrollment"]["age_5_17"].sum() + 
            data["enrollment"]["age_18_greater"].sum()
        )
        
        totals = [demo_total, bio_total, enroll_total]
        labels = ["Demographic\nInteractions", "Biometric\nInteractions", "New\nEnrollments"]
        colors = [
            config.COLORS["demographic"],
            config.COLORS["biometric"],
            config.COLORS["enrollment"]
        ]

        fig, ax = plt.subplots(figsize=(10, 8))

        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            totals,
            labels=labels,
            colors=colors,
            autopct=lambda pct: f"{pct:.1f}%",
            startangle=90,
            explode=(0.05, 0.05, 0.05),
            textprops={"fontsize": 11, "fontweight": "bold"}
        )
        
        # Add value labels
        grand_total = sum(totals)
        for i, (wedge, total) in enumerate(zip(wedges, totals)):
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = 1.3 * wedge.r * plt.np.cos(plt.np.deg2rad(angle))
            y = 1.3 * wedge.r * plt.np.sin(plt.np.deg2rad(angle))
            
            value_text = f"{total/1e6:.1f}M"
            ax.text(
                x, y,
                value_text,
                ha="center",
                va="center",
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", alpha=0.8)
            )

        # Make percentage text white
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(12)

        ax.set_title(self.title, fontsize=14, fontweight="bold", pad=20)
        
        fig.tight_layout()

        return fig
