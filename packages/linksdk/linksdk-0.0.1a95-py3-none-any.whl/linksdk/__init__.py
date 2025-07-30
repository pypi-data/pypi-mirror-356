# wiim/__init__.py
"""WiiM Asynchronous Python SDK."""

from .__version__ import __version__
from .wiim_device import WiimDevice
from .controller import WiimController
from .endpoint import WiimApiEndpoint, WiimBaseEndpoint
from .exceptions import (
    WiimException,
    WiimRequestException,
    WiimInvalidDataException,
    WiimDeviceException,
)
from .consts import (
    # Enums likely to be used by consumers of the SDK
    PlayingStatus,
    PlayingMode,
    LoopMode,
    EqualizerMode,
    MuteMode,
    ChannelType,
    SpeakerType,
    AudioOutputHwMode,
    # Attribute Enums if consumers need to parse raw data (less common)
    # DeviceAttribute,
    # PlayerAttribute,
    # MultiroomAttribute,
    # MetaInfo,
    # MetaInfoMetaData,
    # HTTP Commands (usually internal to SDK but can be exposed if advanced use needed)
    # WiimHttpCommand,
)
from .handler import parse_last_change_event # If useful externally

__all__ = [
    "__version__",
    "WiimDevice",
    "WiimController",
    "WiimApiEndpoint",
    "WiimBaseEndpoint",
    "WiimException",
    "WiimRequestException",
    "WiimInvalidDataException",
    "WiimDeviceException",
    "PlayingStatus",
    "PlayingMode",
    "LoopMode",
    "EqualizerMode",
    "MuteMode",
    "ChannelType",
    "SpeakerType",
    "AudioOutputHwMode",
    "parse_last_change_event",
]


