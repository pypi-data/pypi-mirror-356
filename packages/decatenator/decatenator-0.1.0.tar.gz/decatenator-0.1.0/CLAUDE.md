# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeCat is a command-line utility that extracts code blocks from Markdown files into real source files. It's the inverse of the `catenator` tool - it takes Markdown files with level-3 headings (`###`) that are file paths and writes the fenced code blocks that follow each heading to actual files on disk.

## Architecture

- **Core Logic**: `src/decat/_core.py` contains the main parsing logic with two key functions:
  - `extract_files()`: Parses Markdown lines and yields (filepath, code) tuples
  - `write_files()`: Writes extracted code to files on disk
- **CLI Interface**: `src/decat/cli.py` handles command-line argument parsing and stdin/file input
- **Package Interface**: `src/decat/__init__.py` re-exports core functions for programmatic use

The parsing algorithm looks for level-3 headings with file paths, then captures fenced code blocks that follow until the closing fence.

## Common Commands

### Development
```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Run a specific test
python -m pytest tests/test_core.py::test_extract_files_simple

# Build package
python -m build

# Clean build artifacts
rm -rf dist/ build/ src/*.egg-info/
```

### PyPI Publishing
```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the built package
twine check dist/*

# Upload to Test PyPI (optional)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Install from PyPI
pip install decat
```

### Usage
```bash
# Extract files from Markdown to current directory
decat input.md

# Extract files to specific output directory
decat input.md -o /path/to/output

# Read from stdin
cat input.md | decat -

# Show version
decat --version
```

## Key Implementation Details

- Uses regex patterns to match level-3 headings (`^###\s+([^\s]+)\s*$`) and code fences
- Supports reading from files or stdin (use `-` as filename)
- Creates parent directories automatically when writing files
- Proper error handling for missing or unterminated code blocks
- Uses setuptools build system with entry point configuration in pyproject.toml