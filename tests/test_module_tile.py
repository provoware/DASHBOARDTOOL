from pathlib import Path

from modules.base import ModuleContext
from modules.notes import NotesModule


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
