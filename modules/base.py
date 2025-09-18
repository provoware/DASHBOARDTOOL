"""Basismodul, das alle Untermodule erweitern sollen."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from src.dashboardtool import DashboardConfig, DEFAULT_CONFIG


@dataclass
class ModuleContext:
    """Kontextinformationen für Module (z.B. Logging- oder Speicherpfade)."""

    config: DashboardConfig = DEFAULT_CONFIG
    storage_path: Path = Path("var/data")
    logger_name: str = "dashboardtool"
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.storage_path, Path):
            self.storage_path = Path(self.storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.config.ensure_directories()

    def ensure_storage_dir(self, module_identifier: str) -> Path:
        """Stellt das Speicherverzeichnis für ein Modul bereit."""

        safe_identifier = module_identifier or "module"
        target = self.storage_path / safe_identifier
        target.mkdir(parents=True, exist_ok=True)
        return target

    def ensure_log_file(self, filename: str = "dashboard.log") -> Path:
        """Liefert einen Log-Pfad ("Log": Protokolldatei) und legt Verzeichnisse an."""

        directory = self.config.log_directory
        directory.mkdir(parents=True, exist_ok=True)
        return directory / filename


class DashboardModule:
    """Basisklasse mit standardisierten Hooks und Layoutvorgaben."""

    identifier: str = "base"
    display_name: str = "Basis Modul"
    description: str = "Grundfunktionen"

    def __init__(self, context: Optional[ModuleContext] = None) -> None:
        self.context = context or ModuleContext()
        self.layout_spec = self.context.config.standards
        self.storage_directory = self.context.ensure_storage_dir(self.identifier)

    def render(self) -> Dict[str, Any]:
        """Erzeugt strukturierte Daten für die GUI-Schicht."""

        raise NotImplementedError("Module müssen die render-Methode überschreiben.")

    def autosave(self) -> None:
        """Standard-Autosave, kann überschrieben werden."""

        # Hier würde die konkrete Speicherlogik eingebunden werden.
        pass
