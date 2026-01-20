"""Chart registry and auto-discovery."""
from pathlib import Path
from typing import Dict, List, Optional, Type, Union
import importlib
import pkgutil

from .base import BaseChart

_CHART_REGISTRY: Dict[str, Type[BaseChart]] = {}


def register_chart(cls: Type[BaseChart]) -> Type[BaseChart]:
    _CHART_REGISTRY[cls.__name__] = cls
    return cls


def get_all_chart_classes() -> Dict[str, Type[BaseChart]]:
    return _CHART_REGISTRY.copy()


def get_chart_by_id(chart_id: str) -> Optional[Type[BaseChart]]:
    for cls in _CHART_REGISTRY.values():
        instance = cls()
        if instance.chart_id == chart_id:
            return cls
    return None


def discover_charts() -> None:
    charts_dir = Path(__file__).parent

    for subdir in charts_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("_"):
            for module_info in pkgutil.iter_modules([str(subdir)]):
                if module_info.name.startswith("chart_"):
                    importlib.import_module(
                        f".{subdir.name}.{module_info.name}",
                        package="src.charts"
                    )


def generate_all_charts(
    chart_ids: Optional[List[str]] = None,
    formats: Union[str, List[str]] = "png"
) -> List[Path]:
    """Generate charts in specified format(s).

    Args:
        chart_ids: Optional list of chart IDs to generate
        formats: 'png', 'svg', 'both', or list like ['png', 'svg']

    Returns:
        List of paths to generated files
    """
    discover_charts()
    output_paths = []

    for name, cls in sorted(_CHART_REGISTRY.items()):
        chart = cls()
        if chart_ids and chart.chart_id not in chart_ids:
            continue

        print(f"Generating {chart.chart_id}: {chart.title}...")
        paths = chart.save(formats=formats)

        if isinstance(paths, Path):
            paths = [paths]

        output_paths.extend(paths)
        for path in paths:
            print(f"  -> Saved to {path}")

    return output_paths
