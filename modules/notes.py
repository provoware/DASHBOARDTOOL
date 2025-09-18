"""Notizmodul mit Autospeicher-Logik ("Autospeichern": automatisches Speichern)."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from modules.base import DashboardModule


class NotesModule(DashboardModule):
    identifier = "notes"
    display_name = "Notizbereich"
    description = "Speichert Notizen persistent mit Autosave."

    def __init__(
        self, storage_backend: Dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self._storage = storage_backend if storage_backend is not None else {}
        self._last_saved: datetime | None = None

    def render(self) -> Dict[str, Any]:
        theme = self.context.config.get_theme("aurora")
        return {
            "component": "notes",
            "title": self.display_name,
            "theme": theme,
            "autosave_interval": self.context.config.autosave_interval_minutes,
            "autosave_triggers": self.context.config.autosave_triggers,
            "breakpoints": self.context.config.responsive_profile.as_dicts(),
            "keyboard_shortcuts": self.context.config.standards.keyboard_shortcuts,
            "storage_directory": str(self.storage_directory),
        }

    def write(self, note_id: str, content: str) -> None:
        if not note_id:
            raise ValueError(
                'Die Notiz benötigt eine Kennung ("Kennung": eindeutige ID).'
            )
        timestamp = datetime.utcnow().isoformat()
        self._storage[note_id] = {"content": content, "timestamp": timestamp}
        self._last_saved = datetime.utcnow()

    def autosave(self) -> None:
        if self._last_saved is None:
            self._last_saved = datetime.utcnow()

    @property
    def storage(self) -> Dict[str, Any]:
        return self._storage

    def read(self, note_id: str) -> Dict[str, Any] | None:
        """Liest eine gespeicherte Notiz aus (oder gibt None zurück)."""

        return self._storage.get(note_id)

    def list_note_ids(self) -> list[str]:
        """Gibt verfügbare Notiz-IDs sortiert zurück."""

        return sorted(self._storage)
