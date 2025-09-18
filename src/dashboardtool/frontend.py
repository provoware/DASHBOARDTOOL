"""Einfacher HTML-Renderer für das Dashboard."""

from __future__ import annotations

from html import escape
from typing import Any, Dict


def _render_header(header: Dict[str, Any]) -> str:
    clock = header.get("clock", {})
    clock_html = (
        f"<time datetime='{escape(clock.get('iso', ''))}'>{escape(clock.get('readable', ''))}</time>"
        if clock
        else ""
    )
    return (
        "<header class='dt-header'>"
        f"<h1>{escape(header.get('title', 'DashboardTool'))}</h1>"
        f"<p class='dt-subtitle'>{escape(header.get('subtitle', ''))}</p>"
        f"<div class='dt-clock'>{clock_html}</div>"
        "</header>"
    )


def _render_status(status: Dict[str, Any]) -> str:
    autosave = status.get("autosave", {})
    directories = status.get("storage_directories", [])
    dirs_html = "".join(f"<li>{escape(path)}</li>" for path in directories)
    return (
        "<section class='dt-status'>"
        "<h2>Status</h2>"
        f"<p>Autosave-Intervall: {escape(str(autosave.get('interval_minutes', '0')))} Minuten</p>"
        f"<p>Nächster Lauf: {escape(autosave.get('next_run_hint', ''))}</p>"
        f"<ul class='dt-storage'>{dirs_html}</ul>"
        "</section>"
    )


def _render_sidebar(layout: Dict[str, Any]) -> str:
    sidebar = layout.get("sidebar", {})
    items = sidebar.get("items", [])
    items_html = "".join(
        f"<li><button data-module='{escape(item.get('identifier', ''))}'>"
        f"{escape(item.get('label', ''))}</button></li>"
        for item in items
    )
    return (
        "<nav class='dt-sidebar' aria-label='Sidebar'>"
        "<h2>Module</h2>"
        f"<ul>{items_html}</ul>"
        "</nav>"
    )


def _render_modules(modules: list[Dict[str, Any]]) -> str:
    tiles = []
    for module in modules:
        payload = module.get("payload", {})
        status = payload.get("status")
        status_html = ""
        if isinstance(status, dict):
            status_html = (
                "<ul class='dt-module-status'>"
                + "".join(
                    f"<li><strong>{escape(str(key))}:</strong> {escape(str(value))}</li>"
                    for key, value in status.items()
                )
                + "</ul>"
            )
        tiles.append(
            "<article class='dt-module' id='module-"
            + escape(module.get("identifier", ""))
            + "'>"
            + f"<header><h3>{escape(module.get('display_name', 'Modul'))}</h3>"
            + f"<p>{escape(module.get('description', ''))}</p></header>"
            + status_html
            + "</article>"
        )
    return "<section class='dt-modules'>" + "".join(tiles) + "</section>"


def _render_validation(validation: Dict[str, Any]) -> str:
    if not validation:
        return ""
    info = f"<p>Fehler: {validation.get('error_count', 0)}, Hinweise: {validation.get('warning_count', 0)}</p>"
    return "<section class='dt-validation'><h2>Prüfungen</h2>" + info + "</section>"


def _render_notifications(notifications: list[Dict[str, Any]]) -> str:
    if not notifications:
        return ""
    items = "".join(
        f"<li class='dt-note-{escape(note.get('type', 'info'))}'>"
        f"{escape(note.get('message', ''))}</li>"
        for note in notifications
    )
    return (
        "<section class='dt-notifications'><h2>Hinweise</h2><ul>"
        + items
        + "</ul></section>"
    )


def render_html(model: Dict[str, Any]) -> str:
    """Konvertiert das Dashboard-Modell in eine eigenständige HTML-Seite."""

    header_html = _render_header(model.get("header", {}))
    status_html = _render_status(model.get("status", {}))
    sidebar_html = _render_sidebar(model.get("layout", {}))
    modules_html = _render_modules(model.get("modules", []))
    validation_html = _render_validation(model.get("validation", {}))
    notifications_html = _render_notifications(model.get("notifications", []))
    css_variables = model.get("layout", {}).get("css_variables", {})
    css_custom_props = "".join(
        f"--{escape(name)}: {escape(str(value))};"
        for name, value in css_variables.items()
    )
    html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <title>{escape(model.get('header', {}).get('title', 'DashboardTool'))}</title>
  <style>
    :root {{{css_custom_props}}}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #f5f7fb; }}
    .dt-header {{ background: #0d1b2a; color: white; padding: 2rem; }}
    .dt-subtitle {{ margin: 0; opacity: 0.8; }}
    .dt-layout {{ display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}
    .dt-sidebar {{ background: #1b263b; color: #fff; padding: 1.5rem; }}
    .dt-sidebar ul {{ list-style: none; padding: 0; }}
    .dt-sidebar button {{ width: 100%; margin-bottom: 0.5rem; padding: 0.75rem; border: none; border-radius: 0.5rem; background: #415a77; color: #fff; cursor: pointer; }}
    .dt-content {{ padding: 2rem; display: grid; gap: 1.5rem; }}
    .dt-status, .dt-notifications, .dt-validation {{ background: #fff; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.1); }}
    .dt-modules {{ display: grid; gap: 1.5rem; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }}
    .dt-module {{ background: #fff; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 15px 40px rgba(15, 23, 42, 0.08); }}
    .dt-module-status {{ list-style: none; padding: 0; margin-top: 1rem; }}
    .dt-module-status li {{ margin-bottom: 0.5rem; }}
    @media (max-width: 900px) {{ .dt-layout {{ grid-template-columns: 1fr; }} .dt-sidebar {{ grid-row: 2; }} }}
  </style>
</head>
<body>
  {header_html}
  <div class="dt-layout">
    {sidebar_html}
    <main class="dt-content">
      {status_html}
      {notifications_html}
      {validation_html}
      {modules_html}
    </main>
  </div>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in html.strip().splitlines()) + "\n"
