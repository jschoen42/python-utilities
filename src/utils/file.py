"""
    © Jürgen Schoenemeyer, 16.03.2025 16:38

    src/utils/file.py

    PUBLIC:
     # timestamp
     - get_modification_timestamp(filename: Path | str) -> float
     - set_modification_timestamp(filename: Path | str, timestamp: float) -> None

     # check
     - check_path_exists(path: str) -> bool
     - check_file_exists(filepath: Path | str, filename: str) -> bool

     # Listing
     - listdir(path: Path | str ) -> Tuple[List[str], List[str]]
     - listdir_match_extention(path: Path | str, extensions: List[str] | None = None) -> Tuple[List[str], List[str]]

     # folder operations
     - list_folders(path: Path | str) -> List[str]:
     - clear_folder(path: Path | str) -> None:
     - delete_folder_tree(dest_path: Path | str, relax: bool = False) -> bool:
     - create_folder( folderpath: Path | str ) -> bool:
     - make_dir(path: Path | str) -> None:
     - delete_file(path: Path | str, filename: str) -> bool:
     - beautify_path( path: Path | str ) -> str:

    #
     - get_trace_path(filepath: Path | str) -> str:
     - get_files_in_folder(path: Path) -> List[str]
     - get_folders_in_folder(path: Path) -> List[str]
     - get_save_filename(path: Path, stem: str, suffix: str) -> str

     - import_text(folderpath: Path | str, filename: Path | str, encoding: str="utf-8", show_error: bool=True) -> str | None
     - import_json(folderpath: Path | str, filename: str, show_error: bool=True) -> Any
     - import_json_timestamp( folderpath: Path | str, filename: str, show_error: bool=True ) -> Tuple[Any, float | None]

     - export_text(folderpath: Path | str, filename: str, text: str, encoding: str="utf-8", newline: str="\n", timestamp: float=0.0, create_new_folder: bool=True, show_message: bool=True) -> str | None:
     - export_json(folderpath: Path | str, filename: str, data: Dict[str, Any] | List[Any], newline: str="\n", timestamp: float=0.0, show_message: bool=True) -> str | None:
     - export_binary_file(filepath: Path | str, filename: str, data: bytes, _timestamp: float=0, create_new_folder: bool=False) -> None
     - export_file(filepath: Path|str, filename: str, text: str, in_type: str | None = None, timestamp: float=0, create_new_folder: bool=True, encoding: str ="utf-8", newline: str="\n", overwrite: bool=True) -> None | str
    #
     - get_filename_unique(dirpath: Path, filename: str) -> str
     - find_matching_file(path_name: str) -> bool | str
     - find_matching_file_path(dirname: Path, filename: str) -> Path | bool
     - get_valid_filename(name: str) -> str
     - get_file_infos(path: Path | str, filename: str, _in_type: str) -> None | Dict
    #
     - copy_my_file(source: str, dest: str, _show_updated: bool) -> bool

    PRIVATE:
     - _increment_filename(filename_stem: str) -> str
"""
from __future__ import annotations

import datetime
import filecmp
import hashlib
import json
import os
import re
import shutil

from pathlib import Path
from re import Match
from typing import Any, Dict, List, Tuple

from utils.trace import Trace

# timestamp

def get_modification_timestamp(filename: Path | str) -> float:
    filename = Path(filename)

    try:
        ret = filename.stat().st_mtime
    except OSError as err:
        Trace.error(f"{err}")
        return 0

    return ret

def set_modification_timestamp(filename: Path | str, timestamp: float) -> None:
    filename = Path(filename)

    try:
        os.utime(filename, (timestamp, timestamp)) # atime and mtime
    except OSError as err:
        Trace.error(f"set_modification_timestamp: {err}")

# check

def check_path_exists(path: Path | str) -> bool:
    return Path(path).exists()

def check_file_exists(filepath_start: Path | str, filepath_end: Path | str) -> bool:

    # case sensitive

    # "/dir1/dir2/dir3" + "/file.ext"
    # "/dir1/dir2" + "/dir3/file.ext"
    # "/dir1" + "/dir2/dir3/file.ext"
    # "" + "/dir1/dir2/dir3/file.ext"

    full_path = Path(filepath_start) / filepath_end

    filepath = full_path.parent
    filename = full_path.name

    if not filepath.exists():
        Trace.error(f"directory missing '{filepath}'")
        return False

    try:
        filenames: list[str] = os.listdir(filepath)
    except OSError as err:
        Trace.error(f"{err}")
        return False

    if filename in filenames:
        return True
    else:
        Trace.error(f"file missing {full_path}")
        return False

# folder Listing

def listdir(path: Path | str ) -> Tuple[List[str], List[str]]:
    return listdir_match_extention( path, [".*"] )

#  extensions: [".zip", ".story", ".xlsx", ".docx"], ".*" => all

def listdir_match_extention(path: Path | str, extensions: List[str]) -> Tuple[List[str], List[str]]:
    path = Path(path)

    extensions = list({ext.lstrip(".") for ext in extensions})

    files:   List[str] = []
    folders: List[str] = []

    if not check_path_exists(path):
        Trace.error( f"folder not found '{path.as_posix()}'" )
        return files, folders

    for file in os.listdir(path):
        if file.startswith("~"):
            Trace.warning(f"skip temp file '{file}'")
            continue

        if (path / file).is_file():
            for extention in extensions:
                if extention == "*" or file.endswith("." + extention):
                    files.append(file)
                    break

        elif (path / file).is_dir():
            folders.append(file)

        else:
            Trace.warning(f"skip unknown filetype '{file}'")

    return files, folders

def list_folders(path: Path | str) -> List[str]:
    path = Path(path)

    folders: List[str] = []
    try:
        for file in os.listdir(path):
            if (path / file).is_dir():
                folders.append(file)
    except OSError as err:
        Trace.error(f"{err}")

    return folders

def clear_folder(path: Path | str) -> None:
    path = Path(path)

    for filepath in path.iterdir():
        try:
            shutil.rmtree(filepath)
        except OSError as err:
            error = str(err).split(":")[0]
            try:
                filepath.unlink()
            except OSError:
                Trace.fatal( f"shutil.rmtree {error} '{get_trace_path(filepath)}'")

def delete_folder_tree(dest_path: Path | str, relax: bool = False) -> bool:
    dest_path = Path(dest_path)

    ret = False
    if dest_path.exists():
        try:
            shutil.rmtree(dest_path)
            ret = True
        except OSError as msg:
            if relax and len(os.listdir(dest_path)) == 0:
                Trace.warning( f"relaxed mode: {msg}")
            else:
                Trace.fatal( f"shutil.rmtree: {msg}")
    else:
        ret = True

    return ret

def create_folder( folderpath: Path | str ) -> bool:
    folderpath = Path(folderpath)

    if not folderpath.is_dir():
        try:
            folderpath.mkdir(parents=True)
            Trace.update( f"makedir: {folderpath}")

        except OSError as err:
            error_msg = str(err).split(":")[0]
            Trace.error( f"{error_msg}: {folderpath}")
            return False

        return True
    else:
        return False

def make_dir(path: Path | str) -> None:
    path = Path(path)

    path.mkdir(parents=True, exist_ok=True)

def delete_file(path: Path | str, filename: str) -> bool:
    filepath = Path(path) / filename

    if filepath.is_file():
        try:
            filepath.unlink()
            Trace.update(f"file '{filepath}' deleted")
            return True

        except OSError as err:
            Trace.error(f"{err}")

    return False

def beautify_path( path: Path | str ) -> str:
    return str( path ).replace("\\\\", "/")

#
# D:\Projekte_P4\Articulate-Storyline\WebService1\_workdir\jobs\c4c3dda9-0e58-49dd-86d0-151fe2267edb\tmp\media\image\resultslideVectorText.png -> media\image\resultslideVectorText.png
#
def get_trace_path(filepath: Path | str) -> str:

    tmp_path = os.path.normpath(filepath).replace("\\", "/")

    if "/_workdir/" in tmp_path:
        trace_path = "./" + tmp_path.split("/tmp/")[1]  # noqa: S108
    else:
        trace_path = tmp_path

    # Trace.info(f"trace_path: {trace_path}")
    return trace_path


def get_files_in_folder( path: Path | str ) -> List[str]:
    path = Path(path)
    return [f for f in os.listdir(path) if (path / f).is_file()]

def get_folders_in_folder( path: Path | str ) -> List[str]:
    path = Path(path)
    return [f for f in os.listdir(path) if (path / f).is_dir()]

def get_save_filename( path: Path | str, stem: str, suffix: str ) -> str:
    files: List[str] = get_files_in_folder( Path(path) )

    name = stem
    while name + suffix in files:
        name = _increment_filename( name )

    return name + suffix

def import_text( folderpath: Path | str, filename: Path | str, encoding: str="utf-8", show_error: bool=True ) -> str | None:
    filepath = Path(folderpath, filename)

    if filepath.is_file():
        try:
            with filepath.open(mode="r", encoding=encoding) as file:
                data = file.read()

        except OSError as err:
            Trace.error(f"{err}")
            return None

        except UnicodeDecodeError as err:
            Trace.error(f"{filepath}: {err}")
            return None

        return data

    else:
        if show_error:
            Trace.error(f"file not exist {filepath.resolve()}")
        return None

def import_json( folderpath: Path | str, filename: str, show_error: bool=True ) -> Any | None:
    result = import_text(folderpath, filename, show_error=show_error)
    if result:
        data = json.loads(result)
        return data
    else:
        return None

def import_json_timestamp( folderpath: Path | str, filename: str, show_error: bool=True ) -> Tuple[Any | None, float]:
    ret = import_json(folderpath, filename, show_error=show_error)
    if ret:
        return ret, get_modification_timestamp(Path(folderpath, filename))
    else:
        return None, 0.0

def export_text(folderpath: Path | str, filename: str, text: str, encoding: str="utf-8", newline: str="\n", timestamp: float=0.0, create_new_folder: bool=True, show_message: bool=True) -> str | None:
    folderpath = Path(folderpath)
    filepath   = Path(folderpath, filename)

    exist = False
    try:
        with filepath.open(mode="r", encoding=encoding) as file:
            text_old = file.read()
            exist = True
    except OSError:
        text_old = ""

    if exist:
        if text == text_old:
            if show_message:
                Trace.info(f"not changed '{filepath}'")
            return str(filename)

    if create_new_folder:
        create_folder(folderpath)

    try:
        with filepath.open(mode="w", encoding=encoding, newline=newline) as file:
            file.write(text)

        if timestamp != 0:
            set_modification_timestamp(filepath, timestamp)

        if show_message:
            if text_old == "":
                Trace.update(f"created '{filepath}'")
            else:
                Trace.update(f"changed '{filepath}'")

        return str(filename)

    except OSError as err:
        error_msg = str(err).split(":")[0]
        Trace.error(f"{error_msg} - {filepath}")
        return None

def export_json(folderpath: Path | str, filename: str, data: Dict[str, Any] | List[Any], newline: str="\n", timestamp: float=0.0, show_message: bool=True) -> str | None:
    text = json.dumps(data, ensure_ascii=False, indent=2)

    return export_text(folderpath, filename, text, encoding="utf-8", newline=newline, timestamp=timestamp, show_message=show_message)

def export_binary_file(filepath: Path | str, filename: str, data: bytes, _timestamp: float=0, create_new_folder: bool=False) -> None:
    filepath = Path(filepath)

    if create_new_folder:
        if not filepath.is_dir():
            filepath.mkdir(parents=True)
            Trace.update( f"makedir '{filepath}'")

    with (filepath / filename).open(mode="wb") as f:
        f.write(data)

def export_file(filepath: Path | str, filename: str, text: str, in_type: str | None = None, encoding: str ="utf-8", newline: str="\n",timestamp: float=0.0, create_new_folder: bool=True, overwrite: bool=True) -> None | str:
    filepath = Path(filepath)

    trace_export_path_folder = get_trace_path(filepath)
    trace_export_path        = get_trace_path(filepath / filename)

    if text == "":
        Trace.error(f"text empty '{trace_export_path}'")
        return None

    if overwrite:
        my_filename = filename
    else:
        tmp: list[str] = filename.split(".")
        ext = tmp.pop()
        dest2 = ".".join(tmp)
        copy = ""

        c = 0
        while (filepath / (dest2 + copy + "." + ext)).is_file():
            if c == 0:
                c = 2
            else:
                c += 1
            copy = "_[" + str(c) + "]"

        my_filename = dest2 + copy + "." + ext

    try:
        with (filepath / my_filename).open(mode="r", encoding=encoding) as f:
            ref_text = f.read()
    except OSError:
        ref_text = ""

    if text == ref_text:
        # Trace.wait( f"{my_filename}")

        if in_type:
            Trace.info( f"'{in_type}' not changed '{trace_export_path}'")
        else:
            Trace.info( f"not changed '{trace_export_path}'")

        return my_filename

    else:
        if create_new_folder:
            if not filepath.is_dir():
                try:
                    filepath.mkdir(parents=True)
                    Trace.update( f"makedir: '{trace_export_path_folder}'")
                except OSError as err:
                    error = str(err).split(":")[0]
                    Trace.error(f"{error}: '{trace_export_path_folder}'")
                    return None

        try:
            with (filepath / my_filename).open(mode="w", encoding=encoding, newline=newline) as f:
                f.write(text)

            if timestamp != 0:
                set_modification_timestamp(filepath / my_filename, timestamp)

            if ref_text == "":
                if in_type:
                    Trace.update( f"'{in_type}' created '{trace_export_path}'")
                else:
                    Trace.update( f"created '{trace_export_path}'")

            elif in_type:
                Trace.update( f"'{in_type}' changed '{trace_export_path}'")
            else:
                Trace.update( f"changed '{trace_export_path}'")

        except OSError as err:
            error = str(err).split(":")[0]
            Trace.error(f"{error} '{trace_export_path}'")
            return None

        return my_filename


# increment_filename(filename_stem: str) -> str:
#
# 'filaname'     -> 'filaname (1)'
# 'filaname (1)' -> 'filaname (2)'
# 'filaname (2)' -> 'filaname (3)'
# ...

def _increment_filename(filename_stem: str) -> str:
    pattern = r"^(.*?)(?: \((\d+)\))?$"

    match: Match[str] | None = re.match(pattern, filename_stem)
    if match:
        base_name, number = match.groups()
        number = int(number) + 1 if number else 1

        new_name = f"{base_name} ({number})"
        return new_name

    return filename_stem

def get_filename_unique(dirpath: Path, filename: str) -> str:
    suffix = Path(filename).suffix
    stem = Path(filename).stem

    number = 1
    append = ""
    while (dirpath / (stem + append + suffix)).is_file():
        number += 1
        append = "_[" + str(number) + "]"

    return stem + append + suffix

def find_matching_file(path_name: Path | str) -> bool | str:
    path = Path(path_name)
    matches = list(path.glob("*"))

    if len(matches) == 0:
        Trace.error(f"file not found: {path_name}")
        return False

    if len(matches) > 1:
        Trace.error(f"file not unique: {path_name} - {matches}")
        return False

    return str(matches[0]).replace("\\", "/")

def find_matching_file_path(dirpath: Path, filename: str) -> None | Path:
    filepath = dirpath / filename

    matches = list(filepath.parent.glob(filepath.name))

    if len(matches) == 0:
        Trace.error(f"file not found: {filepath}")
        return None

    if len(matches) > 1:
        Trace.error(f"file not unique: {filepath} - {matches}")
        return None

    return matches[0]

def get_valid_filename(name: str) -> str:
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    #if s in {"", ".", ".."}:
    #    raise SuspiciousFileOperation("Could not derive file name from '%s'" % name)
    return s

def get_file_infos(path: Path | str, filename: str, _in_type: str) -> None | Dict[str, Any]:
    filepath = Path(path, filename)

    if filepath.is_file():
        with filepath.open(mode="rb") as file:
            md5 = hashlib.md5(file.read()).hexdigest()  # noqa: S324

        size           = filepath.stat().st_size
        timestamp      = get_modification_timestamp(filepath)
        date_timestamp = datetime.datetime.fromtimestamp(timestamp).astimezone().isoformat()

        if timestamp.is_integer():
            data_dot_net = date_timestamp
        else:
            decimal_digits = f"{timestamp:.7f}".split(".")[1]
            data_dot_net = date_timestamp[:20] + decimal_digits + date_timestamp[-6:]

        return {
            "date":       date_timestamp, # 2024-08-13T09:38:38.935807+02:00  (6 decimal digits)
            "dateDotNet": data_dot_net,   # 2024-08-13T09:38:38.9358065+02:00 (7 decimal digits)
            "bytes":      size,
            "md5":        md5,
        }
    else:
        Trace.error( f"not found: {filepath}" )
        return None

def copy_my_file(source: Path | str, dest: Path | str, _show_updated: bool) -> bool:

    source = Path(source)
    dest   = Path(dest)

    new_timestamp = get_modification_timestamp(source)

    if not dest.exists() or not filecmp.cmp(source, dest):
        try:
            shutil.copyfile(source, dest)
            set_modification_timestamp(dest, timestamp=new_timestamp)
            Trace.info( f"copy {dest}" )

        except OSError as err:
            Trace.error(f"{err}")
            return False

    return True
