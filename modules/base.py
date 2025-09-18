"""Basismodul, das alle Untermodule erweitern sollen."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from src.dashboardtool.config import DashboardConfig, DEFAULT_CONFIG


@dataclass(frozen=True)
class ModuleAction:
    """Beschreibt eine Interaktionsmöglichkeit im Modul."""

    name: str
    label: str
    description: str
    shortcut: str | None = None

    def to_dict(self) -> Dict[str, str]:
        data = {
            "name": self.name,
            "label": self.label,
            "description": self.description,
        }
        if self.shortcut:
            data["shortcut"] = self.shortcut
        return data


@dataclass(frozen=True)
class ModuleValidationResult:
    """Hält Prüfhinweise für Modul-Daten fest."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "checked_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        }


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

    # ------------------------------------------------------------------
    # Komfortfunktionen für die GUI-Schicht
    # ------------------------------------------------------------------
    def _validate_payload(self, payload: Dict[str, Any]) -> ModuleValidationResult:
        """Prüft die von `render` gelieferten Daten."""

        errors: list[str] = []
        warnings: list[str] = []
        required = {"component", "title"}
        for key in required:
            if key not in payload:
                errors.append(f"Pflichtfeld '{key}' fehlt. Bitte in render() ergänzen.")

        theme = payload.get("theme")
        if theme is None:
            warnings.append(
                "Theme fehlt. Es wird automatisch ein Standardfarbschema ergänzt."
            )
        elif isinstance(theme, dict):
            missing_theme_keys = {"background", "surface", "text_primary"} - set(theme)
            if missing_theme_keys:
                warnings.append(
                    "Theme ist unvollständig. Fehlende Schlüssel: "
                    + ", ".join(sorted(missing_theme_keys))
                )
        else:
            errors.append("Theme muss ein Wörterbuch mit Farbwerten sein.")

        shortcuts = payload.get("keyboard_shortcuts")
        if shortcuts is None:
            warnings.append(
                "Tastenkürzel fehlen. Es werden Standardwerte aus der Konfiguration ergänzt."
            )

        return ModuleValidationResult(errors=errors, warnings=warnings)

    def available_actions(self) -> list[ModuleAction]:
        """Erzeugt eine Liste unterstützter Standardaktionen."""

        shortcuts = self.context.config.standards.keyboard_shortcuts
        actions: list[ModuleAction] = [
            ModuleAction(
                name="focus",
                label="Fokus",
                description="Bringt das Modul per Tastatur in den Vordergrund.",
                shortcut=shortcuts.get("focus"),
            ),
            ModuleAction(
                name="toggle_visibility",
                label="Ein-/Ausblenden",
                description="Zeigt oder versteckt das Modul.",
                shortcut=shortcuts.get("toggle_visibility"),
            ),
        ]

        if self.layout_spec.allow_maximize:
            actions.append(
                ModuleAction(
                    name="maximize",
                    label="Maximieren",
                    description="Schaltet zwischen Standard- und Vollbildansicht um.",
                    shortcut=shortcuts.get("maximize"),
                )
            )
        if self.layout_spec.allow_detach:
            actions.append(
                ModuleAction(
                    name="detach",
                    label="Fenster lösen",
                    description="Öffnet das Modul in einem separaten Fenster.",
                    shortcut=shortcuts.get("detach"),
                )
            )
        return actions

    def layout_defaults(self) -> Dict[str, Any]:
        """Stellt Layout-Informationen für Frontends bereit."""

        return {
            "min_width": self.layout_spec.min_width,
            "min_height": self.layout_spec.min_height,
            "padding": self.layout_spec.padding,
            "allow_detach": self.layout_spec.allow_detach,
            "allow_maximize": self.layout_spec.allow_maximize,
        }

    def render_dashboard_tile(self) -> Dict[str, Any]:
        """Reichert das Render-Ergebnis mit Metadaten an."""

        payload = dict(self.render())
        validation = self._validate_payload(payload)
        theme = payload.get("theme")
        if not isinstance(theme, dict):
            theme = self.context.config.get_theme("aurora")
        shortcuts = (
            payload.get("keyboard_shortcuts")
            or self.context.config.standards.keyboard_shortcuts
        )
        payload.setdefault("keyboard_shortcuts", shortcuts)
        payload.setdefault("theme", theme)

        return {
            "identifier": self.identifier,
            "display_name": self.display_name,
            "description": self.description,
            "component": payload.get("component", self.identifier),
            "payload": payload,
            "actions": [action.to_dict() for action in self.available_actions()],
            "layout": self.layout_defaults(),
            "shortcuts": shortcuts,
            "validation": validation.to_dict(),
            "storage_directory": str(self.storage_directory),
        }

    def autosave(self) -> None:
        """Standard-Autosave, kann überschrieben werden."""

        # Hier würde die konkrete Speicherlogik eingebunden werden.
        pass
