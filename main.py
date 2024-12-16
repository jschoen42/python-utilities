# pwsh: .venv/Scripts/activate
# bash: source .venv/Scripts/activate
# deactivate

# python main.py

import sys
import hashlib
import shutil
from pathlib import Path

from src.utils.trace     import Trace, BASE_PATH
from src.utils.decorator import duration
from src.utils.prefs     import Prefs

SOURCE_PATH = BASE_PATH

DRIVE = Path(__file__).drive

def main():
    projects  = Prefs.get("projects")
    mandatory = Prefs.get("files.mandatory")
    optional  = Prefs.get("files.optional")

    for project in projects:
        Trace.info( project["name"] )
        dest = Path(DRIVE + project["path"]) / project["name"]
        for file in mandatory:
            copy_file_if_different( SOURCE_PATH, dest, project["name"], file, True )

        for file in optional:
            copy_file_if_different( SOURCE_PATH, dest, project["name"], file, False )

def copy_file_if_different( source, dest, name, filepath, mandatory ):
    src = source / filepath
    dst = dest / filepath

    if Path(dst).is_file():
        with open(src, "rb") as file:
            text = file.read()
        source_md5 = hashlib.md5(text).hexdigest()

        with open(dst, "rb") as file:
            text = file.read()
        dest_md5 = hashlib.md5(text).hexdigest()

        if (source_md5 != dest_md5 ):
            shutil.copyfile(src, dst)
            Trace.result( name, filepath )
    else:
        if mandatory:
            shutil.copyfile(src, dst)
            Trace.error( name, filepath )


if __name__ == "__main__":
    Trace.set( debug_mode=True, timezone=False )
    Trace.action(f"Python version {sys.version}")

    Prefs.init("settings", "")
    Prefs.read("projects.yaml")
    Prefs.read("update.yaml")
    main()
