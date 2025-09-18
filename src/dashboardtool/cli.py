"""Kommandozeileneinstieg für DashboardTool ("Kommandozeile": Texteingabe)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from modules.debug import DebugModule
from modules.notes import NotesModule

from .gui import DashboardApp


def _build_default_modules() -> Sequence:
    """Stellt Standardmodule für die GUI zusammen."""

    return [NotesModule(), DebugModule()]


def _export_html(output: Path) -> Path:
    """Speichert die aktuelle Oberfläche als HTML-Datei."""

    from .frontend import render_html

    app = DashboardApp(_build_default_modules())
    html = render_html(app.render())
    output.write_text(html, encoding="utf-8")
    return output


def _export_json(output: Path) -> Path:
    """Exportiert das Dashboard-Modell als JSON ("JSON": Textformat)."""

    app = DashboardApp(_build_default_modules())
    model = app.render()
    output.write_text(json.dumps(model, indent=2, ensure_ascii=False), encoding="utf-8")
    return output


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Erstellt HTML- oder JSON-Ausgaben des modularen DashboardTools "
            "für schnelle Vorschauen."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dashboard.html"),
        help="Zielpfad für die Ausgabe-Datei",
    )
    parser.add_argument(
        "--format",
        choices=("html", "json"),
        default="html",
        help="Ausgabeformat (html: Webseite, json: Rohdaten)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Startpunkt für den Konsolenaufruf."""

    args = _parse_args(argv)
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "html":
        result_path = _export_html(output)
    else:
        result_path = _export_json(output)
    print(f"Dashboard erfolgreich nach {result_path} exportiert.")


if __name__ == "__main__":  # pragma: no cover - direkt ausführbar
    main()
