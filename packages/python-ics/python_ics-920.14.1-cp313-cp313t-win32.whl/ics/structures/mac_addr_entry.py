# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class mac_addr_entry(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('mMacId', ctypes.c_uint16),
        ('mMacAddr', ctypes.c_uint8 * 6),
    ]


_MacAddrEntry = mac_addr_entry
MacAddrEntry = mac_addr_entry

