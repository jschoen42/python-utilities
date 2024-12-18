# pwsh: .venv/Scripts/activate
# bash: source .venv/Scripts/activate
# deactivate

# python main.py

import os
import sys
import hashlib
import shutil
from pathlib import Path

from src.utils.globals   import BASE_PATH, DRIVE
from src.utils.trace     import Trace
from src.utils.prefs     import Prefs
from src.utils.file      import get_modification_timestamp, set_modification_timestamp

SOURCE_PATH = BASE_PATH

def main():
    projects  = Prefs.get("projects")
    mandatory = Prefs.get("files.mandatory")
    optional  = Prefs.get("files.optional")

    for project in projects:
        dest = Path(DRIVE + project["path"]) / project["name"]

        if not os.path.exists(dest):
            Trace.error(f"Project '{dest}' not found")
            continue

        Trace.action( project["name"] )
        for file in mandatory:
            copy_file_if_different( SOURCE_PATH, dest, project["name"], file, True )

        for file in optional:
            copy_file_if_different( SOURCE_PATH, dest, project["name"], file, False )

def copy_file_if_different( source, dest, name, filepath, mandatory ):
    src = source / filepath
    dst = dest / filepath

    if not dst.parent.exists():
        dst.parent.mkdir()

    if Path(dst).is_file():
        if not Path(src).is_file():
            Trace.fatal(f"source '{src}' file is missing")

        with open(src, "rb") as file:
            text = file.read()
        source_md5 = hashlib.md5(text).hexdigest()

        with open(dst, "rb") as file:
            text = file.read()
        dest_md5 = hashlib.md5(text).hexdigest()

        if (source_md5 != dest_md5 ):
            shutil.copyfile(src, dst)
            Trace.result( f"copy '{filepath}' => {name}" )
            set_modification_timestamp( dst, get_modification_timestamp(src) )

    else:
        if mandatory:
            shutil.copyfile(src, dst)
            set_modification_timestamp( dst, get_modification_timestamp(src) )
            Trace.result( f"copy '{filepath}' => {name}" )

if __name__ == "__main__":
    Trace.set( debug_mode=True, timezone=False )
    Trace.action(f"Python version {sys.version}")

    Prefs.init("settings", "")
    Prefs.read("projects.yaml")
    Prefs.read("update.yaml")
    main()
