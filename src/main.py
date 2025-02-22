# pwsh: .venv/Scripts/activate
# bash: source .venv/Scripts/activate
# deactivate

# python src/main.py
# uv run src/main.py

"""
distribute files to all local repos
 - list of repos -> settings/repos.yaml
 - actions -> settings/actions.yaml
"""

import hashlib
import shutil
import sys
from pathlib import Path

from utils.file import (
    delete_file,
    get_modification_timestamp,
    set_modification_timestamp,
)
from utils.globals import BASE_PATH, DRIVE
from utils.prefs import Prefs
from utils.trace import Trace

SOURCE_PATH = BASE_PATH

def main() -> None:
    repos = Prefs.get("repos")
    Trace.action( f"check {len(repos)} repos" )

    modified_repos = 0
    modified_files_all = 0

    for repo in repos:
        dest = DRIVE / repo["path"] / repo["name"]

        if not dest.exists():
            Trace.error(f"Project '{dest}' not found")
            continue

        # copy

        modified_files = 0
        for action_type in ["mandatory", "optional", "new"]:

            for file in Prefs.get(f"actions.copy.{action_type}.common") or []:
                modified_files += copy_file_special( SOURCE_PATH, dest, repo["name"], file, action_type )

            if repo["lib"]:
                for file in Prefs.get(f"actions.copy.{action_type}.lib") or []:
                    modified_files += copy_file_special( SOURCE_PATH, dest, repo["name"], file, action_type )

        # delete

        for file in Prefs.get("actions.delete") or []:
            if delete_file( dest, file ):
                modified_files += 1

        if modified_files>0:
            modified_files_all += modified_files
            modified_repos += 1

    Trace.result( f"{modified_repos} repos, {modified_files_all} files modified" )

# copy file:
#  - mandatory -> copy/overwite files
#  - optional  -> copy/overwrite files, if there is a destination file
#  - new       -> copy file, if there is NO destination file

def copy_file_special( source: Path, dest: Path, name: str, filepath: Path, action_type: str ) -> int:
    src = source / filepath
    dst = dest / filepath

    if not dst.parent.exists():
        dst.parent.mkdir()

    if Path(dst).is_file():
        if action_type == "new":
            return 0

        if not Path(src).is_file():
            Trace.fatal(f"source '{src}' file is missing")
            return 0

        with Path.open(src, "rb") as file:
            text = file.read()
        source_md5 = hashlib.md5(text).hexdigest()

        with Path.open(dst, "rb") as file:
            text = file.read()
        dest_md5 = hashlib.md5(text).hexdigest()

        if (source_md5 != dest_md5 ):
            shutil.copyfile(src, dst)
            set_modification_timestamp( dst, get_modification_timestamp(src) )
            Trace.result( f"copy '{filepath}' => {name}" )
            return 1


    elif action_type in ("mandatory", "new"):
        if not Path(src).is_file():
            Trace.fatal(f"source '{src}' file is missing")
            return 0

        shutil.copyfile(src, dst)
        set_modification_timestamp( dst, get_modification_timestamp(src) )
        Trace.result( f"copy '{filepath}' => {name}" )
        return 1

    return 0

if __name__ == "__main__":
    Trace.set( debug_mode=True, timezone=False )
    Trace.action(f"Python version {sys.version}")

    Prefs.init("settings", "")
    Prefs.load("repos.yaml")
    Prefs.load("actions.yaml")

    try:
        main()
    except KeyboardInterrupt:
        Trace.exception("KeyboardInterrupt")
        sys.exit()
