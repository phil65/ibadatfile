"""IbaDatFile: Pythonic wrapper for IBA dat file DLL"""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("ibadatfile")
__title__ = "IbaDatFile"
__description__ = "Pythonic wrapper for IBA dat file DLL"
__author__ = "Philipp Temminghoff"
__author_email__ = "philipptemminghoff@googlemail.com"
__copyright__ = "Copyright (c) 2025 Philipp Temminghoff"
__license__ = "MIT"
__url__ = "https://github.com/phil65/ibadatfile"

from .ibadatfile import IbaChannel, IbaDatFile, read_ibadat

__all__ = [
    "IbaChannel",
    "IbaDatFile",
    "__version__",
    "read_ibadat",
]

name = "ibadatfile"
