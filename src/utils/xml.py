"""
    © Jürgen Schoenemeyer, 10.01.2025

    PUBLIC:
     - open_xml_as_dict(myzip: ZipFile, path: str) -> Dict | None
"""
from typing import Any, Dict
from zipfile import ZipFile

import xmltodict
from xmltodict import ParsingInterrupted

from utils.trace import Trace

def open_xml_as_dict(myzip: ZipFile, path: str) -> Dict[str, Any] | None:
    try:
        with myzip.open(path) as xml_file:
            data = xmltodict.parse(xml_file.read())
    except (KeyError, ParsingInterrupted) as err:
        Trace.error(f"{path} > {err}")
        return None

    return data
