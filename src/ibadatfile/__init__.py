"""IbaDatFile: main package.

Read iba PDA .dat measurement files into numpy arrays and pandas DataFrames.
"""

from importlib.metadata import version

__version__ = version("ibadatfile")
__title__ = "IbaDatFile"

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
