"""
    © Jürgen Schoenemeyer, 04.01.2025

    PUBLIC:
     - check_zip(in_zip, path: str, files: list) -> Dict[str]
     - expand_zip(source_path: str, dest_path: str) -> bool
     - create_zip(source_path: str, dest_path: str, filename: str, compression = 6) -> bool
"""

import shutil
import os

from typing import Any, Dict
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from utils.trace import Trace
from utils.file  import get_trace_path

def check_zip(myzip: ZipFile, path: Path | str, files: list) -> Dict[str, Any]:
    path = Path(path)

    errors = {}
    for file in files:
        try:
            myzip.extract(file, path)
        except OSError as err:
            errors[file] = str(err)
            Trace.error(f"{file}: {err}")

    return errors

def expand_zip(source_path: Path | str, dest_path: Path | str) -> bool:
    source_path = Path(source_path)
    dest_path = Path(dest_path)

    if os.path.isfile(source_path):
        try:
            shutil.unpack_archive(source_path, dest_path)
            return True

        except OSError as err:
            Trace.error(f"{err}")
            return False
    else:
        Trace.error(f"file not exist: '{get_trace_path(dest_path)}'")
        return False

def create_zip(source_path: Path | str, dest_path: Path | str, filename: str, compression: int = 6) -> bool:
    source_path = Path(source_path)
    dest_path = Path(dest_path)

    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
        Trace.update( f"makedir + '{dest_path}'")

    Trace.info( f"'{get_trace_path(source_path)}/{filename}' > '{get_trace_path(dest_path)}/{filename}'")

    src_path = source_path.expanduser().resolve(strict=True)
    try:
        with ZipFile(dest_path / filename, "w", ZIP_DEFLATED, compresslevel=compression) as zf:
            for file in src_path.rglob("*"):
                zf.write(file, file.relative_to(src_path))
        return True

    except OSError as err:
        Trace.error(f"{err}")
        return False
