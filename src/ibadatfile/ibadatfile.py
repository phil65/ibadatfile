import datetime as dt
import os
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd


if TYPE_CHECKING:
    from collections.abc import Generator

    from numpy.typing import NDArray


A = 0
B = 0


def _variant():
    """Create the by-reference VARIANT used as output argument for data queries."""
    # pywin32 is Windows-only; import lazily so the package stays importable elsewhere.
    import pythoncom
    from win32com import client

    return client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_VARIANT, 2)


def read_ibadat(
    path: str | os.PathLike[str],
    raw_mode: bool = False,
    preload: bool = True,
) -> pd.DataFrame:
    """Read an iba .dat file into a DataFrame.

    Args:
        path: Path to the .dat file.
        raw_mode: Return raw (unscaled) values.
        preload: Let the reader preload the file into memory.

    Returns:
        One column per channel, indexed by a `DatetimeIndex` named "time".
    """
    with IbaDatFile(path, raw_mode, preload) as file:
        return file.data()


class IbaChannel:
    """Class representing a single channel of an iba .dat file."""

    def __init__(self, channel):
        """Initialize the channel object."""
        self.channel = channel

    def name(self) -> str:
        """Return the channel name."""
        return self.channel.QueryInfoByName("name")

    def minscale(self):
        """Return the channel minscale."""
        return self.channel.QueryInfoByName("minscale")

    def maxscale(self):
        """Return the channel maxscale."""
        return self.channel.QueryInfoByName("maxscale")

    def xoffset(self) -> int:
        """Return the channel x offset (in frames?)."""
        return self.channel.QueryInfoByName("xoffset")

    def unit(self) -> str:
        """Return unit of the channel data."""
        return self.channel.QueryInfoByName("unit")

    def digchannel(self):
        """Return digchannel info."""
        return self.channel.QueryInfoByName("digchannel")

    def pda_type(self) -> str:
        """Return the PDA data type of the channel (e.g. "int16")."""
        return self.channel.QueryInfoByName("$PDA_Typ")

    def tbased(self):
        """Return the channel time base ($PDA_Tbase) as float."""
        return float(self.channel.QueryInfoByName("$PDA_Tbase"))

    def data(self) -> NDArray:
        """Return the channel data."""
        if self.channel.IsDefaultTimebased():
            data = np.array(self.channel.QueryTimebasedData(A, B, _variant())[2])
        else:
            data = np.array(self.channel.QueryLengthbasedData(A, B, _variant())[2])
        if self.is_bool():
            return data.astype(bool)
        if self.pda_type() == "int16":
            return data.astype("int16")
        return data

    def series(self) -> pd.Series:
        return pd.Series(self.data(), name=self.name())

    def is_bool(self) -> bool:
        """Return true if series contains boolean values."""
        return self.channel.IsDigital()

    def is_time_based(self) -> bool:
        """Return bool whether series is time based."""
        return self.channel.IsDefaultTimebased()

    def id(self) -> int:
        """Return the channel id."""
        return self.channel.QueryChannelId()


class IbaDatFile:
    """Class representing an Iba .dat file."""

    def __init__(
        self,
        path: str | os.PathLike[str],
        raw_mode: bool = False,
        preload: bool = True,
    ):
        """Initialize the dat file object.

        The file is opened when entering the context manager (or via `open`).

        Args:
            path: Path to the .dat file.
            raw_mode: Return raw (unscaled) values.
            preload: Let the reader preload the file into memory.

        Raises:
            OSError: If the iba COM server (ibaFilesLite.dll) is not registered.
        """
        import pywintypes
        from win32com import client

        self.path = os.fspath(path)
        try:
            self.reader = client.dynamic.Dispatch("IbaFilesLite.IbaFile")
        except pywintypes.com_error as e:
            msg = "Necessary dlls are not installed."
            raise OSError(msg) from e
        self.reader.PreLoad = int(preload)
        self.reader.RawMode = int(raw_mode)

    def __enter__(self):
        """Magic method for context manager."""
        self.reader.Open(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Magic method for context manager."""
        self.reader.Close()

    def __iter__(self) -> Generator[IbaChannel]:
        """Iterator interface, returns next channel."""
        enumerator = self.reader.EnumChannels()
        while not enumerator.IsAtEnd():
            channel = enumerator.Next()
            yield IbaChannel(channel)

    def __getitem__(self, index: str) -> IbaChannel:
        """Return the channel with the given name, raise IndexError if missing."""
        for channel in self:
            if channel.name() == index:
                return channel
        raise IndexError(index)

    def open(self, path: str | os.PathLike[str]):
        """Open the .dat file at *path*."""
        self.path = os.fspath(path)
        self.reader.Open(self.path)
        return self

    def close(self):
        """Close reader."""
        self.reader.Close()

    def index(self) -> pd.DatetimeIndex:
        """Return the time index for the channels."""
        start = self.starttime()
        frames = self.frames()
        clk = self.clk()
        times = [start + dt.timedelta(seconds=i * clk) for i in range(frames)]
        return pd.DatetimeIndex(times, name="time")

    def frames(self) -> int:
        """Return amount of frames of channels."""
        return int(self.reader.QueryInfoByName("frames"))

    def signal_count(self) -> int:
        """Return amount of channels."""
        return int(self.reader.QueryInfoByName("totalSignalCount"))

    def clk(self) -> float:
        """Return the clock rate."""
        return float(self.reader.QueryInfoByName("clk"))

    def recorder_version(self) -> str:
        """Return the software version of the recorder."""
        return self.reader.QueryInfoByName("version")

    def recorder_name(self) -> str:
        """Return the name of the recorder."""
        return self.reader.QueryInfoByName("name")

    def recorder_type(self) -> str:
        """Return the type of the recorder."""
        return self.reader.QueryInfoByName("type")

    def starttime(self) -> dt.datetime:
        """Return the recording start time as datetime object."""
        return dt.datetime.strptime(
            self.reader.QueryInfoByName("starttime"), "%d.%m.%Y %H:%M:%S.%f"
        )

    def starttime_as_str(self) -> str:
        """Return the recording start time as str."""
        return self.reader.QueryInfoByName("starttime")

    def return_channel_names(self) -> list[str]:
        """Return list of channel names."""
        return [channel.name() for channel in self]

    def data(self) -> pd.DataFrame:
        """Return data as a dataframe."""
        data = {channel.name(): channel.data() for channel in self}
        df = pd.DataFrame.from_dict(data)
        df.index = self.index()
        return df
