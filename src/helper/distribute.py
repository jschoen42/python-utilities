"""
    © Jürgen Schoenemeyer, 23.03.2025 15:59

    src/helper/distrubute.py
"""
from __future__ import annotations

import hashlib
import shutil

from pathlib import Path

from utils.file import delete_file, get_modification_timestamp, set_modification_timestamp
from utils.globals import BASE_PATH, ROOT
from utils.prefs import Prefs
from utils.trace import Trace

def format_singular_plural(value: int, text: str) -> str:
    if value == 1:
        return f"{value} {text}"
    return f"{value} {text}s"

def distribute(force: bool = False) -> None:
    repos = Prefs.get("repos")
    Trace.action( f"check {len(repos)} repos" )

    modified_repos = 0
    modified_files_all = 0

    for repo in repos:
        dest = ROOT / repo["path"] / repo["name"]
        if not dest.exists():
            Trace.error(f"Project '{dest}' not found")
            continue

        modified_files = 0

        # delete

        if repo.get("delete", True):
            for file in Prefs.get("actions.delete") or []:
                if delete_file( dest, file ):
                    modified_files += 1

        # copy

        if repo.get("copy", True):
            for action_type in ["mandatory", "optional", "new"]:

                for file in Prefs.get(f"actions.copy.{action_type}.common") or []:
                    modified_files += copy_file_special( BASE_PATH, dest, repo["name"], file, action_type, force=force)

                if repo["lib"]:
                    for file in Prefs.get(f"actions.copy.{action_type}.lib") or []:
                        modified_files += copy_file_special( BASE_PATH, dest, repo["name"], file, action_type, force=force)

                if repo["git"]:
                    for file in Prefs.get(f"actions.copy.{action_type}.git") or []:
                        modified_files += copy_file_special( BASE_PATH, dest, repo["name"], file, action_type, force=force)

        if modified_files>0:
            modified_files_all += modified_files
            modified_repos += 1

    Trace.result( f"modified {format_singular_plural(modified_files_all, "file")} to {format_singular_plural(modified_repos, "repo")}")

# copy file:
#  - mandatory -> copy/overwite files
#  - optional  -> copy/overwrite files, if there is a destination file
#  - new       -> copy file, if there is NO destination file

def copy_file_special( source: Path, dest: Path, name: str, filepath: Path, action_type: str, force: bool = False ) -> int:
    src = source / filepath
    dst = dest / filepath

    if not dst.parent.exists():
        dst.parent.mkdir()

    if dst.is_file():
        if action_type == "new":
            return 0

        if not src.is_file():
            Trace.fatal(f"source '{src}' file is missing")
            return 0

        with Path.open(src, "rb") as file:
            text = file.read()
        source_md5 = hashlib.md5(text).hexdigest()

        src_timestamp = src.stat().st_mtime

        if src.exists():
            dst_timestamp = dst.stat().st_mtime
        else:
            dst_timestamp = 0

        with Path.open(dst, mode="rb") as file:
            text = file.read()

        dest_md5 = hashlib.md5(text).hexdigest()

        if (source_md5 != dest_md5):
            if dst_timestamp>src_timestamp and not force:
                Trace.error( f"'{name}/{filepath}' is newer" )
                return 0
            else:
                shutil.copyfile(src, dst)
                set_modification_timestamp( dst, get_modification_timestamp(src) )
                Trace.result( f"copy '{filepath}' => {name}" )
                return 1

    elif action_type in ("mandatory", "new"):
        if not src.is_file():
            Trace.fatal(f"source '{src}' file is missing")
            return 0

        shutil.copyfile(src, dst)
        set_modification_timestamp( dst, get_modification_timestamp(src) )
        Trace.result( f"copy '{filepath}' => {name}" )
        return 1

    return 0
