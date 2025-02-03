# pwsh: .venv/Scripts/activate
# bash: source .venv/Scripts/activate
# deactivate

# python src/main.py
# uv run src/main.py

import sys
import hashlib
import shutil
from pathlib import Path

from utils.globals   import DRIVE, BASE_PATH
from utils.trace     import Trace
from utils.prefs     import Prefs
from utils.file      import get_modification_timestamp, set_modification_timestamp, delete_file

SOURCE_PATH = BASE_PATH

def main() -> None:
    projects  = Prefs.get("projects")
    mandatory = Prefs.get("files.mandatory")
    optional  = Prefs.get("files.optional")
    new       = Prefs.get("files.new")
    delete    = Prefs.get("files.delete")

    for project in projects:
        dest = DRIVE / project["path"] / project["name"]

        if not dest.exists():
            Trace.error(f"Project '{dest}' not found")
            continue

        Trace.action( f"Project '{project['name']}'" )
        for file in mandatory:
            copy_file_special( SOURCE_PATH, dest, project["name"], file, "mandatory" )

        for file in optional:
            copy_file_special( SOURCE_PATH, dest, project["name"], file, "optional" )

        for file in new:
            copy_file_special( SOURCE_PATH, dest, project["name"], file, "new" )

        for file in delete:
            delete_file( dest, file )

def copy_file_special( source: Path, dest: Path, name: str, filepath: Path, type: str ) -> None:
    src = source / filepath
    dst = dest / filepath

    if not dst.parent.exists():
        dst.parent.mkdir()

    if Path(dst).is_file():
        if type == "new":
            return

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
            set_modification_timestamp( dst, get_modification_timestamp(src) )
            Trace.result( f"copy '{filepath}' => {name}" )

    else:
        if type == "mandatory" or type == "new":
            if not Path(src).is_file():
                Trace.fatal(f"source '{src}' file is missing")

            shutil.copyfile(src, dst)
            set_modification_timestamp( dst, get_modification_timestamp(src) )
            Trace.result( f"copy '{filepath}' => {name}" )

if __name__ == "__main__":
    Trace.set( debug_mode=True, timezone=False )
    Trace.action(f"Python version {sys.version}")
    Trace.action(f"BASE_PATH: '{BASE_PATH.resolve()}'")

    Prefs.init("settings", "")
    Prefs.load("projects.yaml")
    Prefs.load("update.yaml")

    try:
        main()
    except KeyboardInterrupt:
        Trace.exception("KeyboardInterrupt")
        sys.exit()
