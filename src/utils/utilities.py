"""
    © Jürgen Schoenemeyer, 25.02.2025 15:45

    src/utils/utilities.py

    PUBLIC:
     - clean_import_json(text: str) -> str | bool
     - check_html(text_id: str, text: str) -> None
     - exception(function: Callable[[Any], Any]) -> Callable[[Any], Any]
     - check_url(url: str) -> bool
     - insert_meta_node(data: Dict[Any, Any], in_type: str, language: str | None = None) -> None
     - insert_data_node(data: Dict[Any, Any], paths: List[str], key: str, value: Any) -> None
     - prepare_smart_sort(text:str, count:int = 6) -> str
"""
from __future__ import annotations

import functools
import re
import sys
import traceback
from typing import Any, Callable, Dict, List

from utils.prefs import Prefs
from utils.trace import Trace


def clean_import_json(text: str) -> str | bool:
    # mutiple space -> single space
    # _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    # text = _RE_COMBINE_WHITESPACE.sub(" ", text).strip()

    text = str(text)

    text = " ".join(text.split("  ")) # schnellste Lösung
    text = "<br>".join(text.split(" <br>"))
    text = "<br>".join(text.split("<br> "))

    #text = text.replace("_x000D_", "")

    #text = text.replace("[b]", "<b>")
    #text = text.replace("[/b]", "</b>2)
    #text = text.replace("[br]", "<br>")

    if '"' in text:
        Trace.warning( f'wrong quote >"<: {text}')

    text = text.replace("[nbsp]",   "&#160;")
    text = text.replace("[zerosp]", "&#8203;") # Zero white space
    text = text.replace('"', '\\"')

    text = text.strip()

    if text.lower() == "false":
        return False

    elif text.lower() == "true":
        return True

    else:
        return text

def check_html(text_id: str, text: str) -> None:
    if len(text.split("[b]")) > 1:
        start_bold_number = len(text.split("[b]"))
        end_bold_number = len(text.split("[/b]"))

        if start_bold_number != end_bold_number:
            Trace.error(f"text {text_id} - [b] + [/b] different ('{start_bold_number}  + {end_bold_number}')")

# http://www.blog.pythonlibrary.org/2016/06/09/python-how-to-create-an-exception-logging-decorator/
# https://stackoverflow.com/questions/14527819/traceback-shows-up-until-decorator

def exception(function: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except Exception:
            Trace.exception( "".join(traceback.format_exception(*sys.exc_info())))
            raise
    return wrapper

# https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
# https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45

def check_url(url: str) -> bool:
    # regex = re.compile(
    #     r"^(?:http|ftp)s?://"                  # http:// or https://
    #     r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|" #domain...
    #     r"localhost|" #localhost...
    #     r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" # ...or ip
    #     r"(?::\d+)?"                           # optional port
    #     r"(?:/?|[/?]\S+)$", re.IGNORECASE
    # )

    regex = re.compile(r"""
        ^(?:http|ftp)s?://
        (?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|
        localhost|
        \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
        (?::\d+)?
        (?:/?|[/?]\S+)$
    """, re.IGNORECASE | re.VERBOSE)


    ret = re.match(regex, url) is not None
    return ret

def insert_meta_node(data: Dict[Any, Any], in_type: str, language: str | None = None) -> None:
    if ".meta" not in data:
        data[".meta"] = {}

    data[".meta"]["type"] = in_type
    if language:
        data[".meta"]["language"] = language

    data[".meta"]["company"]   = Prefs.get("eventCompany")
    data[".meta"]["eventType"] = Prefs.get("eventType")
    data[".meta"]["eventID"]   = Prefs.get("eventID")
    data[".meta"]["eventName"] = Prefs.get("eventName")
    data[".meta"]["font"]      = Prefs.get("eventFont")

def insert_data_node(data: Dict[Any, Any], paths: List[str], key: str, value: Any) -> None:
    curr_node: Dict[Any, Any] = data

    for node in paths:
        if node not in curr_node:
            curr_node[node] = {}
        curr_node = curr_node[node]

    curr_node[key] = value

def prepare_smart_sort(text:str, count:int = 6) -> str:

    # normalize, e.g. chars ä -> a, Ö -> o
    # insert leading zeros for every number block

    # Slider3testÄÖÜäöü4 -> slider3testaouaou4   -> ["slider",  "3", "testaouaou",  "4"] -> slider000003testaouaou000004
    # ggf. toDo defined sequence e.g. oöòóôõ: o -> o[0], ö -> o[1],  ò -> o[2] ...

    # Slider3testÄÖÜäöü4

    text = text.lower()
    text = re.sub(r"[äàáâãå]", "a", text)
    text = re.sub(r"[ëèéê]",   "e", text)
    text = re.sub(r"[ïìíî]",   "i", text)
    text = re.sub(r"[öòóôõ]",  "o", text)
    text = re.sub(r"[üùúû]",   "u", text)
    text = re.sub(r"[ç]",      "c", text)
    text = re.sub(r"[ñ]",      "n", text)

    # slider3testaouaou4

    split: List[str] = []
    tmp = ""
    num = None
    for char in text:
        if char.isdigit():
            tmp = char
            num = True
        else:
            if num is False:
                tmp += char
            elif num is True:
                split.append(tmp)
                tmp = char
            else:
                tmp = char
            num = False

    if tmp != "":
        split.append(tmp)

    # ["slider",  "3", "testaouaou",  "4"]

    split_smart: List[Any] = []
    for entry in split:
        if entry[0].isdigit():
            split_smart.append(entry.zfill(count))
        else:
            split_smart.append(entry)

    ret = "".join(split_smart)

    # slider000003testaouaou000004

    if "." in ret: # built-in var
        ret = "." + ret

    Trace.info( f"sort normalized '{text}' -> '{ret}'")
    return ret
