# DASHBOARDTOOL

Dieses Projekt bildet die Grundlage für ein modulares Dashboard mit hohen
Qualitätsansprüchen an Optik, Tests und Selbstheilungsmechanismen.

## Schnellstart
1. Vollautomatische Einrichtung der virtuellen Umgebung ("virtuelle Umgebung":
   abgeschottete Arbeitsumgebung) inklusive Abhängigkeiten:
   ```bash
   make setup
   ```
   Der Befehl ruft `python -m tools.venv_setup` auf und liefert leicht verständliche
   Rückmeldungen.
2. Code formatieren ("Formatierer": Werkzeug für einheitlichen Code-Stil):
   ```bash
   make format
   ```
3. Tests ("Tests": automatische Prüfprogramme) ausführen:
   ```bash
   make test
   ```
4. PHP-Syntaxprüfung durchführen:
   ```bash
   make php-lint
   ```

## Projektstruktur
- `src/dashboardtool/`: Zentrale Konfigurationen, Themes und Layouts.
- `src/dashboardtool/gui.py`: Baut die komplette GUI-Struktur samt Sidebar und
  Responsiv-Verhalten als leicht verständliches Datenobjekt auf.
- `modules/`: Basismodul plus Beispiel-Module, alle folgen den Standards.
- `modules/php/`: PHP-Komponenten, werden automatisch per `php -l` geprüft.
- `tests/`: Pytest-basierte ("Pytest": Python-Testframework) Tests für Module und Checks.
- `tools/`: Skripte für Entwicklungsaufgaben, z.B. PHP-Syntaxprüfung und
  `venv_setup.py` für die automatische Umgebungseinrichtung.
- `docs/`: Dokumentationen mit Modul-Standards und Design-Vorgaben.

## Automatisierung
- `make setup` legt eine neue virtuelle Umgebung an oder aktualisiert sie.
- `make format` ruft `black` auf, um Python-Dateien zu formatieren.
- `make lint` führt Formatierung plus Pytest und PHP-Check aus.
- `make php-lint` verwendet `tools/php_syntax_check.py`.

## Verfügbare Module
- **Notizbereich** (`modules/notes.py`): Speichert Texte persistent und liefert
  Autosave-Hinweise inklusive Auslöserliste ("Auslöser": Ereignis, das etwas
  startet). Die Oberfläche ergänzt das Zielverzeichnis automatisch aus den
  Metadaten, sodass keine doppelten Angaben nötig sind.
- **Diagnosemodul** (`modules/debug.py`): Schreibt Echtzeit-Logs ("Log":
  Protokollzeile) in `var/log/dashboardtool/debug.log`, stellt gefilterte Listen
  bereit und sorgt für Selbstheilung, indem alte Protokolle beim Start geladen
  werden.

## Farb- und Layoutrichtlinien
Die Datei `src/dashboardtool/themes.py` definiert vier kontrastreiche Farbwelten und
liefert Hilfsfunktionen, um Kontrastwerte zu prüfen. Layout-Vorgaben inklusive
Breakpoints ("Breakpoint": Umschaltpunkt für responsives Verhalten) stehen in
`src/dashboardtool/layout.py`. Weitere Details zu Modul-Standards finden sich in
`docs/module_standards.md`.

## Weiterentwicklung
- Module sollen sich an `ModuleStandard` orientieren und Tastenkürzel anbieten.
- `DashboardApp` bündelt Module zu einem vollwertigen GUI-Modell inklusive
  Sidebar, Validierung und Selbstheilungs-Checks mit laienfreundlichen
  Lösungsvorschlägen pro Modul.
- Selbstheilung: Bei fehlenden Ressourcen muss das Modul automatisch Ersatz anlegen.
- Barrierefreiheit hat Priorität: klare Kontraste, Fokus-Ringe, Screenreader-Texte.
- Debugging-Tools speichern strukturierte JSON-Zeilen, sodass Support-Teams
  Fehler auch ohne Spezialwissen nachvollziehen können.
