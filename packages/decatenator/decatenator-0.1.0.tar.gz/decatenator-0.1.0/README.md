# DeCatenator

`decat` is a small command-line tool that unpacks code embedded in Markdown.
It reads headings that look like file paths and writes the accompanying code
to real files.

* **Input rule** – a level-2 or level-3 heading whose *text is a single path
  segment* (no spaces).
  Examples: `## main.py`, `### src/utils/helpers.js`.
  Anything with spaces (e.g. `## My Heading`) is ignored.
* **Code source**
  * If the heading is followed (after optional blank lines) by a fenced block
    opened with triple back-ticks, those lines become the file content.
    The closing fence *must be exactly* ` ``` ` (no language tag).
  * Otherwise, all lines until the next matching heading (or EOF) are taken
    as the file content.
* Creates parent directories as needed and overwrites existing files.
* Works with a file argument or `stdin`.
> **Note:** This project is the inverse of [Catenator](https://github.com/philiporange/catenator).

---

## Quick start

```bash
pip install decat
````

### CLI

```bash
# write files into the current directory
decat article.md

# write into a different root
decat article.md -o ./extracted

# read from stdin
cat article.md | decat -

# version
decat --version
```

### Example – fenced

````
### src/hello.py
```python
print("Hello, world!")
````

````

Running `decat readme.md` generates `src/hello.py` containing:

```python
print("Hello, world!")
````

### Example – unfenced

```
## scripts/build.sh
#!/usr/bin/env bash
echo "building"
```

`decat docs.md` writes `scripts/build.sh` with the two lines above.

---

## Programmatic use

```python
from pathlib import Path
from decat import extract_files, write_files

with open("notes.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

pairs = extract_files(lines)            # yields (rel_path, code)
write_files(pairs, Path("out"))         # creates ./out/...
```

---

## How it works

* **Regex** `^#{2,3}\s+([^\s]+)\s*$` recognises valid headings.
* Searches forward:

  * if the next non-blank line matches `^```.*$`, capture until a bare \`\`\`;
    otherwise capture until the next valid heading.
* Raises `SyntaxError` if a fenced block is unterminated.
* All IO logic is isolated in `src/decat/_core.py`; CLI lives in
  `src/decat/cli.py`.

---

## Repository layout

```
./
│   README.md
│   pyproject.toml
│   MANIFEST.in
├── src/
│   └── decat/
│       ├── _core.py
│       ├── cli.py
│       └── __init__.py
└── tests/
    └── test_core.py
```

---

## Development

```bash
# editable install
pip install -e .

# run the test suite
pytest

# build sdist & wheel
python -m build

# upload (requires credentials)
twine upload dist/*
```
