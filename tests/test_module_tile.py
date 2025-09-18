from pathlib import Path

from modules.base import DashboardModule, ModuleContext, ModuleValidationResult
from modules.notes import NotesModule
from src.dashboardtool.config import DashboardConfig
from src.dashboardtool.themes import THEME_PRESETS


def test_render_dashboard_tile_contains_metadata(tmp_path: Path) -> None:
    context = ModuleContext(storage_path=tmp_path / "data")
    module = NotesModule(context=context)

    tile = module.render_dashboard_tile()

    assert tile["layout"]["min_width"] == context.config.standards.min_width
    assert any(action["name"] == "detach" for action in tile["actions"])
    assert tile["validation"]["is_valid"]
    assert tile["validation"]["solutions"] == []
    assert "summary" in tile["validation"]
    assert tile["payload"]["theme"]["background"].startswith("#")


def test_render_dashboard_tile_falls_back_to_available_theme(tmp_path: Path) -> None:
    config = DashboardConfig(themes={"sunrise": THEME_PRESETS["sunrise"]})
    context = ModuleContext(config=config, storage_path=tmp_path / "data")

    class CustomModule(DashboardModule):
        identifier = "custom"
        display_name = "Custom"
        description = "Test"

        def render(self) -> dict[str, object]:
            return {
                "component": "custom",
                "title": "Custom",
                "theme": "sunrise",
            }

    module = CustomModule(context=context)
    tile = module.render_dashboard_tile()

    assert tile["payload"]["theme"] == config.themes["sunrise"]
    assert any("Theme" in message for message in tile["validation"]["errors"])


def test_invalid_shortcuts_are_replaced_and_reported(tmp_path: Path) -> None:
    context = ModuleContext(storage_path=tmp_path / "data")

    class ShortcutModule(DashboardModule):
        identifier = "shortcut"
        display_name = "Shortcut"
        description = ""

        def render(self) -> dict[str, object]:
            return {
                "component": "shortcut",
                "title": "Shortcut",
                "keyboard_shortcuts": "invalid",
            }

    module = ShortcutModule(context=context)
    tile = module.render_dashboard_tile()

    assert tile["payload"]["keyboard_shortcuts"]["focus"]
    assert any("Tastenkürzel" in msg for msg in tile["validation"]["errors"])


def test_validation_result_removes_duplicates() -> None:
    result = ModuleValidationResult(
        errors=["", "Fehler", "Fehler"],
        warnings=[" Hinweis "],
        solutions=["A", "A"],
    )

    assert result.errors == ["Fehler"]
    assert result.warnings == ["Hinweis"]
    assert result.solutions == ["A"]
