"""Basismodul, das alle Untermodule erweitern sollen."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from src.dashboardtool import DashboardConfig, DEFAULT_CONFIG


@dataclass
class ModuleContext:
    """Kontextinformationen für Module (z.B. Logging- oder Speicherpfade)."""

    config: DashboardConfig = DEFAULT_CONFIG
    storage_path: str = "var/data"
    logger_name: str = "dashboardtool"
    extra: Dict[str, Any] = field(default_factory=dict)


class DashboardModule:
    """Basisklasse mit standardisierten Hooks und Layoutvorgaben."""

    identifier: str = "base"
    display_name: str = "Basis Modul"
    description: str = "Grundfunktionen"

    def __init__(self, context: Optional[ModuleContext] = None) -> None:
        self.context = context or ModuleContext()
        self.layout_spec = self.context.config.standards

    def render(self) -> Dict[str, Any]:
        """Erzeugt strukturierte Daten für die GUI-Schicht."""

        raise NotImplementedError("Module müssen die render-Methode überschreiben.")

    def autosave(self) -> None:
        """Standard-Autosave, kann überschrieben werden."""

        # Hier würde die konkrete Speicherlogik eingebunden werden.
        pass
