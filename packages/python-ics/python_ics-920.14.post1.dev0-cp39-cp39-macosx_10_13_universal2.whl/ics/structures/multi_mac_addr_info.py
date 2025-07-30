# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum

from ics.structures.mac_addr_entry import *


class multi_mac_addr_info(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('mAddrCnt', ctypes.c_uint16),
        ('mMacEntries', MacAddrEntry * 32),
    ]


_MultiMacAddrInfo = multi_mac_addr_info
MultiMacAddrInfo = multi_mac_addr_info

