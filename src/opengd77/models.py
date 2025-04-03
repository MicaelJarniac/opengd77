"""Models."""

from __future__ import annotations

__all__: list[str] = [
    "APRS",
    "DTMF",
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
    "Timeslot",
    "Zone",
]

from collections.abc import Sequence  # noqa: TC003
from datetime import timedelta
from decimal import Decimal
from enum import Enum, Flag, auto
from string import digits
from typing import Literal, TypeAlias

from attrs import Attribute, define, field
from attrs.validators import and_, ge, in_, le, max_len, not_, optional

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
    P1 = auto()
    """50mW | 50mW | 100mW"""
    P2 = auto()
    """250mW | 250mW | 250mW"""
    P3 = auto()
    """500mW | 500mW | 500mW"""
    P4 = auto()
    """750mW | 750mW | 750mW"""
    P5 = auto()
    """1W | 1W | 1W"""
    P6 = auto()
    """2W | 2W | 5W"""
    P7 = auto()
    """3W | 3W | 10W"""
    P8 = auto()
    """4W | 5W | 25W"""
    P9 = auto()
    """5W | 10W | 40W"""
    PLUS_W_MINUS = auto()
    """+W-"""


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
Timeslot: TypeAlias = Literal[1, 2]


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
    transmit_qsy: bool = field(default=False)
    beacon_silently: bool = False
    baud_rate: BaudRate = BaudRate.BAUD_1200

    @transmit_qsy.validator
    def validate_transmit_qsy(self, attribute: Attribute[bool], value: bool) -> None:  # noqa: FBT001
        """Validate transmit QSY."""
        if value and self.tx_frequency is None:
            msg = f"{attribute.name} requires tx_frequency to be set"
            raise ValueError(msg)


@define(kw_only=True)
class Contact:
    """Contact."""

    name: str = field(validator=and_(max_len(Max.CHARS_CONTACT_NAME), nn))
    call_id: int = field(validator=[ge(0), le(99999999)])
    call_type: CallType = CallType.PRIVATE
    channel_ts_override: Timeslot | None = None


@define(kw_only=True)
class DTMF:
    """DTMF Contact."""

    name: str = field(validator=and_(max_len(Max.CHARS_DTMF_NAME), nn))
    """Name."""
    code: str = field(validator=and_(max_len(Max.CHARS_DTMF_CODE), nn))
    """DTMF code.

    May only contain digits and `ABCD*#`.
    """

    @code.validator
    def check_number(self, attribute: Attribute[str], value: str) -> None:
        """Check DTMF code.

        May only contain digits and `ABCD*#`.
        """
        if any(c not in f"{digits}ABCD*#" for c in value):
            msg = f"{attribute.name} may only contain digits and `ABCD*#`"
            raise ValueError(msg)


@define(kw_only=True)
class TGList:
    """Talk group list."""

    name: str = field(validator=and_(max_len(Max.CHARS_TG_LIST_NAME), nn))
    contacts: Sequence[Contact] = field(
        factory=list, validator=max_len(Max.TGS_PER_LIST)
    )

    @contacts.validator
    def check_contacts(
        self, attribute: Attribute[list[Contact]], value: list[Contact]
    ) -> None:
        """Check contacts."""
        if len(value) != len({c.name for c in value}):
            msg = f"{attribute.name} may not contain duplicate contacts"
            raise ValueError(msg)


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
    timeout: timedelta | None = field(default=None)
    """Transmit timeout.

    Must be between 15s and 495s, in steps of 15s.
    """
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

    @timeout.validator
    def check_timeout(
        self, attribute: Attribute[timedelta | None], value: timedelta | None
    ) -> None:
        """Must be between 15s and 495s, in steps of 15s."""
        if value is not None and (
            value.total_seconds() % 15 != 0
            or value < timedelta(seconds=15)
            or value > timedelta(seconds=495)
        ):
            msg = f"{attribute.name} must be between 15s and 495s, in steps of 15s"
            raise ValueError(msg)


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
        default=None, validator=optional(and_(ge(Decimal(0)), le(Decimal(1))))
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
    repeater_timeslot: Timeslot = 1
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
    channels: Sequence[Channel] = field(
        factory=list, validator=max_len(Max.CHANNELS_PER_ZONE)
    )
    """Channels."""

    @channels.validator
    def check_channels(
        self, attribute: Attribute[list[Channel]], value: list[Channel]
    ) -> None:
        """Check channels."""
        if len(value) != len({c.name for c in value}):
            msg = f"{attribute.name} may not contain duplicate channels"
            raise ValueError(msg)


@define(kw_only=True)
class Codeplug:
    """Codeplug."""

    aprs: Sequence[APRS] = field(factory=list)
    """APRS settings."""
    contacts: Sequence[Contact] = field(factory=list, validator=max_len(Max.CONTACTS))
    """Contacts."""
    dtmf: Sequence[DTMF] = field(factory=list, validator=max_len(Max.DTMF))
    """DTMF contacts."""
    tg_lists: Sequence[TGList] = field(factory=list, validator=max_len(Max.TG_LISTS))
    """Talk group lists."""
    zones: Sequence[Zone] = field(factory=list, validator=max_len(Max.ZONES))
    """Zones."""
    channels: Sequence[Channel] = field(factory=list, validator=max_len(Max.CHANNELS))
    """Channels."""
