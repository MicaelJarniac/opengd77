"""Converters."""

from __future__ import annotations

__all__: list[str] = [
    "BANDWIDTH",
    "ON_OFF",
    "YES_NO",
    "channel_to_dict",
    "squelch_to_str",
]

from decimal import Decimal
from typing import Final

from attrs import validate

from opengd77.csv_models import BandwidthCSV, ChannelCSV, OnOffCSV, YesNoCSV
from opengd77.models import AnalogChannel, Bandwidth, Channel, DigitalChannel

YES_NO: Final[dict[bool, YesNoCSV]] = {
    True: "Yes",
    False: "No",
}


ON_OFF: Final[dict[bool, OnOffCSV]] = {
    True: "On",
    False: "Off",
}


BANDWIDTH: dict[Bandwidth, BandwidthCSV] = {
    Bandwidth.BW_12_5KHZ: "12.5",
    Bandwidth.BW_25KHZ: "25.0",
}


def squelch_to_str(squelch: Decimal | None) -> str:
    # sourcery skip: assign-if-exp, reintroduce-else
    """Convert squelch value to string."""
    if squelch is None:
        return "Disabled"
    if squelch == Decimal("0.00"):
        return "Open"
    if squelch == Decimal("1.00"):
        return "Closed"
    return f"{squelch * 100:.0f}%"


def channel_to_dict(c: Channel, /, *, number: int) -> ChannelCSV:
    """Convert a channel to a dictionary."""
    validate(c)
    out = ChannelCSV(
        {
            "Channel Number": number,
            "Channel Name": c.name,
            "Channel Type": "Analogue" if isinstance(c, AnalogChannel) else "Digital",
            "Rx Frequency": c.rx_frequency,
            "Tx Frequency": c.tx_frequency,
            "Power": "Master",
            "Rx Only": YES_NO[c.rx_only],
            "Zone Skip": YES_NO[c.scan_zone_skip],
            "All Skip": YES_NO[c.scan_all_skip],
            "TOT": int(c.timeout.total_seconds()) if c.timeout else 60,
            "VOX": ON_OFF[c.vox],
            "No Beep": YES_NO[c.no_beep],
            "No Eco": YES_NO[c.no_economy],
            "APRS": c.aprs.name if c.aprs else "None",
            "Latitude": c.latitude,
            "Longitude": c.longitude,
            "Use location": YES_NO[c.use_location],
        }
    )
    if isinstance(c, AnalogChannel):
        out["Bandwidth (kHz)"] = BANDWIDTH[c.bandwidth]
        out["RX Tone"] = c.rx_tone or "None"
        out["TX Tone"] = c.tx_tone or "None"
        out["Squelch"] = squelch_to_str(c.squelch)
    elif isinstance(c, DigitalChannel):
        out["Colour Code"] = c.color_code
        out["Timeslot"] = c.repeater_timeslot
        out["Contact"] = c.contact.name if c.contact else "None"
        out["TG List"] = c.tg_list.name if c.tg_list else "None"
        out["DMR ID"] = str(c.override_master_dmr_id or "None")
    return out
