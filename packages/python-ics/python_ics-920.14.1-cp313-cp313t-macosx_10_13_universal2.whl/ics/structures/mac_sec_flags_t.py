# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class Nameless46561(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('en', ctypes.c_uint32, 1),
        ('reserved', ctypes.c_uint32, 31),
    ]



class mac_sec_flags_t(ctypes.Union):
    _pack_ = 1
    _anonymous_  = ('Nameless46561',)
    _fields_ = [
        ('Nameless46561', Nameless46561),
        ('flags_32b', ctypes.c_uint32),
    ]


_MACSecFlags = mac_sec_flags_t
MACSecFlags_t = mac_sec_flags_t

