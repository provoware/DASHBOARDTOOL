"""Debugging-Modul mit Echtzeit-Logging ("Logging": Protokollierung)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Sequence

from modules.base import DashboardModule
from src.dashboardtool.logging import LOG_LEVELS, LogBuffer


class DebugModule(DashboardModule):
    identifier = "debug"
    display_name = "Diagnose"
    description = "Zeigt Logeinträge, speichert sie und schlägt Lösungen vor."

    def __init__(
        self,
        *,
        buffer: LogBuffer | None = None,
        max_entries: int = 250,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.buffer = (
            buffer if buffer is not None else LogBuffer(max_entries=max_entries)
        )
        self.theme = self.context.config.get_theme("monochrome")
        self.log_file: Path = self.context.ensure_log_file("debug.log")
        self._loaded_entries = self._load_existing_entries()

    def _load_existing_entries(self) -> int:
        """Liest bereits vorhandene Logdaten für Selbstheilung ein."""

        if not self.log_file.exists():
            return 0
        loaded = 0
        for line in self.log_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            message = str(payload.get("message", "Unbekannte Meldung"))
            level = str(payload.get("level", "info"))
            source = str(payload.get("source", "dashboard"))
            timestamp_str = payload.get("timestamp")
            timestamp = None
            if isinstance(timestamp_str, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except ValueError:
                    timestamp = None
            self.buffer.add(
                message=message, level=level, source=source, timestamp=timestamp
            )
            loaded += 1
        return loaded

    def log_event(
        self,
        message: str,
        *,
        level: str = "info",
        source: str = "dashboard",
    ) -> Dict[str, str]:
        """Fügt einen Logeintrag hinzu und schreibt ihn auf die Festplatte."""

        entry = self.buffer.add(message=message, level=level, source=source)
        self._append_to_file(entry.to_dict())
        return entry.to_dict()

    def _append_to_file(self, payload: Dict[str, str]) -> None:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with self.log_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def get_recent(self, limit: int | None = None) -> List[Dict[str, str]]:
        """Liefert die jüngsten Einträge, optional begrenzt."""

        entries = self.buffer.as_dicts()
        if limit is None or limit >= len(entries):
            return entries
        return entries[-limit:]

    def clear_events(self) -> None:
        """Leert das Protokoll und entfernt die Datei."""

        self.buffer.clear()
        if self.log_file.exists():
            self.log_file.unlink()

    def render(self) -> Dict[str, Any]:
        """Bereitet Daten für die GUI auf."""

        return {
            "component": "debug",
            "title": self.display_name,
            "theme": self.theme,
            "entries": self.get_recent(),
            "log_levels": list(LOG_LEVELS),
            "storage_directory": str(self.storage_directory),
            "log_file": str(self.log_file),
            "loaded_entries": self._loaded_entries,
            "keyboard_shortcuts": self.context.config.standards.keyboard_shortcuts,
            "breakpoints": self.context.config.responsive_profile.as_dicts(),
        }

    def export_snapshot(self, destination: Path) -> Path:
        """Schreibt die aktuelle Logliste als JSON-Zeilen-Datei."""

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            "\n".join(
                json.dumps(entry, ensure_ascii=False) for entry in self.get_recent()
            ),
            encoding="utf-8",
        )
        return destination

    @staticmethod
    def supported_levels() -> Sequence[str]:
        """Erlaubte Log-Stufen für die GUI."""

        return LOG_LEVELS


__all__ = ["DebugModule"]
