"""
    © Jürgen Schoenemeyer, 27.05.2025 18:20

    src/utils/metadata_mutagen.py

    PUBLIC:
     - def get_audioinfo_mutagen(filepath: str) -> None | Dict[str, Any]
     - get_audio_metadata_mutagen(filepath: Path | str) -> None | Dict[str, Any]
     - get_video_metadata_mutagen(filepath: Path | str) -> None | Dict[str, Any]
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Protocol, cast

from mutagen._util import MutagenError  # ty # type: ignore[reportPrivateImportUsage]
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

from utils.decorator import deprecated
from utils.trace import Trace

if TYPE_CHECKING:
    from pathlib import Path


class MP3Info(Protocol): # -> mypi
    info:         Any
    length:       float
    mode:         int
    channels:     int
    bitrate_mode: str
    bitrate:      int
    sample_rate:  int

class MP4Info(Protocol): # -> mypi
    info:         Any
    length:       float
    mode:         int
    bitrate:      int
    sample_rate:  int

###########################################
#  mutagen
#  https://pypi.org/project/mutagen/
###########################################

@deprecated("licence does not fit")
def get_audioinfo_mutagen(filepath: str) -> None | Dict[str, Any]:
    try:
        metadata = MP3.Open(filepath) # type: ignore [attr-defined] # PyRight: Attribute "Open" is unknown
    except MutagenError as e:
        Trace.error(f"MutagenError: {e}")
        return None

    mp3_info = cast("MP3Info", metadata)

    duration = mp3_info.info.length
    if mp3_info.info.mode == 3:
        channels = 1
    else:
        channels = 2

    samples = 44100
    bits = int(channels * duration * samples * 2)
    sample_count = int(bits / 2)
    start_ptr = 106
    bytes_count = bits + start_ptr

    return {
        "bytes":     bytes_count,
        "channels":  channels,
        "samples":   samples,
        "bits":      bits,
        "sampleCnt": sample_count,
        "startPt":   start_ptr,
    }

@deprecated("licence does not fit")
def get_audio_metadata_mutagen(filepath: Path | str) -> None | Dict[str, Any]:
    try:
        metadata = MP3.Open(filepath) # type: ignore [attr-defined] # PyRight: Attribute "Open" is unknown
    except MutagenError as e:
        Trace.error(f"MutagenError: {e}")
        return None

    mp3_info = cast("MP3Info", metadata)

    duration     = mp3_info.info.length
    channels     = mp3_info.info.channels
    mode: str    = ["STEREO", "JOINTSTEREO", "DUALCHANNEL", "MONO"][int(mp3_info.info.mode)]
    bitrate_mode = mp3_info.info.bitrate_mode.split(".")[1]
    bitrate      = mp3_info.info.bitrate
    sample_rate  = mp3_info.info.sample_rate

    return {
        "duration":    round(duration, 2),
        "channels":    channels,
        "mode":        mode,
        "bitrateMode": bitrate_mode,
        "bitrate":     int(bitrate / 1000),
        "sampleRate":  sample_rate,
    }

@deprecated("licence does not fit")
def get_video_metadata_mutagen(filepath: Path | str) -> None | Dict[str, Any]:
    try:
        metadata = MP4.Open(filepath) # type: ignore [attr-defined] # PyRight: Attribute "Open" is unknown
    except MutagenError as e:
        Trace.error(f"MutagenError: {e}")
        return None

    mp4_info = cast("MP4Info", metadata)

    duration    = mp4_info.info.length
    mode        = ["STEREO", "JOINTSTEREO", "DUALCHANNEL", "MONO"][mp4_info.mode]
    bitrate     = mp4_info.info.bitrate
    sample_rate = mp4_info.info.sample_rate

    return {
        "audio":           True,
        "durationAudio":   round(duration, 2),
        "bitrateAudio":    int(bitrate / 1000),
        "modeAudio":       mode,
        "sampleRateAudio": sample_rate,
    }
