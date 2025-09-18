from pathlib import Path

import pytest

from modules.base import DashboardModule, ModuleContext
from modules.debug import DebugModule
from modules.notes import NotesModule
from src.dashboardtool import DashboardApp


@pytest.fixture()
def module_context(tmp_path: Path) -> ModuleContext:
    return ModuleContext(storage_path=tmp_path / "data")


def test_dashboard_app_render_structure(module_context: ModuleContext) -> None:
    app = DashboardApp(
        [NotesModule(context=module_context), DebugModule(context=module_context)]
    )
    payload = app.render()

    assert payload["layout"]["sidebar"]["items"], "Sidebar sollte Module enthalten"
    assert "--grid-columns" in payload["layout"]["css_variables"]
    assert payload["themes"]["active"] in payload["themes"]["available"]
    assert payload["validation"]["modules"]["notes"]["is_valid"]
    assert payload["validation"]["error_count"] == 0
    assert payload["keyboard_navigation"]["module_shortcuts"]["focus"]


def test_dashboard_app_rejects_duplicate_identifiers(
    module_context: ModuleContext,
) -> None:
    notes_a = NotesModule(context=module_context)
    notes_b = NotesModule(context=module_context)
    with pytest.raises(ValueError):
        DashboardApp([notes_a, notes_b])


class BrokenModule(DashboardModule):
    identifier = "broken"
    display_name = "Defektes Modul"
    description = "Fehlende Pflichtangaben"

    def render(self) -> dict[str, object]:
        return {}


def test_self_healing_includes_solutions(module_context: ModuleContext) -> None:
    broken = BrokenModule(context=module_context)
    payload = DashboardApp([broken]).render()

    actions = payload["self_healing"]["recommended_actions"]
    assert any("meldet fehlende Felder" in action for action in actions)
    assert any("Theme" in action or "Farben" in action for action in actions)
