# DASHBOARDTOOL

Dieses Projekt bildet die Grundlage für ein modulares Dashboard mit hohen
Qualitätsansprüchen an Optik, Tests und Selbstheilungsmechanismen.

## Schnellstart
1. Virtuelle Umgebung ("virtuelle Umgebung": abgeschottete Arbeitsumgebung) anlegen:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   ```
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
- `modules/`: Basismodul plus Beispiel-Module, alle folgen den Standards.
- `modules/php/`: PHP-Komponenten, werden automatisch per `php -l` geprüft.
- `tests/`: Pytest-basierte ("Pytest": Python-Testframework) Tests für Module und Checks.
- `tools/`: Skripte für Entwicklungsaufgaben, z.B. PHP-Syntaxprüfung.
- `docs/`: Dokumentationen mit Modul-Standards und Design-Vorgaben.

## Automatisierung
- `make format` ruft `black` auf, um Python-Dateien zu formatieren.
- `make lint` führt Formatierung plus Pytest und PHP-Check aus.
- `make php-lint` verwendet `tools/php_syntax_check.py`.

## Farb- und Layoutrichtlinien
Die Datei `src/dashboardtool/themes.py` definiert vier kontrastreiche Farbwelten.
Layout-Vorgaben sind in `src/dashboardtool/layout.py` dokumentiert. Weitere Details
zu Modul-Standards stehen in `docs/module_standards.md`.

## Weiterentwicklung
- Module sollen sich an `ModuleStandard` orientieren und Tastenkürzel anbieten.
- Selbstheilung: Bei fehlenden Ressourcen muss das Modul automatisch Ersatz anlegen.
- Barrierefreiheit hat Priorität: klare Kontraste, Fokus-Ringe, Screenreader-Texte.
