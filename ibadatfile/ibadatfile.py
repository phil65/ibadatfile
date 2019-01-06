# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import datetime

import numpy as np
import pandas as pd
import pythoncom
from win32com.client import VARIANT
from win32com.client.dynamic import Dispatch


A = 0
B = 0
V = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_VARIANT, 2)


class IbaDatFile(object):
    """
    Class representing an Iba .dat file
    """

    def __init__(self, path=None, raw_mode=False, preload=True):
        """
        initialize the dat file object
        """
        self.path = path
        self.reader = Dispatch("IbaFilesLite.IbaFile")
        self.reader.PreLoad = int(preload)
        self.reader.RawMode = int(raw_mode)

    def __enter__(self):
        """
        magic method for context manager
        """
        self.reader.Open(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        magic method for context manager
        """
        self.reader.Close()

    def __iter__(self):
        """
        iterator interface, returns next channel
        """
        enumerator = self.reader.EnumChannels()
        while not enumerator.IsAtEnd():
            channel = enumerator.Next()
            yield IbaChannel(channel)

    def open(self, path):
        """
        opens .dat file from *path
        """
        self.reader.Open(path)
        self.path = path
        return self

    def close(self):
        """
        closes reader
        """
        self.reader.Close()

    def index(self):
        """
        returns the time index for the channels
        """
        start = self.starttime()
        frames = self.frames()
        clk = self.clk()
        return pd.DatetimeIndex([start + datetime.timedelta(seconds=i * clk) for i in range(frames)],
                                name="time")

    def frames(self):
        """
        returns amount of frames of channels
        """
        return int(self.reader.QueryInfoByName("frames"))

    def signal_count(self):
        """
        returns amount of channels
        """
        return int(self.reader.QueryInfoByName("totalSignalCount"))

    def clk(self):
        """
        returns the clock rate
        """
        return float(self.reader.QueryInfoByName("clk"))

    def recorder_version(self):
        """
        returns the software version of the recorder
        """
        return self.reader.QueryInfoByName("version")

    def recorder_name(self):
        """
        returns the software version of the recorder
        """
        return self.reader.QueryInfoByName("name")

    def recorder_type(self):
        """
        returns the software version of the recorder
        """
        return self.reader.QueryInfoByName("type")

    def starttime(self):
        """
        returns the recording start time as datetime object
        """
        return pd.datetime.strptime(self.reader.QueryInfoByName("starttime"),
                                    '%d.%m.%Y %H:%M:%S.%f')

    def starttime_as_str(self):
        """
        returns the recording start time as datetime object
        """
        return self.reader.QueryInfoByName("starttime")

    def return_channel_names(self):
        return [channel.name() for channel in self]

    def data(self):
        """
        returns data as a dataframe
        """
        data = {channel.name(): channel.data() for channel in self}
        df = pd.DataFrame.from_dict(data)
        df.index = self.index()
        return df


class IbaChannel(object):
    """
    Class representing a single channel of an iba .dat file
    """

    def __init__(self, channel):
        """
        initialize the channel object
        """
        self.channel = channel

    def name(self):
        """
        returns the channel name
        """
        return self.channel.QueryInfoByName("name")

    def minscale(self):
        """
        returns the channel minscale
        """
        return self.channel.QueryInfoByName("minscale")

    def maxscale(self):
        """
        returns the channel maxscale
        """
        return self.channel.QueryInfoByName("maxscale")

    def xoffset(self):
        """
        returns the channel x offset (in frames?)
        """
        return self.channel.QueryInfoByName("xoffset")

    def unit(self):
        """
        returns unit of the channel data
        """
        return self.channel.QueryInfoByName("unit")

    def digchannel(self):
        """
        returns digchannel info
        """
        return self.channel.QueryInfoByName("digchannel")

    def pda_type(self):
        """
        returns the channel unit
        """
        return self.channel.QueryInfoByName("$PDA_Typ")

    def data(self):
        """
        returns the channel data
        """
        if self.channel.IsDefaultTimebased():
            data = np.array(self.channel.QueryTimebasedData(A, B, V)[2])
        else:
            data = np.array(self.channel.QueryLengthbasedData(A, B, V)[2])
        if self.is_bool():
            return data.astype(bool)
        elif self.pda_type() == "int16":
            return data.astype("int16")
        else:
            return data

    def is_bool(self):
        """
        returns true if series contains boolean values
        """
        return self.channel.IsDigital()

    def is_time_based(self):
        """
        returns bool whether series is time based
        """
        return self.channel.IsDefaultTimebased()

    def id(self):
        """
        returns the channel id
        """
        return self.channel.QueryChannelId()
