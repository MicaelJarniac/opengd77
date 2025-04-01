"""Models."""

from __future__ import annotations

__all__: list[str] = [
    "APRS",
    "AnalogChannel",
    "Bandwidth",
    "BaudRate",
    "CallType",
    "Channel",
    "Codeplug",
    "ColorCode",
    "Contact",
    "DigitalChannel",
    "IconTable",
    "PositionMasking",
    "Power",
    "TGList",
    "TalkerAlias",
    "Zone",
]

from datetime import timedelta  # noqa: TC003
from decimal import Decimal
from enum import Enum, Flag, auto
from typing import Literal, TypeAlias

from attrs import Attribute, define, field
from attrs.validators import and_, ge, in_, le, max_len, not_

from opengd77.constants import Max


class Bandwidth(Enum):
    """Channel bandwidth."""

    BW_12_5KHZ = auto()
    """12.5 kHz bandwidth."""
    BW_25KHZ = auto()
    """25 kHz bandwidth."""


class Power(Enum):
    """Channel power."""

    MASTER = auto()
    """Master power."""


class TalkerAlias(Flag):
    """Talker alias."""

    APRS = auto()
    TEXT = auto()


class CallType(Enum):
    """Call type."""

    PRIVATE = auto()
    GROUP = auto()
    ALL = auto()


class IconTable(Enum):
    """Icon table."""

    PRIMARY = auto()
    ALTERNATE = auto()


class PositionMasking(Enum):
    """Position masking."""

    DEG_0_0005 = auto()
    """0.0005 degrees."""
    DEG_0_0010 = auto()
    """0.0010 degrees."""
    DEG_0_0050 = auto()
    """0.0050 degrees."""
    DEG_0_0100 = auto()
    """0.0100 degrees."""
    DEG_0_0500 = auto()
    """0.0500 degrees."""
    DEG_0_1000 = auto()
    """0.1000 degrees."""
    DEG_0_5000 = auto()
    """0.5000 degrees."""


class BaudRate(Enum):
    """Baud rate."""

    BAUD_1200 = auto()
    """1200 baud (VHF/UHF)."""
    BAUD_300 = auto()
    """300 baud (HF)."""


ColorCode: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


nn = not_(in_({"None"}))


@define(kw_only=True)
class APRS:
    """APRS."""

    name: str = field(validator=and_(max_len(Max.CHARS_APRS_NAME), nn))
    tx_ssid: int = field(default=7, validator=[ge(0), le(15)])
    via_1: str = field(default="WIDE1", validator=max_len(Max.CHARS_APRS_VIA))
    via_1_ssid: int = field(validator=[ge(0), le(15)])
    via_2: str = field(default="WIDE2", validator=max_len(Max.CHARS_APRS_VIA))
    via_2_ssid: int = field(validator=[ge(0), le(15)])
    icon_table: IconTable = IconTable.PRIMARY
    icon: int = 15
    comment: str = ""
    position_masking: PositionMasking | None = None
    use_fixed_position: bool = False
    fixed_latitude: Decimal = Decimal(0)
    fixed_longitude: Decimal = Decimal(0)
    tx_frequency: Decimal | None = None
    transmit_qsy: bool = False
    beacon_silently: bool = False
    baud_rate: BaudRate = BaudRate.BAUD_1200


@define(kw_only=True)
class Contact:
    """Contact."""

    name: str = field(validator=and_(max_len(Max.CHARS_CONTACT_NAME), nn))
    call_id: int = field(validator=[ge(0), le(99999999)])
    call_type: CallType = CallType.PRIVATE
    channel_ts_override: Literal[1, 2] | None = None


@define(kw_only=True)
class TGList:
    """Talk group list."""

    name: str = field(validator=and_(max_len(Max.CHARS_TG_LIST_NAME), nn))
    contacts: list[Contact] = field(factory=list, validator=max_len(Max.TGS_PER_LIST))


@define(kw_only=True)
class Channel:
    """Channel."""

    name: str = field(validator=and_(max_len(Max.CHARS_CHANNEL_NAME), nn))
    """Name."""
    rx_frequency: Decimal = field(validator=ge(Decimal(0)))
    """Receive frequency (MHz)."""
    tx_frequency: Decimal = field(validator=ge(Decimal(0)))
    """Transmit frequency (MHz)."""
    power: Power = Power.MASTER
    """Transmit power."""
    rx_only: bool = False
    """Receive only."""
    scan_zone_skip: bool = False
    """Skip on zone scan."""
    scan_all_skip: bool = False
    """Skip on all scan."""
    timeout: timedelta | None = None
    """Transmit timeout."""
    vox: bool = False
    """Voice operated transmit."""
    no_beep: bool = False
    no_economy: bool = False
    """No economy mode."""
    aprs: APRS | None = None
    """APRS settings."""
    latitude: Decimal = Decimal(0)
    """Latitude."""
    longitude: Decimal = Decimal(0)
    """Longitude."""
    use_location: bool = False
    """Use location."""


@define(kw_only=True)
class AnalogChannel(Channel):
    """Analog channel."""

    bandwidth: Bandwidth = Bandwidth.BW_12_5KHZ
    """Bandwidth."""
    # If APRS without set freq, no TX tone allowed.
    tx_tone: str | None = None
    """Transmit tone."""
    rx_tone: str | None = None
    """Receive tone."""
    squelch: Decimal | None = field(
        default=None, validator=and_(ge(Decimal(0)), le(Decimal(1)))
    )
    """Squelch level. 0.00 to 1.00, 0.05 increments."""

    @squelch.validator
    def check_squelch(self, attribute: Attribute[Decimal], value: Decimal) -> None:
        """Check squelch value."""
        if value is not None and value % Decimal("0.05") != 0:
            msg = f"{attribute.name} must be a multiple of 0.05"
            raise ValueError(msg)


@define(kw_only=True)
class DigitalChannel(Channel):
    """Digital channel."""

    tg_list: TGList | None = None
    """Talk group list."""
    color_code: ColorCode = 0
    """Color code."""
    contact: Contact | None = None
    """Contact."""
    repeater_timeslot: Literal[1, 2] = 1
    """Repeater timeslot. 1 or 2."""
    timeslot_1_talker_alias: TalkerAlias | None = None
    """Talker alias for timeslot 1."""
    timeslot_2_talker_alias: TalkerAlias | None = None
    """Talker alias for timeslot 2."""
    override_master_dmr_id: int | None = None
    """Override master DMR ID."""
    force_dmo: bool = False
    """Force DMO mode."""


@define(kw_only=True)
class Zone:
    """Zone."""

    name: str = field(validator=and_(max_len(Max.CHARS_ZONE_NAME), nn))
    """Name."""
    channels: list[Channel] = field(
        factory=list, validator=max_len(Max.CHANNELS_PER_ZONE)
    )
    """Channels."""


@define(kw_only=True)
class Codeplug:
    """Codeplug."""

    aprs: list[APRS] = field(factory=list)
    """APRS settings."""
    contacts: list[Contact] = field(factory=list, validator=max_len(Max.CONTACTS))
    """Contacts."""
    tg_lists: list[TGList] = field(factory=list, validator=max_len(Max.TG_LISTS))
    """Talk group lists."""
    zones: list[Zone] = field(factory=list, validator=max_len(Max.ZONES))
    """Zones."""
    channels: list[Channel] = field(factory=list, validator=max_len(Max.CHANNELS))
    """Channels."""
