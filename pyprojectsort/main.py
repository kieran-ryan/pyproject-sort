"""pyprojectsort implementation."""
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any

import tomli as tomllib
import tomli_w

from pyprojectsort import __version__

DEFAULT_CONFIG = "pyproject.toml"


def _read_cli(args: list):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="pyprojectsort",
        description="Formatter for pyproject.toml files",
    )
    parser.add_argument("file", nargs="?", default=DEFAULT_CONFIG)
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="show package version and exit",
    )
    return parser.parse_args(args)


def _read_config_file(config: pathlib.Path):
    """Check configuration file exists."""
    if not config.is_file():
        print(f"No pyproject.toml detected at path: '{config}'")
        sys.exit(1)
    return config


def _parse_pyproject_toml(file: pathlib.Path) -> dict[str, Any]:
    """Parse pyproject.toml file."""
    with file.open("rb") as f:
        pyproject_toml = tomllib.load(f)
    return {k.replace("--", "").replace("-", "_"): v for k, v in pyproject_toml.items()}


def reformat_pyproject(pyproject: dict) -> dict:
    """Reformat pyproject toml file."""
    if isinstance(pyproject, dict):
        return {
            key: reformat_pyproject(value)
            for key, value in sorted(pyproject.items(), key=lambda item: item[0])
        }
    if isinstance(pyproject, list):
        return sorted(reformat_pyproject(item) for item in pyproject)
    return pyproject


def _save_pyproject(file, pyproject) -> None:
    """Write changes to pyproject.toml."""
    with file.open("wb") as f:
        tomli_w.dump(pyproject, f)


def main():
    """Run application."""
    args = _read_cli(sys.argv[1:])
    pyproject_file = _read_config_file(pathlib.Path(args.file))
    pyproject_toml = _parse_pyproject_toml(pyproject_file)
    reformatted_pyproject = reformat_pyproject(pyproject_toml)
    _save_pyproject(pyproject_file, reformatted_pyproject)
