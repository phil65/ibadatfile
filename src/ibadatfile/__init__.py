from __future__ import annotations

from importlib.metadata import version

__version__ = version("ibadatfile")

from .ibadatfile import IbaChannel, IbaDatFile, read_ibadat

__all__ = [
    "__version__","IbaChannel", "IbaDatFile", "read_ibadat"]

name = "ibadatfile"