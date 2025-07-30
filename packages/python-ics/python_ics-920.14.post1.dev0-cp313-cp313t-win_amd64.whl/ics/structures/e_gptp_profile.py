# This file was auto generated; Do not modify, if you value your sanity!
import ctypes
import enum



class e_gptp_profile(enum.IntEnum):
    """A ctypes-compatible IntEnum superclass."""
    @classmethod
    def from_param(cls, obj):
        return int(obj)

    eGPTP_PROFILE_STANDARD  = 0
    eGPTP_PROFILE_AUTOMOTIVE  = 1


eGPTPProfile = e_gptp_profile

