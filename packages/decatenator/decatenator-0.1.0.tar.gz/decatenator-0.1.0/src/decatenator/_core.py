"""
Core functionality for DeCat.

Split out from CLI wrapper so that it can be imported and unit-tested
without invoking argument parsing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable, Iterator, Tuple

# --- Regexes -----------------------------------------------------------

HEADING_RE = re.compile(
    r"^#{2,3}\s+([^\s]+)\s*$"
)  # Level-2 or Level-3 heading (single word only)
CODE_START_RE = re.compile(r"^```.*$")  # Opening code fence
CODE_END = "```"


def extract_files(lines: Iterable[str]) -> Iterator[Tuple[str, str]]:
    """
    Parse *lines* and yield ``(relative_path, code)`` tuples.

    The algorithm:

    1. Look for a level-2 or level-3 Markdown heading (## or ### filepath).
    2. If a fenced code block follows, capture content until closing fence.
    3. If no fenced code block, capture all content until next heading or EOF.

    Raises
    ------
    SyntaxError
        If a fenced code block is unterminated.
    """
    lines_list = list(lines)
    i = 0

    while i < len(lines_list):
        line = lines_list[i]
        m = HEADING_RE.match(line)
        if not m:
            i += 1
            continue

        filepath = m.group(1).strip()
        i += 1

        # Look ahead to see if there's a code fence
        code_lines: list[str] = []

        # Skip empty lines after heading
        while i < len(lines_list) and lines_list[i].strip() == "":
            i += 1

        if i < len(lines_list) and CODE_START_RE.match(lines_list[i]):
            # Found code fence - capture until closing fence
            i += 1  # Skip opening fence
            start_line = i

            while i < len(lines_list):
                if lines_list[i].rstrip() == CODE_END:
                    break
                code_lines.append(lines_list[i])
                i += 1
            else:
                raise SyntaxError(
                    f"Unterminated code block for {filepath} (began line {start_line})"
                )
            i += 1  # Skip closing fence
        else:
            # No code fence - capture content until next heading or EOF
            while i < len(lines_list):
                if HEADING_RE.match(lines_list[i]):
                    break
                code_lines.append(lines_list[i])
                i += 1

        yield filepath, "".join(code_lines)


def write_files(file_iter: Iterable[Tuple[str, str]], base_dir: Path) -> None:
    """
    Write each *code* blob from *file_iter* under *base_dir* preserving
    the relative path.

    Parameters
    ----------
    file_iter
        Iterable of ``(relative_path, code)`` pairs.
    base_dir
        Destination root directory (created if absent).
    """
    for rel_path, code in file_iter:
        dest = base_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(code, encoding="utf-8")
        print(f"Wrote {dest}", file=sys.stderr)
