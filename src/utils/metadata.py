"""
    © Jürgen Schoenemeyer, 27.05.2025 18:20

    src/utils/metadata.py

    PUBLIC:
     - get_media_info(filepath: str | BytesIO) -> None | Dict[str, int | float]
     - get_audio_duration(filepath: str | BytesIO) -> float
     - get_media_trackinfo(filepath: str | BytesIO) -> None | Dict[str, Any]
     - get_video_metadata(filepath: str | BytesIO) -> None | Dict[str, Any]
     - get_audio_metadata(filepath: str | BytesIO) -> None | Dict[str, Any]
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Protocol

from pymediainfo import MediaInfo, Track

from utils.trace import Trace

if TYPE_CHECKING:
    from io import BytesIO


class AudioTrack(Protocol):
    track_type: str                        # "Audio"
    bit_rate: int                          # 107336
    bit_rate_mode: str                     # "VBR"
    channel_s: int                         # 1
    commercial_name: str                   # "MPEG Audio"
    compression_mode: str                  # "Lossy"
    count: str                             # "285"
    count_of_stream_of_this_kind: str      # "1"
    duration: int                          # 6504
    encoding_settings: str                 # "-m m -V 4 -q 0 -lowpass 17.5 --vbr-new -b 32" (* optional)
    format: str                            # "MPEG Audio"
    format_profile: str                    # "Layer 3"
    format_settings: str                   # "Joint stereo / MS Stereo" (* optional, mono -> empty)
    format_version: str                    # "Version 1"
    frame_count: str                       # "271"
    frame_rate: str                        # "41.667"
    internet_media_type: str               # "audio/mpeg"
    kind_of_stream: str                    # "Audio"
    minimum_bit_rate: int                  # 32000
    proportion_of_this_stream: str         # "0.99236"
    replay_gain: str                       # "-6.62"
    replay_gain_peak: str                  # "0.944061"
    samples_count: str                     # "312192"
    samples_per_frame: str                 # "1152"
    sampling_rate: int                     # 48000
    stream_identifier: str                 # "0"
    stream_size: int                       # 87264
    writing_library: str                   # "LAME3.101"

class VideoTrack(Protocol):
    track_type: str                        # "Video"
    bit_depth: int                         # 8
    chroma_subsampling: str                # "4:2:0"
    codec_id: str                          # "V_VP9"
    codec_id_url: str                      # "http://www.webmproject.org/" (* optional)
    color_primaries: str                   # "BT.709"
    color_range: str                       # "Limited"
    color_space: str                       # "YUV"
    colour_description_present: str        # "Yes"
    colour_description_present_source: str # "Container"
    colour_primaries_source: str           # "Container"
    colour_range_source: str               # "Container / Stream"
    commercial_name: str                   # "VP9"
    count: str                             # "381"
    count_of_stream_of_this_kind: str      # "1"
    default: str                           # "Yes"
    delay: int                             # 0
    delay__origin: str                     # "Container"
    display_aspect_ratio: str              # "1.778"
    duration: str                          # "1195940.000000"
    forced: str                            # "No"
    format: str                            # "VP9"
    format_profile: str                    # "0"
    frame_count: str                       # "59797"
    frame_rate: str                        # "50.000"
    frame_rate_mode: str                   # "CFR"
    framerate_den: str                     # "1"
    framerate_num: str                     # "50"
    height: int                            # 1080
    kind_of_stream: str                    # "Video"
    language: str                          # "en"
    matrix_coefficients: str               # "BT.709"
    matrix_coefficients_source: str        # "Container / Stream"
    pixel_aspect_ratio: str                # "1.000"
    sampled_height: str                    # "1080"
    sampled_width: str                     # "1920"
    stream_identifier: str                 # "0"
    streamorder: str                       # "0"
    track_id: int                          # 1
    transfer_characteristics: str          # "BT.709"
    transfer_characteristics_source: str   # "Container"
    unique_id: str                         # "8640863827297483320"
    width: int                             # 1920

def get_media_info(filepath: str | BytesIO) -> Dict[str, int | float] | None:

    try:
        track = get_media_trackinfo(filepath)
        if track is None:
            return None

    except FileNotFoundError as e:
        Trace.error(f"FileNotFoundError '{e}'")
        return None

    except (AttributeError, ValueError) as e:
         Trace.error(f"MediaInfo: {e}")
         return None

    audio_track: Track = track

    return {
        "duration": round(audio_track.duration/1000, 3), # ty #type: ignore[unresolved-attribute]
        "channels": audio_track.channel_s,               # ty #type: ignore[unresolved-attribute]
        "samplingRate": audio_track.sampling_rate,       # ty #type: ignore[unresolved-attribute]
    }


def get_media_trackinfo(filepath: str | BytesIO) -> Track | None:
    ret = None

    try:
        media_info = MediaInfo.parse(filepath)

    except FileNotFoundError as e:
        Trace.error(f"FileNotFoundError '{e}'")
        return None

    except (AttributeError, ValueError) as e:
         Trace.error(f"MediaInfo: {e}")
         return None

    for track in media_info.tracks:
        if track.track_type == "Audio":
            ret = track
            break

    return ret

def get_audio_duration(filepath: str | BytesIO) -> float:
    duration: float = -1

    try:
        media_info = MediaInfo.parse(filepath)
    except FileNotFoundError as e:
        Trace.error(f"FileNotFoundError '{e}'")
        return -1

    except (AttributeError, ValueError) as e:
         Trace.error(f"MediaInfo: {e}")
         return -1

    for track in media_info.tracks:
        if track.track_type == "Audio":
            duration = round(int(track.duration) / 1000, 3)
            break

    return duration

def get_video_metadata(filepath: str | BytesIO) -> None | Dict[str, Any]:

    info: Dict[str, Any] = {
        "width":    0,
        "height":   0,
        "duration": 0,
        "bitrate":  0.0,
        "tracks":   0,

        "video": {
            "trackID":    0,
            "format":     "",
            "bitrate":    0.0,
            "fps":        0.0,
            "colorInfo":  "",
        },

        "audio": {
            "trackID":      0,
            "format":       "",
            "channels":     0,
            "bitrate":      0.0,
            "samplingRate": 0,
        },
    }

    # https://pymediainfo.readthedocs.io/en/stable/

    try:
        media_info = MediaInfo.parse(filepath)

    except FileNotFoundError as e:
        Trace.error(f"FileNotFoundError '{e}'")
        return None

    except (AttributeError, ValueError) as e:
         Trace.error(f"MediaInfo: {e}")
         return None

    for track in media_info.tracks:
        if track.track_type == "Video":

            info["width"]  = track.width
            info["height"] = track.height
            info["tracks"] += 1

            if track.duration:
                info["duration"] = round(track.duration / 1000, 3)

            info["video"]["track"] = track.track_id
            if track.bit_rate:
                bitrate =  int(track.bit_rate) / 1000
                info["video"]["bitrate"]  = bitrate

                if info["bitrate"] == 0:
                    info["bitrate"] = bitrate
                else:
                    info["bitrate"] += bitrate

            info["video"]["format"]    = track.format + " " + track.format_profile
            info["video"]["fps"]       = float(track.frame_rate)
            info["video"]["colorInfo"] = track.color_space + " " + track.chroma_subsampling

        if track.track_type == "Audio":

            info["tracks"] += 1
            info["audio"]["trackID"] = track.track_id
            if int(track.bit_rate):
                bitrate =  int(track.bit_rate) / 1000
                info["audio"]["bitrate"] = bitrate
                if info["bitrate"] == 0:
                    info["bitrate"] = bitrate
                else:
                    info["bitrate"] += bitrate

            if int(track.channel_s) < 3:
                channels = ["mono", "stereo"][int(track.channel_s)-1]
            else:
                channels = str(track.channel_s) + " channels"

            info["audio"]["channels"]     = track.channel_s
            info["audio"]["samplingRate"] = track.sampling_rate
            info["audio"]["format"]       = track.format  + " " + track.format_additionalfeatures + " (" + channels + ")"

    return info

def get_audio_metadata(filepath: str | BytesIO) -> None | Dict[str, Any]:

    info: Dict[str, Any] = {
        "duration":     0,
        "format":       "",
        "channels":     0,
        "bitrate":      0.0,
        "samplingRate": 0,
    }

    try:
        media_info = MediaInfo.parse(filepath)

    except FileNotFoundError as e:
        Trace.error(f"FileNotFoundError '{e}'")
        return None

    except (AttributeError, ValueError) as e:
         Trace.error(f"MediaInfo: {e}")
         return None

    for track in media_info.tracks:
        if track.track_type == "Audio":
            if track.bit_rate:
                info["bitrate"] = track.bit_rate / 1000

            if int(track.channel_s) < 3:
                channels = ["mono", "stereo"][int(track.channel_s)-1]
            else:
                channels = str(track.channel_s) + " channels"

            info["channels"]     = int(track.channel_s)
            info["samplingRate"] = track.sampling_rate
            info["format"]       = track.format  + " " + track.format_additionalfeatures + " (" + channels + ")"
            break

    return info
