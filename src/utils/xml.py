"""
    © Jürgen Schoenemeyer, 26.12.2024

    PUBLIC:
     - open_xml_as_dict(myzip: ZipFile, path: Path | str) -> dict | None
"""

from pathlib import Path
from zipfile import ZipFile

import xmltodict
from xmltodict import ParsingInterrupted

from utils.trace import Trace

def open_xml_as_dict(myzip: ZipFile, path: Path | str) -> dict | None:
    try:
        with myzip.open(path) as xml_file:
            data = xmltodict.parse(xml_file.read())
    except (KeyError, ParsingInterrupted) as err:
        Trace.error(f"{path} > {err}")
        return None

    return data
