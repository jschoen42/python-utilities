"""
    © Jürgen Schoenemeyer, 23.03.2025 15:59

    src/main.py

    .venv/Scripts/activate

    python src/main.py
    uv run src/main.py

    distribute files to all local repos
     - list of repos -> settings/repos.yaml
     - actions -> settings/actions.yaml

    parameter:
     - overwrite newer files:  -f --force
"""
from __future__ import annotations

import sys

from argparse import ArgumentParser

from helper.distribute import distribute
from utils.prefs import Prefs
from utils.trace import Trace

if __name__ == "__main__":
    Trace.set( timezone=False, show_caller=False )
    Trace.action(f"Python version {sys.version}")

    Prefs.init("settings", "")
    Prefs.load("repos.yaml")
    Prefs.load("actions.yaml")

    parser = ArgumentParser(description="distribute common files to all my repos defined in settings/repos.yaml")
    parser.add_argument("-f", "--force", action="store_true", help="force overwrite newer files")
    args = parser.parse_args()

    try:
        distribute(args.force)
    except KeyboardInterrupt:
        Trace.exception("KeyboardInterrupt")
        sys.exit()
