from pathlib import Path

from dashboardtool.cli import main as cli_main
from dashboardtool.frontend import render_html
from dashboardtool.gui import DashboardApp
from modules.debug import DebugModule
from modules.notes import NotesModule


def test_render_html_contains_modules():
    app = DashboardApp([NotesModule(), DebugModule()])
    html = render_html(app.render())
    assert "Notizbereich" in html
    assert "Diagnose" in html
    assert "Autosave-Intervall" in html


def test_cli_exports_html(tmp_path: Path, capsys):
    output = tmp_path / "dashboard.html"
    cli_main(["--output", str(output), "--format", "html"])
    captured = capsys.readouterr().out
    assert output.exists()
    assert "erfolgreich" in captured
    assert "<html" in output.read_text(encoding="utf-8")
