"""Layoutdefinitionen für das Hauptfenster und Module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .config import ResponsiveLayoutProfile


@dataclass(frozen=True)
class LayoutSpec:
    """Definiert Raster und Bereichsaufteilungen des Dashboards."""

    columns: int = 12
    gutter: int = 16
    sidebar_width_ratio: float = 0.22
    header_height: int = 72
    footer_height: int = 48

    def sidebar_bounds(self, total_width: int) -> Tuple[int, int]:
        """Gibt Pixelbreite der Sidebar als (min, max) zurück."""

        width = int(total_width * self.sidebar_width_ratio)
        return max(240, width), max(360, width + 120)

    def to_css_variables(self) -> Dict[str, str]:
        """Bereitet Variablen für Frontend-Frameworks vor."""

        return {
            "--grid-columns": str(self.columns),
            "--grid-gutter": f"{self.gutter}px",
            "--sidebar-width": f"{int(self.sidebar_width_ratio * 100)}vw",
            "--header-height": f"{self.header_height}px",
            "--footer-height": f"{self.footer_height}px",
        }

    def to_css_with_breakpoints(
        self, profile: ResponsiveLayoutProfile
    ) -> Dict[str, str]:
        """Erweitert CSS-Variablen um responsive Breakpoints."""

        variables = self.to_css_variables()
        for breakpoint in profile.breakpoints:
            prefix = f"--bp-{breakpoint.name}"
            variables[f"{prefix}-min-width"] = f"{breakpoint.min_width}px"
            variables[f"{prefix}-columns"] = str(breakpoint.columns)
            variables[f"{prefix}-max-module-width"] = f"{breakpoint.max_module_width}px"
        return variables


DEFAULT_LAYOUT = LayoutSpec()
"""Standardlayout, das Module automatisch übernehmen sollen."""
