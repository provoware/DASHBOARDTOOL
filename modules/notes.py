"""Notizmodul mit Autospeicher-Logik ("Autospeichern": automatisches Speichern)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from modules.base import DashboardModule


class NotesModule(DashboardModule):
    identifier = "notes"
    display_name = "Notizbereich"
    description = "Speichert Notizen persistent mit Autosave."

    def __init__(
        self,
        storage_backend: Dict[str, Any] | None = None,
        storage_file: str | Path | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.storage_file = (
            Path(storage_file)
            if storage_file is not None
            else self.storage_directory / "notes.json"
        )
        self._storage = storage_backend if storage_backend is not None else {}
        self._last_saved: datetime | None = None
        self._autosave_log: List[str] = []
        self._load_from_disk()

    def render(self) -> Dict[str, Any]:
        theme = self.context.config.get_theme("aurora")
        last_saved = (
            self._last_saved.replace(microsecond=0).isoformat() + "Z"
            if self._last_saved
            else None
        )
        return {
            "component": "notes",
            "title": self.display_name,
            "theme": theme,
            "autosave_interval": self.context.config.autosave_interval_minutes,
            "autosave_triggers": self.context.config.autosave_triggers,
            "breakpoints": self.context.config.responsive_profile.as_dicts(),
            "keyboard_shortcuts": self.context.config.standards.keyboard_shortcuts,
            "status": {
                "last_saved": last_saved,
                "entries": len(self._storage),
                "autosave_log": list(self._autosave_log[-5:]),
            },
            "toolbar": [
                {
                    "action": "autosave_now",
                    "label": "Jetzt speichern",
                    "description": "Speichert die aktuelle Notiz sofort.",
                    "shortcut": "CTRL+ALT+S",
                },
                {
                    "action": "create_note",
                    "label": "Neue Notiz",
                    "description": "Legt eine leere Notiz mit Zeitstempel an.",
                    "shortcut": "CTRL+ALT+N",
                },
            ],
            "notes_index": self.list_note_ids(),
        }

    def write(self, note_id: str, content: str) -> None:
        if not note_id:
            raise ValueError(
                'Die Notiz benötigt eine Kennung ("Kennung": eindeutige ID).'
            )
        timestamp = datetime.utcnow().isoformat()
        self._storage[note_id] = {"content": content, "timestamp": timestamp}
        self._last_saved = datetime.utcnow()
        self._autosave_log.append(
            f"{self._last_saved.replace(microsecond=0).isoformat()}Z: '{note_id}' gespeichert"
        )
        self._flush_to_disk()

    def autosave(self) -> None:
        self._last_saved = datetime.utcnow()
        self._autosave_log.append(
            f"{self._last_saved.replace(microsecond=0).isoformat()}Z: Autosave ausgeführt"
        )
        self._flush_to_disk()

    @property
    def storage(self) -> Dict[str, Any]:
        return self._storage

    def read(self, note_id: str) -> Dict[str, Any] | None:
        """Liest eine gespeicherte Notiz aus (oder gibt None zurück)."""

        return self._storage.get(note_id)

    def list_note_ids(self) -> list[str]:
        """Gibt verfügbare Notiz-IDs sortiert zurück."""

        return sorted(self._storage)

    # ------------------------------------------------------------------
    # Persistenzschicht
    # ------------------------------------------------------------------
    def _load_from_disk(self) -> None:
        """Lädt vorhandene Notizen aus der JSON-Datei."""

        try:
            if self.storage_file.exists():
                raw = json.loads(self.storage_file.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    self._storage.update(raw)
                    timestamps = [
                        datetime.fromisoformat(entry["timestamp"])
                        for entry in self._storage.values()
                        if isinstance(entry, dict) and "timestamp" in entry
                    ]
                    if timestamps:
                        self._last_saved = max(timestamps)
        except Exception as exc:  # pragma: no cover - Schutz vor Dateifehlern
            self._autosave_log.append(f"Fehler beim Laden: {exc}")

    def _flush_to_disk(self) -> None:
        """Speichert Notizen dauerhaft im JSON-Format."""

        try:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            serializable = {
                note_id: {
                    "content": entry.get("content", ""),
                    "timestamp": entry.get("timestamp", datetime.utcnow().isoformat()),
                }
                for note_id, entry in self._storage.items()
                if isinstance(entry, dict)
            }
            self.storage_file.write_text(
                json.dumps(serializable, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:  # pragma: no cover - Schreibschutz
            self._autosave_log.append(f"Fehler beim Speichern: {exc}")
