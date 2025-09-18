from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tools import venv_setup


def test_dry_run_creates_no_environment(tmp_path, capsys):
    env_path = tmp_path / "venv"
    exit_code = venv_setup.main(
        [
            "--venv-path",
            str(env_path),
            "--requirements",
            str(tmp_path / "reqs.txt"),
            "--dry-run",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Trockenlauf" in captured.out
    assert not env_path.exists()


def test_install_requirements_reports_failure(tmp_path):
    env_path = tmp_path / "env"
    bin_dir = env_path / "bin"
    bin_dir.mkdir(parents=True)
    pip_path = bin_dir / "pip"
    pip_path.write_text("#!/bin/sh\n")
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("pytest==0.0.0\n")

    def failing_runner(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0])

    with pytest.raises(RuntimeError):
        venv_setup.install_requirements(env_path, req_file, runner=failing_runner)


def test_install_requirements_checks_missing_files(tmp_path):
    env_path = tmp_path / "env"
    bin_dir = env_path / "bin"
    bin_dir.mkdir(parents=True)
    pip_path = bin_dir / "pip"
    pip_path.write_text("#!/bin/sh\n")

    with pytest.raises(RuntimeError):
        venv_setup.install_requirements(env_path, Path("missing.txt"))
