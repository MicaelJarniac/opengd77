"""CSV Models."""

from __future__ import annotations

__all__: list[str] = [
    "APRSCSV",
    "DTMFCSV",
    "BandwidthCSV",
    "BaudRateCSV",
    "CallTypeCSV",
    "ChannelCSV",
    "ChannelTypeCSV",
    "ColorCodeCSV",
    "ContactCSV",
    "IconTableCSV",
    "OnOffCSV",
    "PowerCSV",
    "TGListCSV",
    "TalkerAliasCSV",
    "TimeslotCSV",
    "TrueFalseCSV",
    "YesNoCSV",
    "ZoneCSV",
]

from decimal import Decimal
from typing import Literal, TypeAlias, TypedDict

from typing_extensions import NotRequired

ChannelTypeCSV: TypeAlias = Literal["Analogue", "Digital"]
BandwidthCSV: TypeAlias = Literal["12.5", "25.0"]
ColorCodeCSV: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
TimeslotCSV: TypeAlias = Literal[1, 2]
TalkerAliasCSV: TypeAlias = Literal["Off", "APRS", "Text", "APRS+Text"]
YesNoCSV: TypeAlias = Literal["Yes", "No"]
OnOffCSV: TypeAlias = Literal["On", "Off"]
TrueFalseCSV: TypeAlias = Literal["True", "False"]
IconTableCSV: TypeAlias = Literal[0, 1]
PositionMaskingCSV: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7]
BaudRateCSV: TypeAlias = Literal[0, 1]
CallTypeCSV: TypeAlias = Literal["Group", "Private", "AllCall"]
PowerCSV: TypeAlias = Literal[
    "Master", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "+W-"
]
DisabledCSV: TypeAlias = Literal["Disabled"]


APRSCSV = TypedDict(
    "APRSCSV",
    {
        "APRS config Name": str,
        "SSID": int,
        "Via1": str,
        "Via1 SSID": int,
        "Via2": str,
        "Via2 SSID": int,
        "Icon table": IconTableCSV,
        "Icon": int,
        "Comment text": str,
        "Ambiguity": PositionMaskingCSV,
        "Use position": TrueFalseCSV,
        "Latitude": Decimal,
        "Longitude": Decimal,
        "TX Frequency": NotRequired[Decimal],
        "Transmit QSY": TrueFalseCSV,
        "Baud rate setting": BaudRateCSV,
    },
)


ChannelCSV = TypedDict(
    "ChannelCSV",
    {
        "Channel Number": int,
        "Channel Name": str,
        "Channel Type": ChannelTypeCSV,
        "Rx Frequency": Decimal,
        "Tx Frequency": Decimal,
        "Bandwidth (kHz)": NotRequired[BandwidthCSV],
        "Colour Code": NotRequired[ColorCodeCSV],
        "Timeslot": NotRequired[TimeslotCSV],
        "Contact": NotRequired[str],
        "TG List": NotRequired[str],
        "DMR ID": NotRequired[str],
        "TS1_TA_Tx": NotRequired[TalkerAliasCSV],
        "TS2_TA_Tx": NotRequired[TalkerAliasCSV],
        "RX Tone": NotRequired[str],
        "TX Tone": NotRequired[str],
        "Squelch": NotRequired[str],
        "Power": PowerCSV,
        "Rx Only": YesNoCSV,
        "Zone Skip": YesNoCSV,
        "All Skip": YesNoCSV,
        "TOT": int,
        "VOX": OnOffCSV,
        "No Beep": YesNoCSV,
        "No Eco": YesNoCSV,
        "APRS": str,
        "Latitude": Decimal,
        "Longitude": Decimal,
        "Use location": YesNoCSV,
    },
)


ContactCSV = TypedDict(
    "ContactCSV",
    {
        "Contact Name": str,
        "ID": int,
        "ID Type": CallTypeCSV,
        "TS Override": TimeslotCSV | DisabledCSV,
    },
)


DTMFCSV = TypedDict(
    "DTMFCSV",
    {
        "Contact Name": str,
        "Code": str,
    },
)


TGListCSV = TypedDict(
    "TGListCSV",
    {
        "TG List Name": str,
    },
)


ZoneCSV = TypedDict(
    "ZoneCSV",
    {
        "Zone Name": str,
    },
)
