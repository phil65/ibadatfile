# IbaDatFile

[![PyPI License](https://img.shields.io/pypi/l/ibadatfile.svg)](https://pypi.org/project/ibadatfile/)
[![Package status](https://img.shields.io/pypi/status/ibadatfile.svg)](https://pypi.org/project/ibadatfile/)
[![Monthly downloads](https://img.shields.io/pypi/dm/ibadatfile.svg)](https://pypi.org/project/ibadatfile/)
[![Distribution format](https://img.shields.io/pypi/format/ibadatfile.svg)](https://pypi.org/project/ibadatfile/)
[![Wheel availability](https://img.shields.io/pypi/wheel/ibadatfile.svg)](https://pypi.org/project/ibadatfile/)
[![Python version](https://img.shields.io/pypi/pyversions/ibadatfile.svg)](https://pypi.org/project/ibadatfile/)
[![Implementation](https://img.shields.io/pypi/implementation/ibadatfile.svg)](https://pypi.org/project/ibadatfile/)
[![Releases](https://img.shields.io/github/downloads/phil65/ibadatfile/total.svg)](https://github.com/phil65/ibadatfile/releases)
[![Github Contributors](https://img.shields.io/github/contributors/phil65/ibadatfile)](https://github.com/phil65/ibadatfile/graphs/contributors)
[![Github Forks](https://img.shields.io/github/forks/phil65/ibadatfile)](https://github.com/phil65/ibadatfile/forks)
[![Github Issues](https://img.shields.io/github/issues/phil65/ibadatfile)](https://github.com/phil65/ibadatfile/issues)
[![Github Issues](https://img.shields.io/github/issues-pr/phil65/ibadatfile)](https://github.com/phil65/ibadatfile/pulls)
[![Github Watchers](https://img.shields.io/github/watchers/phil65/ibadatfile)](https://github.com/phil65/ibadatfile/watchers)
[![Github Stars](https://img.shields.io/github/stars/phil65/ibadatfile)](https://github.com/phil65/ibadatfile/stars)
[![Github Repository size](https://img.shields.io/github/repo-size/phil65/ibadatfile)](https://github.com/phil65/ibadatfile)
[![Github last commit](https://img.shields.io/github/last-commit/phil65/ibadatfile)](https://github.com/phil65/ibadatfile/commits)
[![Github release date](https://img.shields.io/github/release-date/phil65/ibadatfile)](https://github.com/phil65/ibadatfile/releases)
[![Github language count](https://img.shields.io/github/languages/count/phil65/ibadatfile)](https://github.com/phil65/ibadatfile)
[![Github commits this month](https://img.shields.io/github/commit-activity/m/phil65/ibadatfile)](https://github.com/phil65/ibadatfile)
[![Package status](https://codecov.io/gh/phil65/ibadatfile/branch/main/graph/badge.svg)](https://codecov.io/gh/phil65/ibadatfile/)

[Read the documentation!](https://phil65.github.io/ibadatfile/)

Read iba PDA `.dat` measurement files from Python. `ibadatfile` wraps iba's
`ibaFilesLite.dll` COM server and returns channel data as numpy arrays and
pandas DataFrames with a proper time index.

## Requirements

- **Windows**: file access goes through COM (via `pywin32`). The package can be
  imported elsewhere, but opening a file needs Windows.
- `ibaFilesLite.dll` installed and registered:

  ```bat
  regsvr32 path\to\ibaFilesLite.dll
  ```

- The DLL's architecture must match your Python interpreter (32-bit DLL needs 32-bit
  Python, 64-bit DLL needs 64-bit Python).
- Python 3.13+.

## Installation

```bash
pip install ibadatfile
```

## Quickstart

Read a whole file into a DataFrame (one column per channel, `DatetimeIndex` named `time`):

```python
from ibadatfile import read_ibadat

df = read_ibadat("measurement.dat")
print(df.head())
```

Work with the file and its channels directly:

```python
from ibadatfile import IbaDatFile

with IbaDatFile("measurement.dat") as file:
    print(file.starttime(), file.clk(), file.frames())
    print(file.return_channel_names())

    for channel in file:
        print(channel.name(), channel.unit(), channel.is_bool())

    speed = file["speed"].series()  # look up a channel by name
```

## Features

- `read_ibadat()`: one call from path to DataFrame.
- `IbaDatFile`: context manager over a `.dat` file; iterate channels, look them up by
  name, query file info (start time, clock, frame count, signal count, recorder
  name/type/version) and build the time index.
- `IbaChannel`: channel metadata (name, unit, scale, offset, PDA type) and data as a numpy
  array (bool for digital channels) or a named `pandas.Series`.
- `raw_mode` and `preload` options are passed through to the iba reader.

## License

MIT
