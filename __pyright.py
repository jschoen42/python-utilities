# python __pyright.py src/main.py
# uv run __pyright.py src/main.py

# install pyright: npm install --global pyright

import sys
import subprocess
import platform
import json
import os
import shutil

from pathlib import Path
from datetime import datetime

BASE_PATH = Path(sys.argv[0]).parent.parent.resolve()

def run_pyright(target_file: str) -> None:

    settings = {
        "reportMissingImports": "warning",
        "reportPossiblyUnboundVariable": "none",

        # strict
        "reportMissingTypeStubs": True,
        "reportOptionalSubscript": True,
        "reportOptionalMemberAccess": True,
        "reportOptionalCall": True,
        "reportOptionalIterable": True,
        "reportOptionalContextManager": True,
        "reportOptionalOperand": True,
        "reportUntypedFunctionDecorator": True,
        "reportUntypedClassDecorator": True,
        "reportUntypedBaseClass": True,
        "reportUntypedNamedTuple": True,
        "reportFunctionMemberAccess": True,
        "reportPrivateUsage": True,
        "reportUnusedImport": True,
        "reportUnusedClass": True,
        "reportUnusedFunction": True,
        "reportUnusedVariable": True,
        "reportDuplicateImport": True,
        "reportUnnecessaryTypeIgnoreComment": True,
    }

    npx_path = shutil.which("npx")
    if not npx_path:
        print("Error: 'npx' not found")
        return

    filepath = Path(sys.argv[1]).stem

    text =  f"Python:   {sys.version}\n"
    text += f"Platform: {platform.platform()}\n"
    text += f"Date:     {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n"
    text += f"Path:     {BASE_PATH}\n"
    text += "\n"

    text += "PyRight settings:\n"
    for key, value in settings.items():
        text += f" - {key}: {value}\n"

    config = "tmp.json"
    with open(config, "w") as config_file:
        json.dump(settings, config_file)

    try:
        result = subprocess.run([npx_path, "pyright", target_file, "--project", config], capture_output=True, text=True, shell=True)
    finally:
        os.remove(config)

    path = str(BASE_PATH)[0].lower() + str(BASE_PATH)[1:]

    stdout = result.stdout.encode("cp1252").decode("utf-8")
    for line in stdout.splitlines():
        if line.startswith("  "):
            if path in line:
                text += line[3 + len(str(BASE_PATH)):] + "\n"
            else:
                text += " - " + line[4:] + "\n"
        else:
            if "informations" in line:
                summary = line.strip()
                text += f"\n{summary}\n"
            else:
                text += "\n"
            #     text += line + "\n"

    with open(f"__pyright-{filepath}.txt", "w") as file:
        file.write(text)

    print(f"[PyRight] {target_file}: {summary} -> __pyright-{filepath}.txt")

    sys.exit(result.returncode)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: __pyright.py <target_file>")
        sys.exit(1)

    run_pyright(sys.argv[1])
