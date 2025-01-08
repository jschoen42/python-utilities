"""
    © Jürgen Schoenemeyer, 08.01.2025

    PUBLIC:
     - get_audioinfo_mutagen(filepath: str) -> None | Dict
     - get_audio_metadata_mutagen(filepath: Path | str) -> None | Dict
     - get_video_metadata_mutagen(filepath: Path | str) -> None | Dict
"""

from typing import Any, Dict, Protocol, cast
from pathlib import Path

from mutagen import MutagenError
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

from utils.trace import Trace
from utils.decorator import deprecated

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
def get_audioinfo_mutagen(filepath: str) -> None | Dict:
    try:
        metadata = MP3.Open(filepath)  # type: ignore
    except MutagenError as err:
        Trace.error(f"MutagenError: {err}")
        return None

    mp3_info = cast(MP3Info, metadata)

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
        "startPt":   start_ptr
    }

@deprecated("licence does not fit")
def get_audio_metadata_mutagen(filepath: Path | str) -> None | Dict:
    try:
        metadata = MP3.Open(filepath)  # type: ignore
    except MutagenError as err:
        Trace.error(f"MutagenError: {err}")
        return None

    mp3_info = cast(MP3Info, metadata)

    duration     = mp3_info.info.length
    channels     = mp3_info.info.channels
    mode         = ["STEREO", "JOINTSTEREO", "DUALCHANNEL", "MONO"][mp3_info.info.mode]
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
def get_video_metadata_mutagen(filepath: Path | str) -> None | Dict:
    try:
        metadata = MP4.Open(filepath)  # type: ignore
    except MutagenError as err:
        Trace.error(f"MutagenError: {err}")
        return None

    mp4_info = cast(MP4Info, metadata)

    duration    = mp4_info.info.length
    mode        = ["STEREO", "JOINTSTEREO", "DUALCHANNEL", "MONO"][mp4_info.mode]
    bitrate     = mp4_info.info.bitrate
    sample_rate = mp4_info.info.sample_rate

    return {
        "audio":           True,
        "durationAudio":   round(duration, 2),
        "bitrateAudio":    int(bitrate / 1000),
        "modeAudio":       mode,
        "sampleRateAudio": sample_rate
    }
