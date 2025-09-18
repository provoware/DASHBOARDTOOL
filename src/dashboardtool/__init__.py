"""DashboardTool core package.

Dieses Paket bündelt zentrale Konfigurationen und Hilfsfunktionen für das Dashboard.
"""

from .config import (
    DashboardConfig,
    DEFAULT_CONFIG,
    ResponsiveBreakpoint,
    ResponsiveLayoutProfile,
)
from .themes import THEME_PRESETS, contrast_ratio, validate_theme_accessibility
from .layout import LayoutSpec, DEFAULT_LAYOUT

__all__ = [
    "DashboardConfig",
    "DEFAULT_CONFIG",
    "ResponsiveBreakpoint",
    "ResponsiveLayoutProfile",
    "THEME_PRESETS",
    "contrast_ratio",
    "validate_theme_accessibility",
    "LayoutSpec",
    "DEFAULT_LAYOUT",
]
