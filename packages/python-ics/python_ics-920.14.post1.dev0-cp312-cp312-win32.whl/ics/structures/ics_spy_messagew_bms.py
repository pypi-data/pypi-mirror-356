# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class Nameless64992(ctypes.Structure):
    _fields_ = [
        ('', ctypes.c_uint32, 8),
        ('PacketType', ctypes.c_uint32, 8),
        ('PacketID', ctypes.c_uint32, 8),
        ('PacketSource', ctypes.c_uint32, 8),
    ]



class Nameless44788(ctypes.Union):
    _anonymous_  = ('Nameless64992',)
    _fields_ = [
        ('ArbIDOrHeader', ctypes.c_uint32),
        ('Nameless64992', Nameless64992),
    ]



class Nameless61357(ctypes.Structure):
    _fields_ = [
        ('APICode', ctypes.c_uint32, 8),
        ('', ctypes.c_uint32, 24),
    ]



class Nameless62381(ctypes.Union):
    _anonymous_  = ('Nameless61357',)
    _fields_ = [
        ('StatusBitField3', ctypes.c_uint32),
        ('Nameless61357', Nameless61357),
    ]



class Nameless5941(ctypes.Structure):
    _anonymous_  = ('Nameless62381',)
    _fields_ = [
        ('Nameless62381', Nameless62381),
        ('StatusBitField4', ctypes.c_uint32),
    ]



class Nameless61713(ctypes.Union):
    _anonymous_  = ('Nameless5941',)
    _fields_ = [
        ('Nameless5941', Nameless5941),
        ('AckBytes', ctypes.c_uint8 * 8),
    ]



class ics_spy_messagew_bms(ctypes.Structure):
    _anonymous_  = ('Nameless44788', 'Nameless61713')
    _fields_ = [
        ('StatusBitField', ctypes.c_uint32),
        ('StatusBitField2', ctypes.c_uint32),
        ('TimeHardware', ctypes.c_uint32),
        ('TimeHardware2', ctypes.c_uint32),
        ('TimeSystem', ctypes.c_uint32),
        ('TimeSystem2', ctypes.c_uint32),
        ('TimeStampHardwareID', ctypes.c_uint8),
        ('TimeStampSystemID', ctypes.c_uint8),
        ('NetworkID', ctypes.c_uint8),
        ('NodeID', ctypes.c_uint8),
        ('Protocol', ctypes.c_uint8),
        ('MessagePieceID', ctypes.c_uint8),
        ('ExtraDataPtrEnabled', ctypes.c_uint8),
        ('NumberBytesHeader', ctypes.c_uint8),
        ('NumberBytesData', ctypes.c_uint8),
        ('NetworkID2', ctypes.c_uint8),
        ('DescriptionID', ctypes.c_uint16),
        ('Nameless44788', Nameless44788),
        ('Data', ctypes.c_uint8 * 8),
        ('Nameless61713', Nameless61713),
        ('ExtraDataPtr', ctypes.c_void_p),
        ('MiscData', ctypes.c_uint8),
        ('Reserved', ctypes.c_uint8 * 3),
    ]


_icsSpyMessagewBMS = ics_spy_messagew_bms
icsSpyMessagewBMS = ics_spy_messagew_bms

