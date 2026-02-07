"""
    © Jürgen Schoenemeyer, 07.02.2026 22:49

    src/utils/colors.py

    PUBLIC:
     - hex_to_rgb(hex_color: str) -> Tuple[int, int, int]
     - rgb_to_hex(rgb: Tuple[int, int, int]) -> str
     - hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]
     - rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]

"""
from __future__ import annotations

from typing import Tuple

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]: # noqa: E741
    s /= 100
    l /= 100  # noqa: E741
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    r_: float
    g_: float
    b_: float

    if h < 60:
        r_, g_, b_ = c, x, 0
    elif h < 120:
        r_, g_, b_ = x, c, 0
    elif h < 180:
        r_, g_, b_ = 0, c, x
    elif h < 240:
        r_, g_, b_ = 0, x, c
    elif h < 300:
        r_, g_, b_ = x, 0, c
    else:
        r_, g_, b_ = c, 0, x

    return (
        int((r_ + m) * 255),
        int((g_ + m) * 255),
        int((b_ + m) * 255),
    )

def rgb_to_hsl(red: int, green: int, blue: int) -> Tuple[float, float, float]:
    r:float = red / 255
    g:float = green / 255
    b:float = blue / 255

    max_c = max(r, g, b)
    min_c = min(r, g, b)
    delta = max_c - min_c

    l = (max_c + min_c) / 2  # noqa: E741

    h:float = 0
    s:float = 0

    if delta != 0:
        s = delta / (1 - abs(2 * l - 1))
        if max_c == r:
            h = 60 * (((g - b) / delta) % 6)
        elif max_c == g:
            h = 60 * (((b - r) / delta) + 2)
        else:
            h = 60 * (((r - g) / delta) + 4)

    return round(h), round(s * 100), round(l * 100)
