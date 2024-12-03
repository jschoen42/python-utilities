"""
    (c) Jürgen Schoenemeyer, 03.12.2024

    PUBLIC:
    class Prefs:
        init(cls, pref_path = None, pref_prefix = None ) -> None
        read(cls, pref_name: str) -> bool
        get(cls, key_path: str, default: any = None) -> any

    merge_dicts(dict1: dict, dict2: dict) -> dict
    build_tree(tree: list, in_key: str, value: str) -> dict
"""
import sys
import json
import re

from json    import JSONDecodeError
from pathlib import Path

import yaml

from src.utils.trace import Trace
from src.utils.file  import beautify_path

BASE_PATH = Path(sys.argv[0]).parent

class Prefs:
    pref_path   = BASE_PATH / "prefs"
    pref_prefix = ""
    data = {}

    @classmethod
    def init(cls, pref_path = None, pref_prefix = None ) -> None:
        if pref_path is not None:
            cls.pref_path = BASE_PATH / pref_path
        if pref_prefix is not None:
            cls.pref_prefix = pref_prefix
        cls.data = {}

    @classmethod
    def read(cls, pref_name: str) -> bool:
        ext = Path(pref_name).suffix
        if ext not in [".yaml", ".yml"]:
            Trace.error(f"'{ext}' not supported")
            return False

        pref_name = cls.pref_prefix + pref_name
        if not Path(cls.pref_path, pref_name).is_file():
            Trace.error(f"pref not found '{pref_name}'")
            return False
        try:
            with open( Path(cls.pref_path, pref_name), "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)

            cls.data = dict(merge_dicts(cls.data, data))

        except yaml.scanner.ScannerError as err:
            Trace.fatal(f"{pref_name}:\n{err}")

        except OSError as err:
            Trace.error(f"{pref_name}: {err}")
            return False

        return True

    @classmethod
    def get_all(cls) -> dict:
        return cls.data

    @classmethod
    def get(cls, key: str, default: any = None) -> any:

        def get_pref_key(key: str) -> any:
            data = cls.data

            if key in data:
                return data[key]

            elif default:
                Trace.warning(f"unknown key '{key}' -> default value '{default}'")
                return default
            else:
                Trace.fatal(f"unknown pref: {key}")

        result = get_pref_key(key)

        # pref.yaml
        #   filename:  'data.xlsx'
        #   filepaths: ['..\result\{{filename}}']
        #
        # -> filepaths = ['..\result\data.xlsx']

        # dict -> text -> replace -> dict

        tmp = json.dumps(result)

        pattern = r'\{\{([^\}]+)\}\}' # '{{ ... }}'
        replace = re.findall(pattern, tmp)
        if len(replace)==0:
            return result

        for entry in replace:
            tmp = tmp.replace("{{" + entry + "}}", get_pref_key(entry))

        try:
            ret = json.loads(tmp)
        except JSONDecodeError as err:
            Trace.error(f"json error: {key} -> {tmp} ({err})")
            ret = ''

        return ret


def get_pref_special(pref_path: Path, pref_prexix, pref_name: str, key: str) -> str:
    try:
        with open(Path(pref_path, pref_prexix + pref_name + ".yaml"), 'r', encoding="utf-8") as file:
            pref = yaml.safe_load(file)
    except OSError as err:
        Trace.error(f"{beautify_path(err)}")
        return ""

    if key in pref:
        return pref[key]
    else:
        Trace.error(f"unknown pref: {pref_name} / {key}")
        return ""

def read_pref( pref_path: Path, pref_name: str ) -> tuple[bool, dict]:
    try:
        with open( Path(pref_path, pref_name), 'r', encoding="utf-8") as file:
            data = yaml.safe_load(file)

        # Trace.wait( f"{pref_name}: {json.dumps(data, sort_keys=True, indent=2)}" )
        return False, data

    except OSError as err:
        Trace.error( f"{beautify_path(err)}" )
        return True, {}

# https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries

def merge_dicts(dict1: dict, dict2: dict) -> any:
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_dicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])

def build_tree(tree: list, in_key: str, value: str) -> dict:
    if tree:
        return {tree[0]: build_tree(tree[1:], in_key, value)}

    return { in_key: value }
