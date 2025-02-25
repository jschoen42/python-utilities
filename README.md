## list of utilities

| File         | Last update | Note      |
| :----------- | :---------: | :-------: |
| audio.py     | 22.02.2025  | |
| beautify.py  | 22.02.2025  | |
| decorator.py | 22.02.2025  | |
| excel.py     | 22.02.2025  | |
| file.py      | 22.02.2025  | |
| files.py     | 22.02.2025  | rustedpy  |
| format.py    | 22.02.2025  | |
| globals.py   | 22.02.2025  | |
| log.py       | 22.02.2025  | |
| metadata.py  | 22.02.2025  | |
| metadata_mutagen.py | 22.02.2025 | |
| pandas.py    | 22.02.2025  | |
| result.py    | 22.02.2025  | rustedpy   |
| prefs.py     | 22.02.2025  | |
| text.py      | 22.02.2025  | |
| trace.py     | 24.02.2025  | |
| util.py      | 22.02.2025  | |
| utilities.py | 22.02.2025  | |
| utils.py     | 22.02.2025  | |
| xml.py       | 22.02.2025  | |
| zip.py       | 22.02.2025  | |

### src/utils/audio.py

``` python
- split_audio(source_path: Path | str, dest_path: Path | str, filename: str, ffmpeg: str) -> None
- convert_to_mp3(source_path: Path | str, dest_path: Path | str, filename: str, sampling: int, channels: int, ffmpeg: str) -> None
- convert_to_wav(source_path: Path | str, dest_path: Path | str, filename: str, sampling: int, channels: int, ffmpeg: str) -> None
- convert_to_flac(source_path: Path | str, dest_path: Path | str, filename: str, sampling: int, channels: int, ffmpeg: str) -> None
- filter_to_wav(source_path: Path | str, dest_path: Path | str, filename: str, sampling: int, channels: int, ffmpeg: str, filter_path: str, filter_name: str) -> None
```

### src/utils/beautify.py ("JS" | "CSS" | "JSON" | "XML")

``` python
- beautify_file(file_type: str, source_path: Path | str, source_filename: str, dest_path: Path | str, dest_filename: str) -> bool
```

### src/utils/decorator.py

``` python
- @duration(text: str=None, rounds: int=1)
- @deprecated(message: str="")
```

### src/utils/excel.py

``` python
- check_excel_file_exists(filepath: Path | str) -> bool

- read_excel_file(folderpath: Path | str, filename: str) -> None | Tuple[Workbook, float]
- read_excel_worksheet(folderpath: str, filename: str, sheet_name: str) -> None | Tuple[Worksheet, float]
- get_excel_worksheet(workbook: Workbook, sheet_name: str) -> None | Worksheet

- get_cell_text(in_cell: Cell | MergedCell) -> str:
- get_cell_value(in_cell: Cell | MergedCell, check_boolean: bool = True) -> bool | str

- check_hidden_rows_columns(sheet: Worksheet) -> None
- check_single_quotes(wb_name: str, cell_text: str, line_number: int, function_name: str) -> Tuple[bool, str]
- check_double_quotes(wb_name: str, cell_text: str, line_number: int, function_name: str) -> Tuple[bool, str]

- excel_date(date: datetime, time_zone_offset: tzoffset) -> float
- convert_datetime(time_string: str) -> int
- seconds_to_timecode_excel(x: float) -> str
```

### src/utils/file.py

``` python
- get_modification_timestamp(filename: Path | str) -> float
- set_modification_timestamp(filename: Path | str, timestamp: float) -> None

- check_path_exists(path: str) -> bool
- check_file_exists(filepath: Path | str, filename: str) -> bool

- listdir(path: Path | str) -> Tuple[List[str], List[str]]
- listdir_match_extention(path: Path | str, extensions: List[str] | None = None) -> Tuple[List[str], List[str]]

- list_folders(path: Path | str) -> List[str]:
- clear_folder(path: Path | str) -> None:
- delete_folder_tree(dest_path: Path | str, relax: bool = False) -> bool:
- create_folder(folderpath: Path | str) -> bool:
- make_dir(path: Path | str) -> None:
- delete_file(path: Path | str, filename: str) -> bool:
- beautify_path(path: Path | str) -> str:

- get_trace_path(filepath: Path | str) -> str:
- get_files_in_folder(path: Path) -> List[str]
- get_folders_in_folder(path: Path) -> List[str]
- get_save_filename(path: Path, stem: str, suffix: str) -> str

- import_text(folderpath: Path | str, filename: Path | str, encoding: str="utf-8", show_error: bool=True) -> str | None
- import_json(folderpath: Path | str, filename: str, show_error: bool=True) -> Any
- import_json_timestamp(folderpath: Path | str, filename: str, show_error: bool=True) -> Tuple[Any, float | None]

- export_text(folderpath: Path | str, filename: str, text: str, encoding: str="utf-8", newline: str="\n", timestamp: float=0.0, create_new_folder: bool=True, show_message: bool=True) -> str | None:
- export_json(folderpath: Path | str, filename: str, data: Dict[str, Any] | List[Any], newline: str="\n", timestamp: float=0.0, show_message: bool=True) -> str | None:
- export_binary_file(filepath: Path | str, filename: str, data: bytes, _timestamp: float=0, create_new_folder: bool=False) -> None

- export_file(filepath: Path | str, filename: str, text: str, in_type: str | None = None, encoding: str ="utf-8", newline: str="\n", timestamp: float=0.0, create_new_folder: bool=True, overwrite: bool=True) -> None | str

- get_filename_unique(dirpath: Path, filename: str) -> str
- find_matching_file(path_name: str) -> bool | str
- find_matching_file_path(dirname: Path, filename: str) -> Path | bool
- get_valid_filename(name: str) -> str
- get_file_infos(path: Path | str, filename: str, _in_type: str) -> None | Dict

- copy_my_file(source: str, dest: str, _show_updated: bool) -> bool
```

### src/utils/files.py

``` python
- result = get_timestamp(filepath: Path | str) -> Result[float, str]
- result = set_timestamp(filepath: Path | str, timestamp: float) -> Result[(), str]

- result = get_files_dirs(path: str, extensions: List) -> Result[Tuple[List, List], str]

- result = read_file(filepath: Path | str, encoding: str="utf-8") -> Result[Any, str]
- result = write_file(filepath: Path | str, data: Any, encoding: str="utf-8", create_dir: bool = True, show_message: bool=True) -> Result[str, str]
```

### src/utils/format.py

``` python
- floor(number: float, decimals: int=2) -> int

- convert_date_time(time_string: str) -> int

- format_bytes(size: int, unit: str) -> str
- format_bytes_v2(size: int) -> str

- convert_duration(duration: int) -> str

- bin_nibble_null(val: int) -> str
- bin_nibble(val: int) -> str

- to_bool(in_text: str) -> bool
- str_to_bool(value: str) -> bool
```

### src/utils/globals.py

``` python
- DRIVE: Path
- BASE_PATH: Path
- SYSTEM_ENV_PATHS: List[str]
```

### src/utils/log.py

``` python
- log_clear()
- log_add(mediafile: str, text: str, corrected_details: List[Dict], last_segment_text: str, repetition_error: List[Dict], pause_error: List[Dict], spelling_failed: List[Dict]) -> None:
- log_get_data() -> Tuple[str, str]
```

### src/utils/metadata (MediaInfo)

``` python
- get_media_info(filepath: str | BytesIO) -> None | Dict[str, int | float]
- get_audio_duration(filepath: str | BytesIO) -> float:
- get_media_trackinfo(filepath: str | BytesIO) -> None | Dict[str, Any]
- get_video_metadata(filepath: str | BytesIO) -> None | Dict[str, Any]
- get_audio_metadata(filepath: str | BytesIO) -> None | Dict[str, Any]
```

### src/utils/metadata_mutagen.py

``` python
- def get_audioinfo_mutagen(filepath: str) -> None | Dict[str, Any]
- get_audio_metadata_mutagen(filepath: Path | str) -> None | Dict[str, Any]
- get_video_metadata_mutagen(filepath: Path | str) -> None | Dict[str, Any]
```

### src/utils/pandas.py

``` python
- load_data(filepath:Path | str, filename:str, sheet_name:str = "", key:str = "") -> Any:
- save_data(filepath:str, filename:str, data:Any, sheet_name:str = "Sheet1", key:str = "") -> None:
```

### src/utils/result.py

``` python
- is_ok(result: Result[T, E]) -> bool:
- is_err(result: Result[T, E]) -> bool:
- unwrap_ok(result: Result[T, E]) -> T:
- unwrap_err(result: Result[T, E]) -> E:
```

### src/utils/prefs.py

``` python
class Prefs:
- init(cls, pref_path = None, pref_prefix = None) -> None
- load(cls, pref_name: str) -> bool
- get(cls, key_path: str) -> Any

- merge_dicts(a: Dict, b: Dict) -> Dict
- build_tree(tree: List, in_key: str, value: str) -> Dict
```

### src/utils/text.py

``` python
- check_quote(test_id: str, text: None | str, language: str) -> str
```

### src/utils/trace.py

``` python
class Trace:
- Trace.set(debug_mode=True)
- Trace.set(reduced_mode=True)
- Trace.set(color=False)
- Trace.set(timezone=False)
- Trace.set(timezone="Europe/Berlin") # "UTC", "America/New_York"
- Trace.set(show_caller=False)
- Trace.set(appl_folder="/trace/")

- Trace.file_init(["action", "result", "warning", "error"], csv=False)
- Trace.file_save("./logs", "testTrace")

- Trace.redirect(function) # -> e.g. qDebug (PySide6)

- Trace.action()
- Trace.result()
- Trace.info()     # not in reduced mode
- Trace.update()   # not in reduced mode
- Trace.download() # not in reduced mode
- Trace.warning()
- Trace.error()
- Trace.exception()
- Trace.fatal()
- Trace.debug()    # only in debug mode
- Trace.wait()     # only in debug mode

class Color:
- Color.<color_name>
- Color.clear(text: str) -> str:

### src/utils/util.py

``` python
- format_subtitle(start_time: float, end_time: float, text: str, color=True) -> str
- format_timestamp(seconds: float, always_include_hours: bool=False, decimal_marker: str=".", fps: float = 30) -> str

class CacheJSON:
- CacheJSON.init(path: Path | str, name: str, model: str, reset: bool)
- CacheJSON.get(self, value_hash: str) -> Dict | None
- CacheJSON.add(self, value_hash: str, value: Dict) -> None
- CacheJSON.flush(self) -> None:

class ProcessLog (array cache)
- ProcessLog.init()
- ProcessLog.add(info: str)
- ProcessLog.get() -> List[str]
```

### src/utils/utils.py

``` python
- camel_to_snake(name: str) -> str
- snake_to_camel(name: str) -> str
- pascal_to_snake(name: str) -> str
- snake_to_pascal(name: str) -> str
```

### src/utils/utilities.py

``` python
- clean_import_json(text: str) -> str | bool
- check_html(text_id: str, text: str) -> None
- exception(function: Callable[[Any], Any]) -> Callable[[Any], Any]
- check_url(url: str) -> bool
- insert_meta_node(data: Dict[Any, Any], in_type: str, language: str | None = None) -> None
- insert_data_node(data: Dict[Any, Any], paths: List[str], key: str, value: Any) -> None
- prepare_smart_sort(text:str, count:int = 6) -> str
```

### src/utils/xml.py

``` python
- open_xml_as_dict(myzip: ZipFile, path: str) -> Dict[str, Any] | None
```

### src/utils/zip.py

``` python
- check_zip(in_zip, path: str, files: List) -> Dict[str]
- expand_zip(source_path: str, dest_path: str) -> bool
- create_zip(source_path: str, dest_path: str, filename: str, compression = 6) -> bool
```
