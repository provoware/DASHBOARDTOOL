import json
from datetime import datetime, timedelta

import pytest

from src.dashboardtool.logging import LOG_LEVELS, LogBuffer


def test_logbuffer_stores_entries_in_order():
    buffer = LogBuffer(max_entries=3)
    buffer.add("Erster Eintrag", level="info", source="system")
    buffer.add("Zweiter Eintrag", level="warning", source="module")
    entries = buffer.entries()
    assert entries[0].message == "Erster Eintrag"
    assert entries[1].level == "warning"


def test_logbuffer_respects_max_entries():
    buffer = LogBuffer(max_entries=2)
    buffer.add("Eins")
    buffer.add("Zwei")
    buffer.add("Drei")
    messages = [entry.message for entry in buffer.entries()]
    assert messages == ["Zwei", "Drei"]


def test_logbuffer_filter_by_level():
    buffer = LogBuffer()
    buffer.add("Debug", level="debug")
    buffer.add("Warnung", level="warning")
    warnings = buffer.filter_by_level("warning")
    assert [entry.message for entry in warnings] == ["Warnung"]


def test_logbuffer_rejects_invalid_level():
    buffer = LogBuffer()
    with pytest.raises(ValueError):
        buffer.add("Test", level="invalid")


def test_logbuffer_accepts_provided_timestamp():
    buffer = LogBuffer()
    custom_time = datetime.utcnow() - timedelta(hours=1)
    buffer.add("Archiv", timestamp=custom_time)
    assert buffer.entries()[0].timestamp.replace(microsecond=0) == custom_time.replace(
        microsecond=0
    )


def test_logbuffer_exports_json_lines():
    buffer = LogBuffer()
    buffer.add("A")
    exported = buffer.export_json_lines()
    loaded = [json.loads(line) for line in exported.splitlines() if line]
    assert loaded[0]["message"] == "A"
    assert loaded[0]["level"] in LOG_LEVELS
