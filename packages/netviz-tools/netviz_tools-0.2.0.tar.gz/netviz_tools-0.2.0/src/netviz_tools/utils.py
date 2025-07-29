"""
Utilities for the netviz_tools package.

This module provides constants and configurations used throughout the netviz_tools package.

Constants include:
- CONTINENT_COLORS: A dictionary mapping continents to their respective colors for visualizations.
- PACKAGE_DIR: The directory where the package is located.
- DATA_DIR: The directory where data files are stored.
- LOG_DIR: The directory where log files are stored.
- LOG_FILE: The path to the log file for the package.
"""

import json
from pathlib import Path
from typing import Any

# Color mapping for continents in visualizations
CONTINENT_COLORS: dict[str, str] = {
    "Africa": "red",
    "Asia": "green",
    "Europe": "blue",
    "Northern America": "purple",
    "Oceania": "orange",
    "South America": "pink",
    "Central America": "cyan",
    "Caribbean": "brown",
}

# Constants
PACKAGE_DIR: Path = Path(__file__).parent
DATA_DIR: Path = PACKAGE_DIR / "data"
LOG_DIR: Path = PACKAGE_DIR / "logs"
LOG_FILE: Path = LOG_DIR / "netviz_tools.log"


def save_json(data: Any, file_path: Path) -> None:
    """
    Save data to a JSON file.

    Args:
        data: Data to save (typically a plotly figure's JSON representation)
        file_path: Path where to save the JSON file
    """
    # Convert plotly figure to JSON if needed
    if hasattr(data, "to_json"):
        json_data = data.to_json()
    else:
        json_data = json.dumps(data, indent=2)

    # Ensure parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write JSON data to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_data)


# Verify directories exist and log file is created
def directory_setup():
    """Ensure necessary directories exist and log file is created."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.touch()
