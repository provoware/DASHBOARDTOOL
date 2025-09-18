from dataclasses import replace
from pathlib import Path

import pytest

from modules.base import ModuleContext
from modules.debug import DebugModule
from src.dashboardtool import DEFAULT_CONFIG


@pytest.fixture()
def tmp_context(tmp_path: Path) -> ModuleContext:
    config = replace(DEFAULT_CONFIG, log_directory=tmp_path / "logs")
    return ModuleContext(config=config, storage_path=tmp_path / "data")


def test_debug_module_logs_and_persists(tmp_context: ModuleContext) -> None:
    module = DebugModule(context=tmp_context)
    module.log_event("Test", level="info", source="unit")
    payload = module.render()
    assert payload["entries"], "Es sollten Einträge vorhanden sein"
    assert Path(payload["log_file"]).exists()
    assert payload["log_levels"][0] == "debug"


def test_debug_module_limit_and_clear(tmp_context: ModuleContext) -> None:
    module = DebugModule(context=tmp_context)
    for index in range(5):
        module.log_event(f"Eintrag {index}", level="warning")
    recent = module.get_recent(limit=3)
    assert len(recent) == 3
    module.clear_events()
    assert module.get_recent() == []
    assert not Path(module.log_file).exists()


def test_debug_module_rejects_invalid_level(tmp_context: ModuleContext) -> None:
    module = DebugModule(context=tmp_context)
    with pytest.raises(ValueError):
        module.log_event("Fehler", level="fatal")


def test_debug_module_restores_existing_log(tmp_context: ModuleContext) -> None:
    module = DebugModule(context=tmp_context)
    module.log_event("Alt", level="info")
    module2 = DebugModule(context=tmp_context)
    assert module2.render()["loaded_entries"] >= 1
