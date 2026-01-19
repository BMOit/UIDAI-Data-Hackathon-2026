"""Global configuration for the UIDAI Hackathon chart generation system."""
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent
DATASETS_DIR = PROJECT_ROOT / "Datasets"
CHARTS_OUTPUT_DIR = PROJECT_ROOT / "charts"

# Dataset directories
DEMOGRAPHIC_DIR = DATASETS_DIR / "demographic"
BIOMETRIC_DIR = DATASETS_DIR / "biometric"
ENROLLMENT_DIR = DATASETS_DIR / "enrollment"

# Chart styling
COLORS = {
    "demographic": "#1f77b4",  # Blue
    "biometric": "#ff7f0e",    # Orange
    "enrollment": "#2ca02c",   # Green
    "primary": "#9467bd",      # Purple (for general charts)
}

FIGURE_DPI = 150
DEFAULT_FIGSIZE = (12, 8)

# Date format in CSVs (DD-MM-YYYY)
DATE_FORMAT = "%d-%m-%Y"
