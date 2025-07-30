# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class e_dev_name_type(enum.IntEnum):
    """A ctypes-compatible IntEnum superclass."""
    @classmethod
    def from_param(cls, obj):
        return int(obj)

    EDevNameTypeDefault = 0
    EDevNameTypeNoSerial = enum.auto()
    EDevNameTypeTCP = enum.auto()
    EDevNameTypeTCPShort = enum.auto()


_EDevNameType = e_dev_name_type
EDevNameType = e_dev_name_type

