"""Base class for all chart implementations."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List, Union
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from scour import scour

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
    def svg_filename(self) -> str:
        safe_title = self.title.lower().replace(" ", "_").replace("-", "_")
        return f"chart_{self.chart_id}_{safe_title}.svg"

    @property
    def output_path(self) -> Path:
        return config.CHARTS_OUTPUT_DIR / self.filename

    @property
    def svg_output_path(self) -> Path:
        return config.CHARTS_SVG_OUTPUT_DIR / self.svg_filename

    @abstractmethod
    def generate(self) -> plt.Figure:
        pass

    def save(
        self,
        fig: Optional[plt.Figure] = None,
        formats: Union[str, List[str]] = "png"
    ) -> Union[Path, List[Path]]:
        """Save the chart in specified format(s).

        Args:
            fig: Matplotlib figure (generates if None)
            formats: 'png', 'svg', 'both', or list like ['png', 'svg']

        Returns:
            Single Path or list of Paths for saved files
        """
        if fig is None:
            fig = self.generate()

        self._add_watermark(fig)

        if formats == "both":
            format_list = ["png", "svg"]
        elif isinstance(formats, str):
            format_list = [formats]
        else:
            format_list = formats

        output_paths = []

        for fmt in format_list:
            if fmt == "png":
                path = self._save_png(fig)
            elif fmt == "svg":
                path = self._save_svg(fig)
            else:
                raise ValueError(f"Unsupported format: {fmt}")
            output_paths.append(path)

        plt.close(fig)

        return output_paths[0] if len(output_paths) == 1 else output_paths

    def _add_watermark(self, fig: plt.Figure) -> None:
        """Add watermark text to figure."""
        fig.text(
            0.99, 0.01,
            config.CHART_AUTHOR,
            transform=fig.transFigure,
            fontsize=9,
            color="gray",
            alpha=0.7,
            ha="right",
            va="bottom"
        )

    def _save_png(self, fig: plt.Figure) -> Path:
        """Save figure as PNG with metadata."""
        config.CHARTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            self.output_path,
            dpi=config.FIGURE_DPI,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none"
        )

        self._add_png_metadata()
        return self.output_path

    def _add_png_metadata(self) -> None:
        """Add metadata to PNG file."""
        img = Image.open(self.output_path)
        metadata = PngInfo()
        metadata.add_text("Author", config.CHART_AUTHOR)
        metadata.add_text("Title", self.title)
        metadata.add_text("Software", config.CHART_SOFTWARE)
        metadata.add_text("Copyright", config.CHART_COPYRIGHT)
        img.save(self.output_path, pnginfo=metadata)

    def _save_svg(self, fig: plt.Figure) -> Path:
        """Save figure as SVG with metadata and optimization."""
        config.CHARTS_SVG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        fig.savefig(
            self.svg_output_path,
            format="svg",
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none"
        )

        self._add_svg_metadata()

        if config.SVG_OPTIMIZE:
            self._optimize_svg()

        return self.svg_output_path

    def _add_svg_metadata(self) -> None:
        """Embed Dublin Core metadata in SVG file."""
        namespaces = {
            "": "http://www.w3.org/2000/svg",
            "xlink": "http://www.w3.org/1999/xlink",
            "dc": "http://purl.org/dc/elements/1.1/",
            "cc": "http://creativecommons.org/ns#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        }
        for prefix, uri in namespaces.items():
            if prefix:
                ET.register_namespace(prefix, uri)
            else:
                ET.register_namespace("", uri)

        tree = ET.parse(self.svg_output_path)
        root = tree.getroot()

        metadata = ET.SubElement(root, "metadata")
        rdf = ET.SubElement(metadata, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF")
        work = ET.SubElement(rdf, "{http://creativecommons.org/ns#}Work")

        dc_title = ET.SubElement(work, "{http://purl.org/dc/elements/1.1/}title")
        dc_title.text = self.title

        dc_creator = ET.SubElement(work, "{http://purl.org/dc/elements/1.1/}creator")
        dc_creator.text = config.CHART_AUTHOR

        dc_rights = ET.SubElement(work, "{http://purl.org/dc/elements/1.1/}rights")
        dc_rights.text = config.CHART_COPYRIGHT

        dc_source = ET.SubElement(work, "{http://purl.org/dc/elements/1.1/}source")
        dc_source.text = config.CHART_SOFTWARE

        title_elem = ET.Element("title")
        title_elem.text = self.title
        root.insert(0, title_elem)

        desc_elem = ET.Element("desc")
        desc_elem.text = f"Chart by {config.CHART_AUTHOR}"
        root.insert(1, desc_elem)

        tree.write(self.svg_output_path, encoding="utf-8", xml_declaration=True)

    def _optimize_svg(self) -> None:
        """Optimize SVG using scour."""
        with open(self.svg_output_path, "rb") as f:
            svg_content = f.read()

        options = scour.sanitizeOptions(options=None)
        options.remove_descriptive_elements = config.SVG_OPTIMIZATION_OPTIONS.get(
            "remove_descriptive_elements", False
        )
        options.strip_xml_prolog = config.SVG_OPTIMIZATION_OPTIONS.get(
            "strip_xml_prolog", False
        )
        options.enable_viewboxing = config.SVG_OPTIMIZATION_OPTIONS.get(
            "enable_viewboxing", True
        )
        options.shorten_ids = config.SVG_OPTIMIZATION_OPTIONS.get(
            "shorten_ids", True
        )

        optimized = scour.scourString(svg_content.decode("utf-8"), options=options)

        with open(self.svg_output_path, "w", encoding="utf-8") as f:
            f.write(optimized)

    def _apply_common_style(self, ax: plt.Axes) -> None:
        ax.set_title(self.title, fontsize=14, fontweight="bold", pad=15)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(labelsize=10)
