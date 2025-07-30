# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class Nameless1916(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('icsGptpDrvVerMajor', ctypes.c_uint8, 4),
        ('icsGptpDrvVerMinor', ctypes.c_uint8, 4),
    ]



class Nameless63799(ctypes.Union):
    _pack_ = 2
    _anonymous_  = ('Nameless1916',)
    _fields_ = [
        ('icsGptpDrvVerMajorMinor', ctypes.c_uint8),
        ('Nameless1916', Nameless1916),
    ]



class Nameless32745(ctypes.Structure):
    _pack_ = 2
    _fields_ = [
        ('PORT_AE01', ctypes.c_uint32, 1),
        ('PORT_AE02', ctypes.c_uint32, 1),
        ('PORT_AE03', ctypes.c_uint32, 1),
        ('PORT_AE04', ctypes.c_uint32, 1),
        ('PORT_AE05', ctypes.c_uint32, 1),
        ('PORT_AE06', ctypes.c_uint32, 1),
        ('PORT_AE07', ctypes.c_uint32, 1),
        ('PORT_AE08', ctypes.c_uint32, 1),
        ('PORT_AE09', ctypes.c_uint32, 1),
        ('PORT_AE10', ctypes.c_uint32, 1),
        ('PORT_AE11', ctypes.c_uint32, 1),
        ('PORT_AE12', ctypes.c_uint32, 1),
        ('PORT_ETH1', ctypes.c_uint32, 1),
        ('PORT_ETH2', ctypes.c_uint32, 1),
        ('PORT_ETH3', ctypes.c_uint32, 1),
        ('PORT_AE13', ctypes.c_uint32, 1),
        ('PORT_AE14', ctypes.c_uint32, 1),
        ('PORT_AE15', ctypes.c_uint32, 1),
        ('PORT_AE16', ctypes.c_uint32, 1),
    ]



class Nameless8462(ctypes.Union):
    _pack_ = 2
    _anonymous_  = ('Nameless32745',)
    _fields_ = [
        ('multiPortsEnabledForMaster', ctypes.c_uint32),
        ('Nameless32745', Nameless32745),
    ]



class srad_gptp_settings_s(ctypes.Structure):
    _pack_ = 2
    _anonymous_  = ('Nameless63799', 'Nameless8462')
    _fields_ = [
        ('neighborPropDelayThresh', ctypes.c_uint32),
        ('sys_phc_sync_interval', ctypes.c_uint32),
        ('logPDelayReqInterval', ctypes.c_int8),
        ('logSyncInterval', ctypes.c_int8),
        ('logAnnounceInterval', ctypes.c_int8),
        ('profile', ctypes.c_uint8),
        ('priority1', ctypes.c_uint8),
        ('clockclass', ctypes.c_uint8),
        ('clockaccuracy', ctypes.c_uint8),
        ('priority2', ctypes.c_uint8),
        ('offset_scaled_log_variance', ctypes.c_uint16),
        ('gPTPportRole', ctypes.c_uint8),
        ('gptpEnabledPort', ctypes.c_uint8),
        ('enableClockSyntonization', ctypes.c_uint8),
        ('rsvd_1', ctypes.c_uint8),
        ('icsGptpDrvVerHeader', ctypes.c_uint8),
        ('Nameless63799', Nameless63799),
        ('Nameless8462', Nameless8462),
        ('rsvd_2', ctypes.c_uint8 * 8),
    ]


SRAD_GPTP_SETTINGS_s = srad_gptp_settings_s
RAD_GPTP_SETTINGS = srad_gptp_settings_s

