#!/usr/bin/env python3
"""
CLI entry point for *DeCat*.

This script is installed as the ``decat`` console tool (see
``pyproject.toml``).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ._core import extract_files, write_files
from . import __version__


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="decat",
        description="Unpack Markdown-embedded code into real source files.",
    )
    parser.add_argument(
        "markdown",
        type=Path,
        help="Markdown file to unpack (use '-' to read from stdin)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory to place extracted files (default: current dir)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> None:  # noqa: D401
    """
    Run the command-line interface.

    Parameters
    ----------
    argv
        Argument list; defaults to ``sys.argv[1:]`` when *None*.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.markdown == Path("-"):
        lines = sys.stdin.readlines()
    else:
        lines = args.markdown.read_text(encoding="utf-8").splitlines(keepends=True)

    try:
        write_files(extract_files(lines), args.output_dir.resolve())
    except SyntaxError as exc:
        parser.error(str(exc))


if __name__ == "__main__":  # pragma: no cover
    main()
