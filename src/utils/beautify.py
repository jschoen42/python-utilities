"""
    © Jürgen Schoenemeyer, 21.06.2025 13:47

    src/utils/beautify.py

    PUBLIC:
     - beautify_css( text: str ) -> str
     - beautify_js( text: str ) -> str
     - beautify_file(file_type: str, source_path: Path | str, source_filename: str, dest_path: Path | str, dest_filename: str) -> bool:
        - file_type = "JS" | "CSS" | "JSON" | "XML"

    PRIVATE:
     - expand_js(text: str) -> str:
     - expand_css(text: str) -> str:
"""
from __future__ import annotations

import json

from pathlib import Path
from typing import Dict

import cssbeautifier  # type: ignore[import-untyped, reportMissingTypeStubs]
import jsbeautifier  # type: ignore[import-untyped, reportMissingTypeStubs]

from lxml import etree

from utils.decorator import duration
from utils.file import export_text, import_text
from utils.trace import Trace

expand_data_js: Dict[str, str] = {
    "!0":  "true",
    "!1":  "false",

    " 1e3":  " 1000",
    " 1e4":  " 10000",
    " 1e5":  " 100000",
    " 1e6":  " 1000000",
    " 1e7":  " 10000000",
    " 1e8":  " 100000000",
    " 1e9":  " 1000000000",
    " 1e10": " 10000000000",
    " 1e11": " 100000000000",
    " 1e12": " 1000000000000",
    " 1e13": " 10000000000000",
    " 1e14": " 100000000000000",
    " 1e15": " 1000000000000000",
    " 1e16": " 10000000000000000",

    "(1e3":  "(1000",
    "(1e4":  "(10000",
    "(1e5":  "(100000",
    "(1e6":  "(1000000",
    "(1e7":  "(10000000",
    "(1e8":  "(100000000",
    "(1e9":  "(1000000000",
    "(1e10": "(10000000000",
    "(1e11": "(100000000000",
    "(1e12": "(1000000000000",
    "(1e13": "(10000000000000",
    "(1e14": "(100000000000000",
    "(1e15": "(1000000000000000",
    "(1e16": "(10000000000000000",

    "[1e3":  "[1000",
    "[1e4":  "[10000",
    "[1e5":  "[100000",
    "[1e6":  "[1000000",
    "[1e7":  "[10000000",
    "[1e8":  "[100000000",
    "[1e9":  "[1000000000",
    "[1e10": "[10000000000",
    "[1e11": "[100000000000",
    "[1e12": "[1000000000000",
    "[1e13": "[10000000000000",
    "[1e14": "[100000000000000",
    "[1e15": "[1000000000000000",
    "[1e16": "[10000000000000000",

    "/1e3":  "/1000",
    "/1e4":  "/10000",
    "/1e5":  "/100000",
    "/1e6":  "/1000000",
    "/1e7":  "/10000000",
    "/1e8":  "/100000000",
    "/1e9":  "/1000000000",
    "/1e10": "/10000000000",
    "/1e11": "/100000000000",
    "/1e12": "/1000000000000",
    "/1e13": "/10000000000000",
    "/1e14": "/100000000000000",
    "/1e15": "/1000000000000000",
    "/1e16": "/10000000000000000",

    " -1e3":  " -1000",
    " -1e4":  " -10000",
    " -1e5":  " -100000",
    " -1e6":  " -1000000",
    " -1e7":  " -10000000",
    " -1e8":  " -100000000",
    " -1e9":  " -1000000000",
    " -1e10": " -10000000000",
    " -1e11": " -100000000000",
    " -1e12": " -1000000000000",
    " -1e13": " -10000000000000",
    " -1e14": " -100000000000000",
    " -1e15": " -1000000000000000",
    " -1e16": " -10000000000000000",

    " -2e3":  " -2000",
    " -4e3":  " -4000",
    " -8e3":  " -8000",

    " 4e3": " 4000",
    " 8e3": " 8000",

    " 31e3":  " 31000",
    " 6e4":   " 60000",
    " 36e4":  " 360000",
    " 36e5":  " 3600000",
    " 108e5": " 108000000",
    " 36e9":  " 36000000000",

    "(31e3":  "(31000",
    "(6e4":   "(60000",
    "(36e4":  "(360000",
    "(36e5":  "(3600000",
    "(108e5": "(108000000",
    "(36e9":  "(36000000000",

    "/31e3":  "/31000",
    "/6e4":   "/60000",
    "/36e4":  "/360000",
    "/36e5":  "/3600000",
    "/108e5": "/108000000",
    "/36e9":  "/36000000000",

    "~~(": "Math.floor(",
}

expand_data_css: Dict[str, str] = {
    ">":      " > ",
    "  >  ":  " > ",

    "\n  }": ";\n  }",
    "\n}":   ";\n}",
    ";  ;":  ";",
    ";;":    ";",

    "};":    "}",
}

def expand_js(text: str) -> str:
    for key, value in expand_data_js.items():
        text = text.replace(key, value)
    return text

def expand_css(text: str) -> str:
    for key, value in expand_data_css.items():
        text = text.replace(key, value)
    return text

def beautify_css( text: str ) -> str:
    """
        default_options.brace_style = 'collapse'
        default_options.end_with_newline = false
        default_options.indent_char = ' '
        default_options.indent_size = 4
        default_options.newline_between_rules = false
        default_options.preserve_newlines = false
        default_options.selector_separator_newline = true
        default_options.space_around_combinator = false
        default_options.space_around_selector_separator = false
    """
    opts = cssbeautifier.default_options()
    opts.indent_size = 2
    return expand_css(cssbeautifier.beautify(text, opts))

def beautify_js( text: str ) -> str:
    """
        default_options.break_chained_methods = false
        default_options.eol = '\n'
        default_options.indent_char = ' '
        default_options.indent_level = 0
        default_options.indent_size = 4
        default_options.jslint_happy = false
        default_options.preserve_newlines = true
    """
    opts = jsbeautifier.default_options()
    opts.indent_size = 2
    data = expand_js(jsbeautifier.beautify(text, opts))
    return data

@duration("beautify '{1}\\{2}'")
def beautify_file(file_type: str, source_path: Path | str, source_filename: str, dest_path: Path | str, dest_filename: str) -> bool:
    source = Path(source_path) / source_filename
    dest   = Path(dest_path) / dest_filename

    text = import_text(source.parent, source.name)
    if text is None:
        return False

    mtime = source.stat().st_mtime

    if file_type == "JS":
        """
            default_options.break_chained_methods = false
            default_options.eol = '\n'
            default_options.indent_char = ' '
            default_options.indent_level = 0
            default_options.indent_size = 4
            default_options.jslint_happy = false
            default_options.preserve_newlines = true
        """
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        data = expand_js(jsbeautifier.beautify(text, opts))

    elif file_type == "CSS":
        """
            default_options.brace_style = 'collapse'
            default_options.end_with_newline = false
            default_options.indent_char = ' '
            default_options.indent_size = 4
            default_options.newline_between_rules = false
            default_options.preserve_newlines = false
            default_options.selector_separator_newline = true
            default_options.space_around_combinator = false
            default_options.space_around_selector_separator = false
        """
        opts = cssbeautifier.default_options()
        opts.indent_size = 2
        data = expand_css(cssbeautifier.beautify(text, opts))

    elif file_type == "JSON":
        try:
            data = json.dumps(json.loads(text), indent=2, sort_keys=False)
        except ValueError as e:
            Trace.error(f"JSON parse error: {e} - {source}")
            data = text

    elif file_type == "XML":
        try:
            x = etree.fromstring(text)  # noqa: S320
            data = etree.tostring(x, pretty_print=True, encoding=str)
        except ValueError as e:
            Trace.error(f"XML parse error: {e} - {source}")
            data = text

    else:
        Trace.error(f"unknown file type '{file_type}'")
        return False

    if export_text(dest.parent, dest.name, data, timestamp = mtime):
        return True
    else:
        return False
