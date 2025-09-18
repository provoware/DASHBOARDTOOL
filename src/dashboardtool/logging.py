"""Hilfsfunktionen für strukturierte Logdaten ("Log": Protokoll)."""

from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, Dict, Iterable, List

LOG_LEVELS: tuple[str, ...] = ("debug", "info", "warning", "error", "critical")


@dataclass(frozen=True)
class LogEntry:
    """Ein einzelner Logeintrag mit Zeitstempel."""

    timestamp: datetime
    level: str
    message: str
    source: str

    def to_dict(self) -> Dict[str, str]:
        """Konvertiert den Eintrag in eine speicherbare Darstellung."""

        return {
            "timestamp": self.timestamp.replace(microsecond=0).isoformat(),
            "level": self.level,
            "message": self.message,
            "source": self.source,
        }


class LogBuffer:
    """Begrenzt wachsendes Protokoll mit Komfortfunktionen."""

    def __init__(self, max_entries: int = 100) -> None:
        if max_entries <= 0:
            raise ValueError("max_entries muss größer als 0 sein.")
        self._entries: Deque[LogEntry] = deque(maxlen=max_entries)

    def add(
        self,
        message: str,
        level: str = "info",
        source: str = "dashboard",
        timestamp: datetime | None = None,
    ) -> LogEntry:
        level_normalized = level.lower()
        if level_normalized not in LOG_LEVELS:
            raise ValueError(
                "Unbekannte Log-Stufe. Erlaubt sind: " + ", ".join(LOG_LEVELS)
            )
        entry = LogEntry(
            timestamp=timestamp or datetime.utcnow(),
            level=level_normalized,
            message=message,
            source=source,
        )
        self._entries.append(entry)
        return entry

    def entries(self) -> List[LogEntry]:
        """Gibt aktuelle Einträge als Liste zurück."""

        return list(self._entries)

    def as_dicts(self) -> List[Dict[str, str]]:
        """Gibt Einträge als JSON-kompatible Objekte zurück."""

        return [entry.to_dict() for entry in self._entries]

    def filter_by_level(self, minimum_level: str) -> List[LogEntry]:
        """Filtert Einträge nach Mindeststufe."""

        minimum = minimum_level.lower()
        if minimum not in LOG_LEVELS:
            raise ValueError(
                "Unbekannte Log-Stufe. Erlaubt sind: " + ", ".join(LOG_LEVELS)
            )
        allowed: Iterable[str] = LOG_LEVELS[LOG_LEVELS.index(minimum) :]
        return [entry for entry in self._entries if entry.level in allowed]

    def clear(self) -> None:
        """Leert den Zwischenspeicher."""

        self._entries.clear()

    def export_json_lines(self) -> str:
        """Gibt alle Einträge als JSON-Zeilen zurück."""

        return "\n".join(
            json.dumps(entry.to_dict(), ensure_ascii=False) for entry in self._entries
        )


__all__ = ["LOG_LEVELS", "LogEntry", "LogBuffer"]
