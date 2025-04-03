"""Constants."""

from __future__ import annotations

__all__: list[str] = [
    "Max",
]

from enum import IntEnum


# https://www.opengd77.com/viewtopic.php?f=12&t=4348#p32632
class Max(IntEnum):
    """Maximums."""

    CONTACTS = 1024
    DTMF = 63
    CHANNELS = 1024
    ZONES = 68
    CHANNELS_PER_ZONE = 80
    TG_LISTS = 76
    TGS_PER_LIST = 32
    CHARS_CHANNEL_NAME = 16
    CHARS_CONTACT_NAME = 16
    CHARS_ZONE_NAME = 16
    CHARS_APRS_NAME = 8
    CHARS_TG_LIST_NAME = 15
    CHARS_DTMF_NAME = 15
    CHARS_DTMF_CODE = 16
    CHARS_APRS_VIA = 6
