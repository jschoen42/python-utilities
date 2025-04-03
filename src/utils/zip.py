"""
    © Jürgen Schoenemeyer, 03.04.2025 20:50

    src/utils/zip.py

    PUBLIC:
     - check_zip(in_zip, path: str, files: List) -> Dict[str]
     - expand_zip(source_path: str, dest_path: str) -> bool
     - create_zip(source_path: str, dest_path: str, filename: str, compression = 6) -> bool
"""
from __future__ import annotations

import shutil

from pathlib import Path
from typing import Any, Dict, List
from zipfile import ZIP_DEFLATED, ZipFile

from utils.file import get_trace_path
from utils.trace import Trace

def check_zip(myzip: ZipFile, path: Path | str, files: List[str]) -> Dict[str, Any]:
    path = Path(path)

    errors: Dict[str, Any] = {}
    for file in files:
        try:
            myzip.extract(file, path)
        except OSError as e:
            errors[file] = str(e)
            Trace.error(f"{file}: {e}")

    return errors

def expand_zip(source_path: Path | str, dest_path: Path | str) -> bool:
    source_path = Path(source_path)
    dest_path = Path(dest_path)

    if Path.is_file(source_path):
        try:
            shutil.unpack_archive(source_path, dest_path)
        except OSError as e:
            Trace.error(f"{e}")
            return False

        return True
    else:
        Trace.error(f"file not exist: '{get_trace_path(dest_path)}'")
        return False

def create_zip(source_path: Path | str, dest_path: Path | str, filename: str, compression: int = 6) -> bool:
    source_path = Path(source_path)
    dest_path   = Path(dest_path)

    if not dest_path.is_dir():
        dest_path.mkdir(parents=True)
        Trace.update(f"makedir + '{dest_path}'")

    Trace.info(f"'{get_trace_path(source_path)}/{filename}' > '{get_trace_path(dest_path)}/{filename}'")

    src_path = source_path.expanduser().resolve(strict=True)
    try:
        with ZipFile(dest_path / filename, "w", ZIP_DEFLATED, compresslevel=compression) as zf:
            for file in src_path.rglob("*"):
                zf.write(file, file.relative_to(src_path))
    except OSError as e:
        Trace.error(f"{e}")
        return False

    return True
