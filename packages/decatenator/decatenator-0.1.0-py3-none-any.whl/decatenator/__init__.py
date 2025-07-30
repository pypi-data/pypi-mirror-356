"""
decat public package interface.
"""

from importlib.metadata import version as _v

from ._core import extract_files, write_files  # re-export

__all__ = ["extract_files", "write_files"]

__version__: str
try:
    __version__ = _v(__name__)
except Exception:  # pragma: no cover
    __version__ = "0.0.0"
