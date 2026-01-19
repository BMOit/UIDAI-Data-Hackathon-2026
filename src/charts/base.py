"""Base class for all chart implementations."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt

from src.data_loader import DataLoader
import config


class BaseChart(ABC):

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self._data_loader = data_loader or DataLoader()

    @property
    def data_loader(self) -> DataLoader:
        return self._data_loader

    @property
    @abstractmethod
    def chart_id(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    def filename(self) -> str:
        safe_title = self.title.lower().replace(" ", "_").replace("-", "_")
        return f"chart_{self.chart_id}_{safe_title}.png"

    @property
    def output_path(self) -> Path:
        return config.CHARTS_OUTPUT_DIR / self.filename

    @abstractmethod
    def generate(self) -> plt.Figure:
        pass

    def save(self, fig: Optional[plt.Figure] = None) -> Path:
        if fig is None:
            fig = self.generate()

        fig.text(
            0.99, 0.01,
            "github.com/BMOit",
            transform=fig.transFigure,
            fontsize=9,
            color="gray",
            alpha=0.7,
            ha="right",
            va="bottom"
        )

        config.CHARTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            self.output_path,
            dpi=config.FIGURE_DPI,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none"
        )
        plt.close(fig)

        return self.output_path

    def _apply_common_style(self, ax: plt.Axes) -> None:
        ax.set_title(self.title, fontsize=14, fontweight="bold", pad=15)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(labelsize=10)
