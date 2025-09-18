"""Hilfsprogramm zur automatischen Einrichtung einer virtuellen Umgebung."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, Iterable


CommandRunner = Callable[..., subprocess.CompletedProcess]


def _pip_executable(venv_path: Path) -> Path:
    """Ermittelt den Pfad zur Pip-Datei der virtuellen Umgebung."""

    if os.name == "nt":
        return venv_path / "Scripts" / "pip.exe"
    return venv_path / "bin" / "pip"


def create_virtualenv(
    venv_path: Path, python_executable: str | None = None, dry_run: bool = False
) -> str:
    """Erstellt eine virtuelle Umgebung, falls noch nicht vorhanden."""

    if python_executable is None:
        python_executable = sys.executable

    if venv_path.exists() and (venv_path / "pyvenv.cfg").exists():
        return "exists"

    if dry_run:
        return "planned"

    venv_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [python_executable, "-m", "venv", str(venv_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            'Python-Interpreter nicht gefunden ("Interpreter": Programm zum Ausführen).'
        ) from error
    except subprocess.CalledProcessError as error:  # pragma: no cover - selten
        raise RuntimeError(
            "Anlegen der virtuellen Umgebung ist fehlgeschlagen."
        ) from error
    return "created"


def install_requirements(
    venv_path: Path,
    requirements_file: Path,
    upgrade: bool = False,
    dry_run: bool = False,
    runner: CommandRunner | None = None,
) -> None:
    """Installiert Abhängigkeiten mit hilfreichem Fehlertext."""

    runner = runner or subprocess.run
    pip_path = _pip_executable(venv_path)
    if not pip_path.exists():
        raise RuntimeError(
            'Pip wurde in der virtuellen Umgebung nicht gefunden ("Pip": Paketmanager).'
        )

    if not requirements_file.exists():
        raise RuntimeError(
            f"Die Datei {requirements_file} konnte nicht gefunden werden."
        )

    if dry_run:
        return

    command: list[str] = [str(pip_path), "install", "-r", str(requirements_file)]
    if upgrade:
        command.insert(2, "--upgrade")

    try:
        runner(command, check=True)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            "Installation der Abhängigkeiten ist fehlgeschlagen. Bitte Ausgabe prüfen."
        ) from error


def parse_args(arguments: Iterable[str] | None = None) -> argparse.Namespace:
    """Parst Kommandozeilenargumente für das Hilfsprogramm."""

    parser = argparse.ArgumentParser(
        description=(
            'Richtet eine virtuelle Umgebung ("virtuelle Umgebung": abgeschotteter Arbeitsbereich) ein.'
        )
    )
    parser.add_argument(
        "--venv-path",
        default=".venv",
        help="Zielordner für die virtuelle Umgebung",
    )
    parser.add_argument(
        "--requirements",
        default="requirements-dev.txt",
        help="Pfad zur Abhängigkeitsliste",
    )
    parser.add_argument(
        "--python",
        default=None,
        help="Alternativer Python-Interpreter",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Bestehende Pakete aktualisieren",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Nur Schritte anzeigen, nichts ausführen",
    )
    return parser.parse_args(list(arguments) if arguments is not None else None)


def main(arguments: Iterable[str] | None = None) -> int:
    """Einstiegspunkt für die Befehlszeile."""

    args = parse_args(arguments)
    venv_path = Path(args.venv_path).expanduser().resolve()
    requirements = Path(args.requirements).expanduser().resolve()

    print("➡️  Schritt 1/2: Virtuelle Umgebung prüfen/erstellen …")
    try:
        state = create_virtualenv(venv_path, args.python, dry_run=args.dry_run)
    except RuntimeError as error:
        print(f"❌ {error}")
        return 1

    if state == "exists":
        print("✅ Umgebung bereits vorhanden – wird wiederverwendet.")
    elif state == "created":
        print(f"✅ Neue Umgebung angelegt unter {venv_path}.")
    else:
        print(
            "ℹ️  Trockenlauf: Umgebung würde angelegt werden (keine Änderungen durchgeführt)."
        )

    print("➡️  Schritt 2/2: Abhängigkeiten installieren …")
    if args.dry_run:
        print(
            "ℹ️  Trockenlauf: Installation übersprungen. "
            "Nutzen Sie den Befehl erneut ohne --dry-run."
        )
        return 0

    try:
        install_requirements(
            venv_path, requirements, upgrade=args.upgrade, dry_run=False
        )
    except RuntimeError as error:
        print(f"❌ {error}")
        return 1

    print("✅ Alle Pakete wurden erfolgreich installiert. Viel Erfolg beim Start!")
    return 0


if __name__ == "__main__":  # pragma: no cover - direkter Aufruf
    sys.exit(main())
