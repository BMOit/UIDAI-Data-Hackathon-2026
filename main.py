"""
UIDAI Data Hackathon 2026
Problem Statement: Understanding repeated aadhar engagement patterns and their impact on users
By Rajneesh (github.com/BMOit / rajneesh.blog)
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import config
from src.charts import discover_charts, generate_all_charts, get_all_chart_classes
from src.data_loader import DataLoader


def list_charts() -> None:
    discover_charts()
    charts = get_all_chart_classes()

    print("\nAvailable Charts:")
    print("-" * 60)

    for _, cls in sorted(charts.items()):
        chart = cls()
        print(f"  {chart.chart_id}: {chart.title}")

    print("-" * 60)
    print(f"Total: {len(charts)} charts\n")


def main():
    parser = argparse.ArgumentParser(description="Generate UIDAI Hackathon charts")
    parser.add_argument("--chart", "-c", type=str, nargs="+", help="Chart ID(s) to generate")
    parser.add_argument("--list", "-l", action="store_true", help="List available charts")
    parser.add_argument("--output", "-o", type=Path, default=config.CHARTS_OUTPUT_DIR)
    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["png", "svg", "both"],
        default="png",
        help="Output format: png, svg, or both (default: png)"
    )
    parser.add_argument(
        "--svg-output",
        type=Path,
        default=None,
        help="Output directory for SVG files (default: charts-svg/)"
    )

    args = parser.parse_args()

    if args.list:
        list_charts()
        return

    if args.output != config.CHARTS_OUTPUT_DIR:
        config.CHARTS_OUTPUT_DIR = args.output

    if args.svg_output:
        config.CHARTS_SVG_OUTPUT_DIR = args.svg_output

    config.CHARTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.format in ("svg", "both"):
        config.CHARTS_SVG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\nUIDAI Data Hackathon 2026 - Chart Generator")
    print(f"Output format: {args.format}")
    print(f"PNG output directory: {config.CHARTS_OUTPUT_DIR}")
    if args.format in ("svg", "both"):
        print(f"SVG output directory: {config.CHARTS_SVG_OUTPUT_DIR}")
    print("-" * 50)

    print("\nLoading datasets...")
    loader = DataLoader()
    _ = loader.demographic
    _ = loader.biometric
    _ = loader.enrollment
    print("  -> Datasets loaded and cached")

    print("\nGenerating charts...")
    output_paths = generate_all_charts(args.chart, formats=args.format)

    print("-" * 50)
    print(f"\nGenerated {len(output_paths)} file(s)")
    if args.format == "png":
        print(f"Output location: {config.CHARTS_OUTPUT_DIR}\n")
    elif args.format == "svg":
        print(f"Output location: {config.CHARTS_SVG_OUTPUT_DIR}\n")
    else:
        print(f"PNG location: {config.CHARTS_OUTPUT_DIR}")
        print(f"SVG location: {config.CHARTS_SVG_OUTPUT_DIR}\n")


if __name__ == "__main__":
    main()
