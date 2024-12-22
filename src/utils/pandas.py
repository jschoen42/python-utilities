"""
    © Jürgen Schoenemeyer, 21.12.2024

    PUBLIC:
      - load_data(filepath:Path | str, filename:str, sheet_name:str = "", key:str = "") -> DataFrame:
      - save_data(filepath:str, filename:str, data:DataFrame, sheet_name:str = "Sheet1", key:str = "") -> None:
"""

import time
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from utils.trace import Trace
from utils.file  import check_file_exists

# https://pandas.pydata.org/docs/user_guide/io.html

##################################################
#
#    pandas: readers
#
#    text:   cvs, xml, json
#    binary: parquet, feather, pickle, HDF5, xlsx
#
###################################################

def load_data(filepath:Path | str, filename:str, sheet_name:str = "", key:str = "") -> DataFrame:

    start_timer = time.time()

    if check_file_exists(filepath, filename) is False:
        Trace.fatal(f"'{filename}' not found")

    data_path = Path(filepath, filename)
    import_type = Path(filename).suffix[1:].lower()

    # text

    if import_type == "csv":
        data_frame = pd.read_csv(data_path)

    elif import_type == "xml":
        data_frame = pd.read_xml(data_path)

    elif import_type == "json":
        data_frame = pd.read_json(data_path)

    # binary

    elif import_type == "feather":
        data_frame = pd.read_feather(data_path)

    elif import_type == "parquet":
        data_frame = pd.read_parquet(data_path)

    elif import_type == "orc":
        data_frame = pd.read_orc(data_path)

    elif import_type == "pkl":
        data_frame = pd.read_pickle(data_path)

    elif import_type == "hdf":
        data_frame = pd.read_hdf(data_path, key=key)

    elif import_type == "xlsx":
        if sheet_name == "":
            data_frame = pd.read_excel(data_path) # first sheet
        else:
            try:
                data_frame = pd.read_excel(data_path, sheet_name=sheet_name)
            except ValueError as err:
                Trace.fatal(f"'{filename}': {err}")
    else:
        Trace.fatal( f"unknown file type '{import_type}'")

    duration = time.time() - start_timer
    Trace.info(f"'{filename}' loaded: {duration:.3f} sec")

    return data_frame

###################################################
#
#    pandas: writers
#
#    text:   cvs, xml, json, html
#    binary: parquet, feather, pickle, HDF5, xlsx
#
####################################################

def save_data(filepath:str, filename:str, data:DataFrame, sheet_name:str = "Sheet1", key:str = "") -> None:

    start_timer = time.time()

    data_path = Path(filepath, filename)
    export_type = Path(filename).suffix[1:].lower()

    # text

    if export_type == "csv":
        data.to_csv(data_path)

    elif export_type == "xml":
        data.to_xml(data_path)

    elif export_type == "json":
        data.to_json(data_path)

    elif export_type == "html":
        data.to_html(data_path)

    # binary

    elif export_type == "parquet":
        data.to_parquet(data_path)

    elif export_type == "feather":
        data.to_feather(data_path)

    elif export_type == "orc":
        data.to_orc(data_path)

    elif export_type == "pkl":
        data.to_pickle(data_path)

    elif export_type == "hdf":
        data.to_hdf(data_path, key=key)

    elif export_type == "xlsx":
        data.to_excel(data_path, sheet_name=sheet_name)

    else:
        Trace.fatal( f"unknown file type '{export_type}'")

    duration = time.time() - start_timer
    Trace.info(f"'{filename}' saved: {duration:.3f} sec")
