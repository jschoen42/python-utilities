"""
    © Jürgen Schoenemeyer, 22.02.2025

    src/utils/xml.py

    PUBLIC:
     - open_xml_as_dict(myzip: ZipFile, path: str) -> Dict[str, Any] | None
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

import xmltodict
from xmltodict import ParsingInterrupted

from utils.trace import Trace

if TYPE_CHECKING:
    from zipfile import ZipFile


def open_xml_as_dict(myzip: ZipFile, path: str) -> Dict[str, Any] | None:
    try:
        with myzip.open(path) as xml_file:
            data = xmltodict.parse(xml_file.read())
    except (KeyError, ParsingInterrupted) as err:
        Trace.error(f"{path} > {err}")
        return None

    return data
