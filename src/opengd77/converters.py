"""Converters."""

from __future__ import annotations

__all__: list[str] = [
    "BANDWIDTH",
    "BAUD_RATE",
    "CALL_TYPE",
    "ICON_TABLE",
    "ON_OFF",
    "POSITION_MASKING",
    "POWER",
    "TALKER_ALIAS",
    "TRUE_FALSE",
    "YES_NO",
    "aprs_to_dict",
    "channel_to_dict",
    "codeplug_to_csvs",
    "contact_to_dict",
    "dicts_to_csv",
    "dtmf_to_dict",
    "squelch_to_str",
    "tg_list_to_dict",
    "zone_to_dict",
]

import csv
from decimal import Decimal
from typing import TYPE_CHECKING, Final

from attrs import validate

from opengd77.constants import Max
from opengd77.csv_models import (
    APRSCSV,
    DTMFCSV,
    BandwidthCSV,
    BaudRateCSV,
    CallTypeCSV,
    ChannelCSV,
    ContactCSV,
    IconTableCSV,
    OnOffCSV,
    PositionMaskingCSV,
    PowerCSV,
    TalkerAliasCSV,
    TGListCSV,
    TrueFalseCSV,
    YesNoCSV,
    ZoneCSV,
)
from opengd77.models import (
    APRS,
    DTMF,
    AnalogChannel,
    Bandwidth,
    BaudRate,
    CallType,
    Channel,
    Codeplug,
    Contact,
    DigitalChannel,
    IconTable,
    PositionMasking,
    Power,
    TalkerAlias,
    TGList,
    Zone,
)

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Iterable, Mapping, Sequence
    from pathlib import Path

TRUE_FALSE: Final[dict[bool, TrueFalseCSV]] = {
    True: "True",
    False: "False",
}


YES_NO: Final[dict[bool, YesNoCSV]] = {
    True: "Yes",
    False: "No",
}


ON_OFF: Final[dict[bool, OnOffCSV]] = {
    True: "On",
    False: "Off",
}


ICON_TABLE: Final[dict[IconTable, IconTableCSV]] = {
    IconTable.PRIMARY: 0,
    IconTable.ALTERNATE: 1,
}


POSITION_MASKING: Final[dict[PositionMasking | None, PositionMaskingCSV]] = {
    None: 0,
    PositionMasking.DEG_0_0005: 1,
    PositionMasking.DEG_0_0010: 2,
    PositionMasking.DEG_0_0050: 3,
    PositionMasking.DEG_0_0100: 4,
    PositionMasking.DEG_0_0500: 5,
    PositionMasking.DEG_0_1000: 6,
    PositionMasking.DEG_0_5000: 7,
}


BAUD_RATE: Final[dict[BaudRate, BaudRateCSV]] = {
    BaudRate.BAUD_1200: 0,
    BaudRate.BAUD_300: 1,
}


BANDWIDTH: Final[dict[Bandwidth, BandwidthCSV]] = {
    Bandwidth.BW_12_5KHZ: "12.5",
    Bandwidth.BW_25KHZ: "25.0",
}


TALKER_ALIAS: Final[dict[TalkerAlias | None, TalkerAliasCSV]] = {
    None: "Off",
    TalkerAlias.APRS: "APRS",
    TalkerAlias.TEXT: "Text",
    TalkerAlias.APRS | TalkerAlias.TEXT: "APRS+Text",
}


POWER: Final[dict[Power, PowerCSV]] = {
    Power.MASTER: "Master",
    Power.P1: "P1",
    Power.P2: "P2",
    Power.P3: "P3",
    Power.P4: "P4",
    Power.P5: "P5",
    Power.P6: "P6",
    Power.P7: "P7",
    Power.P8: "P8",
    Power.P9: "P9",
    Power.PLUS_W_MINUS: "+W-",
}


CALL_TYPE: Final[dict[CallType, CallTypeCSV]] = {
    CallType.PRIVATE: "Private",
    CallType.GROUP: "Group",
    CallType.ALL: "AllCall",
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


def aprs_to_dict(aprs: APRS) -> APRSCSV:
    """Convert an APRS object to a dictionary."""
    validate(aprs)
    out = APRSCSV(
        {
            "APRS config Name": aprs.name,
            "SSID": aprs.tx_ssid,
            "Via1": aprs.via_1,
            "Via1 SSID": aprs.via_1_ssid,
            "Via2": aprs.via_2,
            "Via2 SSID": aprs.via_2_ssid,
            "Icon table": ICON_TABLE[aprs.icon_table],
            "Icon": aprs.icon,
            "Comment text": aprs.comment,
            "Ambiguity": POSITION_MASKING[aprs.position_masking],
            "Use position": TRUE_FALSE[aprs.use_fixed_position],
            "Latitude": aprs.fixed_latitude,
            "Longitude": aprs.fixed_longitude,
            "Transmit QSY": TRUE_FALSE[aprs.transmit_qsy],
            "Baud rate setting": BAUD_RATE[aprs.baud_rate],
        }
    )
    if aprs.tx_frequency is not None:
        out["TX Frequency"] = aprs.tx_frequency
    return out


def contact_to_dict(contact: Contact) -> ContactCSV:
    """Convert a contact to a dictionary."""
    validate(contact)
    return ContactCSV(
        {
            "Contact Name": contact.name,
            "ID": contact.call_id,
            "ID Type": CALL_TYPE[contact.call_type],
            "TS Override": contact.channel_ts_override or "Disabled",
        }
    )


def dtmf_to_dict(dtmf: DTMF) -> DTMFCSV:
    """Convert a DTMF object to a dictionary."""
    validate(dtmf)
    return DTMFCSV(
        {
            "Contact Name": dtmf.name,
            "Code": dtmf.code,
        }
    )


def tg_list_to_dict(tg_list: TGList) -> TGListCSV:
    """Convert a TGList object to a dictionary."""
    validate(tg_list)
    out = TGListCSV(
        {
            "TG List Name": tg_list.name,
        }
    )
    for i, contact in enumerate(tg_list.contacts):
        out[f"Contact{i + 1}"] = contact.name  # type: ignore[literal-required]
    return out


def channel_to_dict(channel: Channel, /, *, number: int) -> ChannelCSV:
    # sourcery skip: extract-method
    """Convert a channel to a dictionary."""
    validate(channel)
    out = ChannelCSV(
        {
            "Channel Number": number,
            "Channel Name": channel.name,
            "Channel Type": "Analogue"
            if isinstance(channel, AnalogChannel)
            else "Digital",
            "Rx Frequency": channel.rx_frequency,
            "Tx Frequency": channel.tx_frequency,
            "Power": POWER[channel.power],
            "Rx Only": YES_NO[channel.rx_only],
            "Zone Skip": YES_NO[channel.scan_zone_skip],
            "All Skip": YES_NO[channel.scan_all_skip],
            "TOT": int(channel.timeout.total_seconds()) if channel.timeout else 0,
            "VOX": ON_OFF[channel.vox],
            "No Beep": YES_NO[channel.no_beep],
            "No Eco": YES_NO[channel.no_economy],
            "APRS": channel.aprs.name if channel.aprs else "None",
            "Latitude": channel.latitude,
            "Longitude": channel.longitude,
            "Use location": YES_NO[channel.use_location],
        }
    )
    if isinstance(channel, AnalogChannel):
        out["Bandwidth (kHz)"] = BANDWIDTH[channel.bandwidth]
        out["RX Tone"] = channel.rx_tone or "None"
        out["TX Tone"] = channel.tx_tone or "None"
        out["Squelch"] = squelch_to_str(channel.squelch)
    elif isinstance(channel, DigitalChannel):
        out["Colour Code"] = channel.color_code
        out["Timeslot"] = channel.repeater_timeslot
        out["Contact"] = channel.contact.name if channel.contact else "None"
        out["TG List"] = channel.tg_list.name if channel.tg_list else "None"
        out["DMR ID"] = str(channel.override_master_dmr_id or "None")
        out["TS1_TA_Tx"] = TALKER_ALIAS[channel.timeslot_1_talker_alias]
        out["TS2_TA_Tx"] = TALKER_ALIAS[channel.timeslot_2_talker_alias]
    return out


def zone_to_dict(zone: Zone) -> ZoneCSV:
    """Convert a zone to a dictionary."""
    validate(zone)
    out = ZoneCSV(
        {
            "Zone Name": zone.name,
        }
    )
    for i, channel in enumerate(zone.channels):
        out[f"Channel{i + 1}"] = channel.name  # type: ignore[literal-required]
    return out


def dicts_to_csv(
    file: Path,
    data: Iterable[Mapping[str, str | int | Decimal]],
    cols: Sequence[str],
) -> None:
    """Convert a dictionary to a CSV string."""
    with file.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def codeplug_to_csvs(folder: Path, codeplug: Codeplug) -> None:
    """Convert a codeplug to CSV files."""
    folder.mkdir(parents=True, exist_ok=True)

    # APRS
    dicts_to_csv(
        folder / "APRS.csv",
        [aprs_to_dict(aprs) for aprs in codeplug.aprs],  # type: ignore[misc]
        list(APRSCSV.__annotations__.keys()),
    )

    # Contacts
    dicts_to_csv(
        folder / "Contacts.csv",
        [contact_to_dict(contact) for contact in codeplug.contacts],  # type: ignore[misc]
        list(ContactCSV.__annotations__.keys()),
    )

    # DTMF
    dicts_to_csv(
        folder / "DTMF.csv",
        [dtmf_to_dict(dtmf) for dtmf in codeplug.dtmf],  # type: ignore[misc]
        list(DTMFCSV.__annotations__.keys()),
    )

    # TG Lists
    dicts_to_csv(
        folder / "TG_Lists.csv",
        [tg_list_to_dict(tg_list) for tg_list in codeplug.tg_lists],  # type: ignore[misc]
        list(TGListCSV.__annotations__.keys())
        + [f"Contact{i + 1}" for i in range(Max.TGS_PER_LIST)],
    )

    # Zones
    dicts_to_csv(
        folder / "Zones.csv",
        [zone_to_dict(zone) for zone in codeplug.zones],  # type: ignore[misc]
        list(ZoneCSV.__annotations__.keys())
        + [f"Channel{i + 1}" for i in range(Max.CHANNELS_PER_ZONE)],
    )

    # Channels
    dicts_to_csv(
        folder / "Channels.csv",
        [
            channel_to_dict(channel, number=i + 1)  # type: ignore[misc]
            for i, channel in enumerate(codeplug.channels)
        ],
        list(ChannelCSV.__annotations__.keys()),
    )
