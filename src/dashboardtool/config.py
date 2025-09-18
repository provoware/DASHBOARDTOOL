"""Globale Dashboard-Konfigurationen.

Hier werden Standards für Module, Farben und Verhalten festgelegt, damit alle Module
auf denselben Vorgaben ("Standards": allgemeine Richtlinien) basieren.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

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
class DashboardConfig:
    """Zentrale Konfigurationsdaten für das Dashboard."""

    standards: ModuleStandard = ModuleStandard()
    themes: Dict[str, Dict[str, str]] = field(default_factory=lambda: THEME_PRESETS)
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


DEFAULT_CONFIG = DashboardConfig()
"""Global abrufbare Konfiguration mit Standards und Farbthemen."""
