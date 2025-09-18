"""Globale Dashboard-Konfigurationen.

Hier werden Standards für Module, Farben und Verhalten festgelegt, damit alle Module
auf denselben Vorgaben ("Standards": allgemeine Richtlinien) basieren.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

from .themes import THEME_PRESETS


@dataclass(frozen=True)
class ModuleStandard:
    """Definiert Größen- und Layoutvorgaben für Module."""

    min_width: int = 320
    min_height: int = 240
    padding: int = 16
    allow_detach: bool = True
    allow_maximize: bool = True
    keyboard_shortcuts: Dict[str, str] = field(
        default_factory=lambda: {
            "focus": "CTRL+ALT+F",
            "toggle_visibility": "CTRL+ALT+V",
            "detach": "CTRL+ALT+D",
        }
    )


@dataclass(frozen=True)
class ResponsiveBreakpoint:
    """Beschreibt einen Layout-Breakpoint ("Breakpoint": Umschaltpunkt)."""

    name: str
    min_width: int
    columns: int
    max_module_width: int

    def to_dict(self) -> Dict[str, int | str]:
        return {
            "name": self.name,
            "min_width": self.min_width,
            "columns": self.columns,
            "max_module_width": self.max_module_width,
        }


@dataclass(frozen=True)
class ResponsiveLayoutProfile:
    """Hält mehrere Breakpoints für responsive Ansichten."""

    breakpoints: Tuple[ResponsiveBreakpoint, ...] = (
        ResponsiveBreakpoint("mobile", 0, 4, 360),
        ResponsiveBreakpoint("tablet", 768, 8, 480),
        ResponsiveBreakpoint("desktop", 1280, 12, 640),
        ResponsiveBreakpoint("wide", 1600, 12, 820),
    )

    def for_width(self, width: int) -> ResponsiveBreakpoint:
        """Liefert den passenden Breakpoint für eine Breite."""

        active = self.breakpoints[0]
        for breakpoint in sorted(self.breakpoints, key=lambda bp: bp.min_width):
            if width >= breakpoint.min_width:
                active = breakpoint
        return active

    def as_dicts(self) -> List[Dict[str, int | str]]:
        """Praktische Darstellung für GUI- oder Dokumentationszwecke."""

        return [bp.to_dict() for bp in self.breakpoints]


@dataclass(frozen=True)
class DashboardConfig:
    """Zentrale Konfigurationsdaten für das Dashboard."""

    standards: ModuleStandard = ModuleStandard()
    themes: Dict[str, Dict[str, str]] = field(default_factory=lambda: THEME_PRESETS)
    responsive_profile: ResponsiveLayoutProfile = ResponsiveLayoutProfile()
    autosave_interval_minutes: int = 10
    autosave_triggers: List[str] = field(
        default_factory=lambda: ["field_change", "timer", "on_exit"]
    )
    log_directory: Path = Path("var/log/dashboardtool")
    default_timezone: str = "Europe/Berlin"

    def get_theme(self, name: str) -> Dict[str, str]:
        """Liefert ein Farbthema oder wirft einen beschreibenden Fehler."""

        if name not in self.themes:
            available = ", ".join(sorted(self.themes))
            raise KeyError(
                f"Theme '{name}' nicht gefunden. Verfügbare Themes: {available}."
            )
        return self.themes[name]

    def breakpoint_for_width(self, width: int) -> Dict[str, int | str]:
        """Gibt passende responsive Layout-Daten für eine Breite zurück."""

        breakpoint = self.responsive_profile.for_width(width)
        return breakpoint.to_dict()

    def ensure_directories(self) -> None:
        """Legt notwendige Verzeichnisse an, falls sie fehlen."""

        self.log_directory.mkdir(parents=True, exist_ok=True)


DEFAULT_CONFIG = DashboardConfig()
"""Global abrufbare Konfiguration mit Standards und Farbthemen."""
