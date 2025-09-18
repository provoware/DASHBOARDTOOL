"""DashboardTool core package.

Dieses Paket bündelt zentrale Konfigurationen und Hilfsfunktionen für das Dashboard.
"""

from .config import DashboardConfig, DEFAULT_CONFIG
from .themes import THEME_PRESETS
from .layout import LayoutSpec, DEFAULT_LAYOUT

__all__ = [
    "DashboardConfig",
    "DEFAULT_CONFIG",
    "THEME_PRESETS",
    "LayoutSpec",
    "DEFAULT_LAYOUT",
]
