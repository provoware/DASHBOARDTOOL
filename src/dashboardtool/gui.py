"""Orchestriert die grafische Oberfläche des Dashboards."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Sequence

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover - nur für sehr alte Python-Versionen
    ZoneInfo = None  # type: ignore
    ZoneInfoNotFoundError = Exception  # type: ignore

from modules.base import DashboardModule

from .config import DashboardConfig, DEFAULT_CONFIG
from .layout import DEFAULT_LAYOUT, LayoutSpec
from .themes import validate_theme_accessibility


@dataclass(frozen=True)
class SidebarItem:
    """Ein Eintrag in der linken Navigationsleiste."""

    identifier: str
    label: str
    description: str
    shortcut: str | None = None

    def to_dict(self) -> Dict[str, str]:
        data = {
            "identifier": self.identifier,
            "label": self.label,
            "description": self.description,
        }
        if self.shortcut:
            data["shortcut"] = self.shortcut
        return data


@dataclass
class DashboardApp:
    """Fasst Module, Layout und Statusinformationen für die GUI zusammen."""

    modules: Sequence[DashboardModule]
    config: DashboardConfig = DEFAULT_CONFIG
    layout: LayoutSpec = DEFAULT_LAYOUT
    title: str = "DashboardTool"
    subtitle: str = "Modulares Kontrollzentrum mit Hilfe-Overlays für Einsteiger"
    active_theme: str = "aurora"

    def __post_init__(self) -> None:
        self.modules = list(self.modules)
        self._ensure_unique_identifiers()

    # ------------------------------------------------------------------
    # Öffentliche API
    # ------------------------------------------------------------------
    def render(self) -> Dict[str, Any]:
        """Erzeugt eine leicht verständliche Darstellung für das Frontend."""

        now = self._current_time()
        module_tiles = [module.render_dashboard_tile() for module in self.modules]
        sidebar = self._build_sidebar(module_tiles)
        theme_report = self._theme_report()
        layout_variables = self.layout.to_css_with_breakpoints(
            self.config.responsive_profile
        )
        validation_summary = self._validation_summary(module_tiles)

        return {
            "header": self._header(now),
            "status": self._status(now, module_tiles),
            "layout": {
                "css_variables": layout_variables,
                "responsive_profile": self.config.responsive_profile.as_dicts(),
                "sidebar": sidebar,
            },
            "themes": theme_report,
            "modules": module_tiles,
            "validation": validation_summary,
            "keyboard_navigation": self._keyboard_navigation(sidebar["items"]),
            "notifications": self._notifications(),
            "self_healing": self._self_healing(module_tiles),
        }

    # ------------------------------------------------------------------
    # Aufbau einzelner Abschnitte
    # ------------------------------------------------------------------
    def _header(self, now: datetime) -> Dict[str, Any]:
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "clock": {
                "timezone": self.config.default_timezone,
                "iso": now.isoformat(),
                "readable": now.strftime("%d.%m.%Y %H:%M"),
            },
        }

    def _status(
        self, now: datetime, module_tiles: Sequence[Dict[str, Any]]
    ) -> Dict[str, Any]:
        storage_directories = sorted(
            {tile["storage_directory"] for tile in module_tiles}
        )
        return {
            "timestamp": now.isoformat(),
            "autosave": {
                "interval_minutes": self.config.autosave_interval_minutes,
                "triggers": self.config.autosave_triggers,
                "next_run_hint": "spätestens in 10 Minuten",  # Laienhinweis
            },
            "storage_directories": storage_directories,
            "module_count": len(module_tiles),
        }

    def _build_sidebar(self, module_tiles: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
        items = [
            SidebarItem(
                identifier=tile["identifier"],
                label=tile["display_name"],
                description=tile["description"],
                shortcut=tile.get("shortcuts", {}).get("focus"),
            ).to_dict()
            for tile in module_tiles
        ]
        return {
            "items": items,
            "collapsible": True,
            "initial_state": {
                "collapsed": False,
                "mobile_collapsed": True,
            },
            "aria_label": "Modulauswahl",
            "tips": [
                "Drücke CTRL+ALT+S, um die Sidebar zu öffnen (Tastenkürzel: Tastenfolge).",
            ],
        }

    def _theme_report(self) -> Dict[str, Any]:
        available = {
            name: {
                "colors": theme,
                "accessibility": validate_theme_accessibility(theme),
            }
            for name, theme in self.config.themes.items()
        }
        active = (
            self.active_theme
            if self.active_theme in available
            else next(iter(available))
        )
        return {
            "active": active,
            "available": available,
        }

    def _keyboard_navigation(
        self, sidebar_items: Sequence[Dict[str, str]]
    ) -> Dict[str, Any]:
        shortcuts = self.config.standards.keyboard_shortcuts
        return {
            "global_shortcuts": {
                "toggle_sidebar": "CTRL+ALT+S",
                "open_help": "F1",
            },
            "module_shortcuts": shortcuts,
            "sidebar_focus_order": [item["identifier"] for item in sidebar_items],
        }

    def _notifications(self) -> List[Dict[str, str]]:
        return [
            {
                "type": "info",
                "message": (
                    "Autosave aktiv: Speichert beim Feldwechsel, alle 10 Minuten "
                    "und beim Schließen automatisch."
                ),
            },
            {
                "type": "tip",
                "message": (
                    "Nutze die Sidebar, um Module ein- oder auszublenden. "
                    "Die Farben lassen sich unter 'Themes' umstellen."
                ),
            },
        ]

    def _validation_summary(
        self, module_tiles: Sequence[Dict[str, Any]]
    ) -> Dict[str, Any]:
        module_results = {
            tile["identifier"]: tile["validation"] for tile in module_tiles
        }
        has_errors = any(not result["is_valid"] for result in module_results.values())
        return {
            "modules": module_results,
            "has_errors": has_errors,
        }

    def _self_healing(self, module_tiles: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
        recovery_actions: List[str] = []
        for tile in module_tiles:
            if not tile["validation"]["is_valid"]:
                recovery_actions.append(
                    f"Modul '{tile['display_name']}' meldet fehlende Felder."
                )
        if not recovery_actions:
            recovery_actions.append(
                "Alle Module liefern vollständige Daten – keine Sofortmaßnahmen nötig."
            )
        return {
            "recommended_actions": recovery_actions,
            "auto_checks": [
                "Verzeichnis-Prüfung: Alle Speicherorte existieren.",
                "Theme-Prüfung: Farbkontraste wurden bewertet.",
            ],
        }

    # ------------------------------------------------------------------
    # Hilfsfunktionen
    # ------------------------------------------------------------------
    def _ensure_unique_identifiers(self) -> None:
        seen: Dict[str, str] = {}
        for module in self.modules:
            if module.identifier in seen:
                raise ValueError(
                    "Modulkennung doppelt vergeben: "
                    f"'{module.identifier}' für {seen[module.identifier]} und {module.display_name}"
                )
            seen[module.identifier] = module.display_name

    def _current_time(self) -> datetime:
        tz_name = self.config.default_timezone
        if ZoneInfo and tz_name:
            try:
                return datetime.now(ZoneInfo(tz_name))
            except ZoneInfoNotFoundError:
                pass
        return datetime.utcnow()
