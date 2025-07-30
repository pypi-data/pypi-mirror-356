import logging
from enum import IntFlag, StrEnum, unique

# SDK_LOGGER should be distinct from HA's logger if SDK is standalone
SDK_LOGGER = logging.getLogger("wiim.sdk") # Changed logger name

API_ENDPOINT: str = "{}/httpapi.asp?command={}" # For WiimApiEndpoint
API_TIMEOUT: int = 10 # Increased default timeout slightly
UNKNOWN_TRACK_PLAYING: str = "Unknown"

# Standard UPnP Device Type for Media Renderers
UPNP_DEVICE_TYPE = "urn:schemas-upnp-org:device:MediaRenderer:1"

# Standard UPnP Service IDs
UPNP_AV_TRANSPORT_SERVICE_ID = "urn:schemas-upnp-org:service:AVTransport:1"
UPNP_RENDERING_CONTROL_SERVICE_ID = "urn:schemas-upnp-org:service:RenderingControl:1"
# Custom WiiM UPnP Service ID (as specified by user)
UPNP_WIIM_PLAY_QUEUE_SERVICE_ID = "urn:schemas-wiimu-com:service:PlayQueue:1"
UPNP_TIMEOUT_TIME = 1800
AUDIO_AUX_MODE_IDS = ("FF98F359", "FF98FC04")

# Renamed from LinkPlayCommand to WiimHttpCommand
class WiimHttpCommand(StrEnum):
    """Defines the WiiM HTTP API commands."""
    DEVICE_STATUS = "getStatusEx"
    POSITION_INFO = "GetPositionInfo"
    MEDIA_INFO = "GetInfoEx"
    REBOOT = "StartRebootTime:1"
    PLAYER_STATUS = "getPlayerStatusEx"
    SWITCH_MODE = "setPlayerCmd:switchmode:{}" # Takes mode string e.g. "line-in"
    MULTIROOM_LIST = "multiroom:getSlaveList"
    MULTIROOM_UNGROUP = "multiroom:Ungroup"
    MULTIROOM_LEAVEGROUP = "multiroom:LeaveGroup"
    MULTIROOM_KICK = "multiroom:SlaveKickout:{}" # Takes follower's IP/eth
    MULTIROOM_JOIN = "multiroom:JoinGroup:IP={}:uuid={}" # Executed on follower
    PLAY_PRESET = "MCUKeyShortClick:{}" # Takes preset number 1-based
    TIMESYNC = "timeSync:{}" # Takes YYYYMMDDHHMMSS
    AUDIO_OUTPUT_HW_MODE_SET = "setAudioOutputHardwareMode:{}" # Keep if used
    AUDIO_OUTPUT_HW_MODE = "getNewAudioOutputHardwareMode" # Keep if used

# Enums (largely unchanged, ensure they match API responses)
class SpeakerType(StrEnum):
    MAIN_SPEAKER = "0"
    SUB_SPEAKER = "1"

class ChannelType(StrEnum):
    STEREO = "0"
    LEFT_CHANNEL = "1"
    RIGHT_CHANNEL = "2"

class LoopMode(IntFlag):
    # Values from getPlayerStatusEx 'loop' field
    NONE_MODE_ERROR =            -1 # Repeat one song
    SHUFFLE_DISABLE_REPEAT_ALL =  0
    SHUFFLE_DISABLE_REPEAT_ONE =  1
    SHUFFLE_ENABLE_REPEAT_ALL =   2
    SHUFFLE_ENABLE_REPEAT_NONE =  3
    SHUFFLE_DISABLE_REPEAT_NONE = 4
    SHUFFLE_ENABLE_REPEAT_ONE =   5

class EqualizerMode(StrEnum):
    NONE = "None" # Or "off"
    # General EQ modes (may or may not be supported by WiiM HTTP API directly for setPlayerCmd:equalizer)
    CLASSIC = "Classic"
    POP = "Pop"
    JAZZ = "Jazz"
    VOCAL = "Vocal"
    # WiiM specific EQ modes for WIIM_EQ_LOAD command
    FLAT = "Flat"
    ACOUSTIC = "Acoustic"
    BASS_BOOSTER = "Bass Booster"
    BASS_REDUCER = "Bass Reducer"
    CLASSICAL = "Classical" # Note: different from "Classic"
    DANCE = "Dance"
    DEEP = "Deep"
    ELECTRONIC = "Electronic"
    HIP_HOP = "Hip-Hop"
    LATIN = "Latin"
    LOUDNESS = "Loudness"
    LOUNGE = "Lounge"
    PIANO = "Piano"
    R_B = "R&B" # Ensure no special chars if used as command param
    ROCK = "Rock"
    SMALL_SPEAKERS = "Small Speakers"
    SPOKEN_WORD = "Spoken Word"
    TREBLE_BOOSTER = "Treble Booster"
    TREBLE_REDUCER = "Treble Reducer"
    VOCAL_BOOSTER = "Vocal Booster"

class PlayingStatus(StrEnum):
    # Values from getPlayerStatusEx 'status' field
    PLAYING = "PLAYING"
    LOADING = "TRANSITIONING" # Buffering/transitioning
    STOPPED = "STOPPED" # Or "idle"
    PAUSED = "PAUSED_PLAYBACK"
    UNKNOWN = "NO_MEDIA_PRESENT"

class PlayerStatus(StrEnum):
    # Values from getPlayerStatusEx 'status' field
    PLAYING = "play"
    LOADING = "load"
    STOPPED = "stop"
    PAUSED = "pause"

_PLAYER_TO_PLAYING: dict[PlayerStatus, PlayingStatus] = {
    PlayerStatus.PLAYING: PlayingStatus.PLAYING,
    PlayerStatus.LOADING: PlayingStatus.LOADING,
    PlayerStatus.STOPPED: PlayingStatus.STOPPED,
    PlayerStatus.PAUSED: PlayingStatus.PAUSED,
}

class MuteMode(StrEnum):
    # Values from getPlayerStatusEx 'mute' field
    UNMUTED = "0"
    MUTED = "1"

# Player attributes from getPlayerStatusEx JSON response
class PlayerAttribute(StrEnum):
    SPEAKER_TYPE = "type" # 0 for main, 1 for sub
    CHANNEL_TYPE = "ch" # 0 for stereo, 1 for L, 2 for R
    PLAYBACK_MODE = "mode" # Current PlayingMode (e.g. "40" for line-in)
    PLAYLIST_MODE = "loop" # Current LoopMode (e.g. "1" for repeat all)
    EQUALIZER_MODE = "eq" # Current EQ setting (e.g. "0" for none, or name for WiiM)
    PLAYING_STATUS = "status" # "play", "pause", "stop", "load"
    CURRENT_POSITION = "curpos" # Milliseconds
    OFFSET_POSITION = "offset_pts" # Keep if used
    TOTAL_LENGTH = "totlen" # Milliseconds
    TITLE = "Title" # Uppercase T
    ARTIST = "Artist" # Uppercase A
    ALBUM = "Album" # Uppercase A
    # ALARM_FLAG = "alarmflag" # Keep if used
    # PLAYLIST_COUNT = "plicount" # Keep if used
    # PLAYLIST_INDEX = "plicurr" # Keep if used
    VOLUME = "vol" # 0-100
    MUTED = "mute" # "0" or "1"
    # Add any other relevant fields from API 1.03 getPlayerStatusEx

# Device attributes from getStatusEx JSON response
class DeviceAttribute(StrEnum):
    UUID = "uuid" # Primary identifier
    DEVICE_NAME = "DeviceName"
    # GROUP_NAME = "GroupName" # Keep if used
    SSID = "ssid"
    LANGUAGE = "language"
    FIRMWARE = "firmware"
    HARDWARE = "hardware"
    BUILD = "build"
    PROJECT = "project" # Used for manufacturer/model mapping
    # PRIV_PRJ = "priv_prj"
    # PROJECT_BUILD_NAME = "project_build_name"
    RELEASE = "Release" # Often same as firmware
    # TEMP_UUID = "temp_uuid"
    # HIDE_SSID = "hideSSID"
    # SSID_STRATEGY = "SSIDStrategy"
    # BRANCH = "branch"
    # GROUP = "group" # Multiroom group ID?
    # WMRM_VERSION = "wmrm_version"
    INTERNET = "internet" # "1" if connected
    MAC_ADDRESS = "MAC" # Primary MAC
    STA_MAC_ADDRESS = "STA_MAC" # Wi-Fi client MAC
    # COUNTRY_CODE = "CountryCode"
    # COUNTRY_REGION = "CountryRegion"
    NET_STAT = "netstat" # Network status code
    # ESSID = "essid" # Connected Wi-Fi SSID
    APCLI0 = "apcli0" # IP address on Wi-Fi client interface
    ETH0 = "eth0" # IP address on Ethernet interface (if present)
    # ETH2 = "eth2" # Another ethernet interface?
    # RA0 = "ra0" # Wi-Fi AP interface IP?
    # ETH_DHCP = "eth_dhcp"
    # VERSION_UPDATE = "VersionUpdate" # Update status
    NEW_VER = "NewVer" # Available new firmware version
    # SET_DNS_ENABLE = "set_dns_enable"
    MCU_VER = "mcu_ver"
    # MCU_VER_NEW = "mcu_ver_new"
    # DSP_VER = "dsp_ver"
    # DSP_VER_NEW = "dsp_ver_new"
    # DATE = "date"
    # TIME = "time"
    # TIMEZONE = "tz"
    # DST_ENABLE = "dst_enable"
    # REGION = "region"
    # PROMPT_STATUS = "prompt_status"
    # IOT_VER = "iot_ver"
    UPNP_VERSION = "upnp_version" # UPnP stack version?
    # CAP1 = "cap1"
    # CAPABILITY = "capability"
    # LANGUAGES = "languages"
    # STREAMS_ALL = "streams_all"
    # STREAMS = "streams"
    # EXTERNAL = "external"
    PLAYMODE_SUPPORT = "plm_support" # Bitmask of supported InputModes
    PRESET_KEY = "preset_key" # Number of supported presets (e.g., "10")
    SPOTIFY_ACTIVE = "spotify_active" # "1" if Spotify Connect is active
    # LBC_SUPPORT = "lbc_support"
    # PRIVACY_MODE = "privacy_mode"
    # WIFI_CHANNEL = "WifiChannel"
    RSSI = "RSSI" # Wi-Fi signal strength
    # BSSID = "BSSID"
    BATTERY = "battery" # "1" if battery present/charging, "0" otherwise
    BATTERY_PERCENT = "battery_percent" # "0" to "100"
    # SECURE_MODE = "securemode"
    # AUTH = "auth"
    # ENCRYPTION = "encry"
    UPNP_UUID = "upnp_uuid" # Should match 'uuid'
    # UART_PASS_PORT = "uart_pass_port"
    # COMMUNICATION_PORT = "communication_port"
    # WEB_FIRMWARE_UPDATE_HIDE = "web_firmware_update_hide"
    # IGNORE_TALKSTART = "ignore_talkstart"
    # WEB_LOGIN_RESULT = "web_login_result"
    # SILENCE_OTA_TIME = "silenceOTATime"
    # IGNORE_SILENCE_OTA_TIME = "ignore_silenceOTATime"
    # NEW_TUNEIN_PRESET_AND_ALARM = "new_tunein_preset_and_alarm"
    # IHEARTRADIO_NEW = "iheartradio_new"
    # NEW_IHEART_PODCAST = "new_iheart_podcast"
    # TIDAL_VERSION = "tidal_version"
    # SERVICE_VERSION = "service_version"
    ETH_MAC_ADDRESS = "ETH_MAC" # Ethernet MAC
    # SECURITY = "security"
    # SECURITY_VERSION = "security_version"
    # FW_RELEASE_VERSION = "FW_Release_version" # Detailed firmware version
    # PCB_VERSION = "PCB_version"
    # EXPIRED = "expired" # License status?
    BT_MAC = "BT_MAC" # Bluetooth MAC
    # AP_MAC = "AP_MAC" # Wi-Fi AP MAC
    # UPDATE_CHECK_COUNT = "update_check_count"
    # BLE_REMOTE_UPDATE_CHECKED_COUNTER = "BleRemote_update_checked_counter"
    # ALEXA_VER = "alexa_ver"
    # ALEXA_BETA_ENABLE = "alexa_beta_enable"
    # ALEXA_FORCE_BETA_CFG = "alexa_force_beta_cfg"
    # VOLUME_CONTROL = "volume_control" # e.g. "hw" or "sw"
    # WLAN_SNR = "wlanSnr"
    # WLAN_NOISE = "wlanNoise"
    # WLAN_FREQ = "wlanFreq"
    # WLAN_DATA_RATE = "wlanDataRate"
    # OTA_INTERFACE_VER = "ota_interface_ver"
    EQ_SUPPORT = "EQ_support" # "1" if device supports EQ settings
    # AUDIO_CHANNEL_CONFIG = "audio_channel_config" # e.g. "L", "R", "S"
    # APP_TIMEZONE_ID = "app_timezone_id"
    # AVS_TIMEZONE_ID = "avs_timezone_id"
    # TZ_INFO_VER = "tz_info_ver"
    # POWER_MODE = "power_mode"
    # SECURITY_CAPABILITIES = "security_capabilities"


# Multiroom attributes from multiroom:getSlaveList JSON response
class MultiroomAttribute(StrEnum):
    NUM_FOLLOWERS = "slaves" # Number of followers as string
    FOLLOWER_LIST = "slave_list" # Array of follower dicts
    UUID = "uuid" # Follower's UUID (should be UDN)
    IP = "ip" # Follower's IP address
    # Add other fields if present in slave_info dict (e.g., name, status)

# MetaInfo for getMetaInfo command (WiiM specific for rich metadata)
class MetaInfo(StrEnum):
    METADATA = "metaData" # Top-level key in the response

class MetaInfoMetaData(StrEnum):
    # Fields within the 'metaData' object
    ALBUM_TITLE = "album"
    TRACK_TITLE = "title"
    TRACK_SUBTITLE = "subtitle"
    ALBUM_ART = "albumArtURI" # URL to album art
    SAMPLE_RATE = "sampleRate"
    BIT_DEPTH = "bitDepth"
    BIT_RATE = "bitRate"
    TRACK_ID = "trackId"
    # Add other fields like 'duration', 'artist' if present

# Manufacturer constant (already in manufacturers.py, but good to have here too for SDK use)
MANUFACTURER_WIIM = "Linkplay" # Or "WiiM" if they changed it in device description

@unique
class AudioOutputHwMode(IntFlag):
    OPTICAL      = (1,  "Optical Out",    1,  "AUDIO_OUTPUT_SPDIF_MODE")
    LINE_OUT     = (2,  "Line Out",       2,  "AUDIO_OUTPUT_AUX_MODE")
    COAXIAL      = (4,  "COAX Out",       3,  "AUDIO_OUTPUT_COAX_MODE")
    HEADPHONES   = (8,  "Headphone Out",  4,  "AUDIO_OUTPUT_PHONE_JACK_MODE")
    SPEAKER_OUT  = (16, "Speaker Out",    7,  "AUDIO_OUTPUT_SPEAKER_MODE")
    OTHER_OUT    = (64, "Other Out",      64, "AUDIO_OTHER_OUT_MODE")

    def __new__(cls, value: int, display_name: str, cmd: int, command_str: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.display_name = display_name
        obj.cmd = cmd
        obj.command_str = command_str
        return obj

    def __str__(self):
        return self.display_name
    
CMD_TO_MODE_MAP: dict[int, AudioOutputHwMode] = {
    member.cmd: member for member in AudioOutputHwMode
}

@unique
class InputMode(IntFlag):
    WIFI        = (1,    "Network",      "wifi")
    BLUETOOTH   = (2,    "Bluetooth",    "bluetooth")
    LINE_IN     = (4,    "Line In",      "line-in")
    OPTICAL     = (8,    "Optical In",   "optical")
    HDMI        = (16,   "TV",           "HDMI")
    PHONO       = (32,   "Phono In",     "phono")

    def __new__(cls, value: int, display_name: str, command_name: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.display_name = display_name
        obj.command_name = command_name
        return obj

    def __str__(self):
        return self.display_name
    
class PlayingMode(StrEnum):
    NETWORK = "10"
    BLUETOOTH = "41"
    LINE_IN = "40"    
    OPTICAL = "43"
    HDMI = "49"
    PHONO = "54"

PLAYING_TO_INPUT_MAP: dict[PlayingMode, InputMode] = {
    # PlayingMode.NETWORK: InputMode.WIFI,
    PlayingMode.BLUETOOTH: InputMode.BLUETOOTH,
    PlayingMode.LINE_IN: InputMode.LINE_IN,
    PlayingMode.OPTICAL: InputMode.OPTICAL,
    PlayingMode.HDMI: InputMode.HDMI,
    PlayingMode.PHONO: InputMode.PHONO,
}
    
SUPPORTED_INPUT_MODES_BY_MODEL = {
    "WiiM Pro": InputMode.WIFI | InputMode.BLUETOOTH | InputMode.LINE_IN | InputMode.OPTICAL,
    "WiiM Pro Plus": InputMode.WIFI | InputMode.BLUETOOTH | InputMode.LINE_IN | InputMode.OPTICAL,
    "WiiM Ultra": InputMode.WIFI | InputMode.BLUETOOTH | InputMode.LINE_IN | InputMode.OPTICAL | InputMode.HDMI | InputMode.PHONO,
    "WiiM Amp": InputMode.WIFI | InputMode.BLUETOOTH | InputMode.LINE_IN | InputMode.OPTICAL | InputMode.HDMI,
    "WiiM Amp Pro": InputMode.WIFI | InputMode.BLUETOOTH | InputMode.LINE_IN | InputMode.OPTICAL | InputMode.HDMI,
    "WiiM Amp Ultra": InputMode.WIFI | InputMode.BLUETOOTH | InputMode.LINE_IN | InputMode.OPTICAL | InputMode.HDMI,
    "WiiM CI MOD A80": InputMode.WIFI | InputMode.BLUETOOTH | InputMode.LINE_IN | InputMode.OPTICAL | InputMode.HDMI,
    "WiiM CI MOD S": InputMode.WIFI | InputMode.BLUETOOTH | InputMode.LINE_IN | InputMode.OPTICAL,    
}

SUPPORTED_OUTPUT_MODES_BY_MODEL = {
    "WiiM Pro": AudioOutputHwMode.LINE_OUT | AudioOutputHwMode.OPTICAL | AudioOutputHwMode.COAXIAL | AudioOutputHwMode.OTHER_OUT,
    "WiiM Pro Plus": AudioOutputHwMode.LINE_OUT | AudioOutputHwMode.OPTICAL | AudioOutputHwMode.COAXIAL | AudioOutputHwMode.OTHER_OUT,
    "WiiM Ultra": AudioOutputHwMode.LINE_OUT | AudioOutputHwMode.OPTICAL | AudioOutputHwMode.COAXIAL | AudioOutputHwMode.HEADPHONES | AudioOutputHwMode.OTHER_OUT,
    "WiiM Amp": AudioOutputHwMode.SPEAKER_OUT | AudioOutputHwMode.OTHER_OUT,
    "WiiM Amp Pro": AudioOutputHwMode.SPEAKER_OUT | AudioOutputHwMode.OTHER_OUT,
    "WiiM Amp Ultra": AudioOutputHwMode.SPEAKER_OUT | AudioOutputHwMode.OTHER_OUT,
    "WiiM CI MOD A80": AudioOutputHwMode.SPEAKER_OUT | AudioOutputHwMode.OTHER_OUT,
    "WiiM CI MOD S": AudioOutputHwMode.LINE_OUT | AudioOutputHwMode.OPTICAL | AudioOutputHwMode.COAXIAL | AudioOutputHwMode.OTHER_OUT,
}

wiimDeviceType = {
    "FF970016": "WiiM Mini",
    "FF98F09C": "WiiM Pro",
    "FF98F3C7": "WiiM Pro",       # no mfi
    "FF98FCDE": "WiiM Pro Plus",
    "FF98F0BC": "WiiM Pro Plus",  # no mfi
    "FF98F359": "WiiM Amp",
    "FF98FC04": "WiiM Amp",       # no mfi
    "FF98F2F7": "WiiM Amp",       # 4layer
    "FF49BC43": "WiiM Amp",       # castlite
    "FF98FC37": "WiiM Amp Pro",
    "FF98F9ED": "WiiM Amp Ultra",
    "FF98F56B": "WiiM CI MODE A80",
    "FF98FB4F": "WiiM CI MODE S",
    # "FF98F824": "Sub Pro",
    "FF98F7F4": "WiiM Ultra",
}

PlayMediumToInputMode = {
    "BLUETOOTH": 2,
    "LINE-IN": 4,
    "OPTICAL": 8,
    "HDMI": 16,
    "PHONO": 32,    
}

VALID_PLAY_MEDIUMS = {
    "SONGLIST-LOCAL",
    "SONGLIST-LOCAL_TF",
    "SONGLIST-NETWORK",
    "QPLAY",
    "TIDAL_CONNECT",
    "Samba",
}

PLAY_MEDIUMS_CTRL = {
    "RADIO-NETWORK",
    "THIRD-DLNA",
    "LINE-IN",
    "OPTICAL",
    "HDMI",
    "PHONO",
}

TRACK_SOURCES_CTRL = {
    "Pandora2",
    "SoundMachine",
    "Soundtrack",
    "iHeartRadio",
}
