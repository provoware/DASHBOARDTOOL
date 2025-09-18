# Benutzerhilfe und Entwicklerleitfaden

## Schneller Einstieg für Anwenderinnen und Anwender
- **Dashboard starten:**
  1. Terminal (Eingabefenster) öffnen.
  2. Virtuelle Umgebung aktivieren: `source .venv/bin/activate`
  3. Dashboard-Daten als Übersicht anzeigen:
     ```bash
     python - <<'PY'
     from modules.notes import NotesModule
     from src.dashboardtool import DashboardApp
     app = DashboardApp([NotesModule()])
     print(app.render()["status"])
     PY
     ```
- **Module bedienen:**
  - Linke Sidebar (Seitenleiste) nutzen, um Module mit der Tastenkombination (Tastenkürzel: gleichzeitiges Drücken mehrerer Tasten) `CTRL+ALT+F` in den Fokus zu holen.
  - Aktionen wie "Fenster lösen" (Modul als separates Fenster) über das Zahnrad-Menü oder die Tasten `CTRL+ALT+D` auslösen.
- **Notizen sichern:**
  - Eigene Texte im Notizmodul eingeben und für ein Sofort-Speichern den Button "Jetzt speichern" betätigen oder das Tastenkürzel `CTRL+ALT+S` drücken.
  - Autosave (automatisches Speichern) läuft nach jeder Eingabe, nach Ablauf des Intervalls und beim Beenden automatisch.
- **Fehler verstehen:**
  - Rote Meldungen beschreiben fehlende Angaben in einfacher Sprache.
  - Unter jeder Meldung stehen Vorschläge, die Schritt für Schritt erklären, welche Taste oder welcher Button hilft.

## Hilfreiche Routinen
- **Logdatei prüfen:**
  ```bash
  python - <<'PY'
  from pathlib import Path
  log_file = Path("var/log/dashboardtool/debug.log")
  if log_file.exists():
      print(log_file.read_text(encoding="utf-8"))
  else:
      print("Noch keine Logdatei vorhanden – einfach im Debug-Modul einen Eintrag erzeugen.")
  PY
  ```
- **Theme (Farbschema) wechseln:**
  ```bash
  python - <<'PY'
  from src.dashboardtool import DashboardApp
  from modules.notes import NotesModule
  app = DashboardApp([NotesModule()], active_theme="forest")
  print(app.render()["themes"])
  PY
  ```
- **Validierung (Überprüfung) neu auslösen:**
  ```bash
  python - <<'PY'
  from modules.notes import NotesModule
  from src.dashboardtool import DashboardApp
  app = DashboardApp([NotesModule()])
  print(app.render()["validation"])
  PY
  ```

## Leitfaden für Entwicklerinnen und Entwickler
- **Tests ausführen:** `make test`
- **Code formatieren:** `make format`
- **Erweiterte Vorschau erzeugen:**
  ```bash
  python - <<'PY'
  from modules.base import ModuleContext
  from modules.notes import NotesModule
  from modules.debug import DebugModule
  from src.dashboardtool import DashboardApp

  ctx = ModuleContext()
  app = DashboardApp([NotesModule(context=ctx), DebugModule(context=ctx)])
  from pprint import pprint
  pprint(app.render())
  PY
  ```
- **Module erweitern:**
  1. Neue Klasse von `DashboardModule` ableiten.
  2. `identifier`, `display_name` und `description` setzen.
  3. In `render()` mindestens `component` und `title` liefern.
  4. Tests unter `tests/` ergänzen, damit die automatische Prüfung alles abdeckt.
- **Logs exportieren:**
  ```bash
  python - <<'PY'
  from pathlib import Path
  from modules.debug import DebugModule
  module = DebugModule()
  destination = module.export_snapshot(Path("var/log/dashboardtool/debug_snapshot.jsonl"))
  print(f"Snapshot gespeichert unter: {destination}")
  PY
  ```

Diese Übersicht ergänzt die technische Dokumentation und sorgt dafür, dass sowohl Einsteigerinnen als auch Entwicklerinnen sofort handlungsfähig sind.
