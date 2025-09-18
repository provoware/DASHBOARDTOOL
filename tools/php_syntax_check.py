"""Prüft die Syntax aller PHP-Dateien mit `php -l`.

Falls kein PHP-Interpreter verfügbar ist, kann der Check optional übersprungen werden,
indem `--allow-missing-php` gesetzt wird. So lassen sich Tests auf Systemen ohne PHP
(tz. Entwicklungsrechner) trotzdem ausführen, während produktive Pipelines den Check
erzwingen können.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List


def discover_php_files(paths: Iterable[Path]) -> List[Path]:
    found: List[Path] = []
    for base in paths:
        if base.is_file() and base.suffix == ".php":
            found.append(base)
            continue
        if base.is_dir():
            for file in base.rglob("*.php"):
                if file.is_file():
                    found.append(file)
    return sorted(found)


def check_php_syntax(paths: Iterable[Path], allow_missing_php: bool = False) -> int:
    php_executable = subprocess.run(
        ["which", "php"],
        capture_output=True,
        text=True,
        check=False,
    )
    php_path = php_executable.stdout.strip()
    if not php_path:
        message = (
            "PHP-Interpreter nicht gefunden. Bitte PHP installieren oder "
            "--allow-missing-php verwenden."
        )
        if allow_missing_php:
            print(message)
            return 0
        print(message, file=sys.stderr)
        return 1

    php_files = discover_php_files(paths)
    if not php_files:
        print("Keine PHP-Dateien gefunden.")
        return 0

    exit_code = 0
    for file in php_files:
        result = subprocess.run(
            [php_path, "-l", str(file)], capture_output=True, text=True
        )
        if result.returncode != 0:
            exit_code = result.returncode
            print(result.stderr, file=sys.stderr)
        else:
            print(result.stdout.strip())
    return exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        default=[Path("modules")],
        type=Path,
        help="Verzeichnisse oder Dateien, die geprüft werden sollen.",
    )
    parser.add_argument(
        "--allow-missing-php",
        action="store_true",
        help="Wenn gesetzt, wird ein fehlender PHP-Interpreter nicht als Fehler gewertet.",
    )
    args = parser.parse_args(argv)
    return check_php_syntax(args.paths, allow_missing_php=args.allow_missing_php)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
