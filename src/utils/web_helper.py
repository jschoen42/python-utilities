"""
    © Jürgen Schoenemeyer, 15.07.2025 22:52

    src/utils/web_helper.py

    PUBLIC:
     . parse_url(url: str) -> Tuple[str, str]
     - requests_get_html(url: str) -> Tuple[str, str]
     - requests_head(url: str) -> Tuple[str, int]

"""
from __future__ import annotations

import os

from typing import Any, Dict, List, Tuple
from urllib.parse import parse_qs, urlparse

import requests
import requests.exceptions
import tldextract

from dotenv import load_dotenv

from utils.format import format_bytes_v2
from utils.trace import Trace

def parse_url(url: str) -> Tuple[str, str, str]:
    if urlparse(url).scheme == "":
        Trace.warning(f"upgrade to https '{url}'")
        url = "https://" + url

    parse = urlparse(url)
    scheme = parse.scheme
    if scheme == "http":
        Trace.warning(f"{scheme=}")

    return scheme + "://", parse.netloc, parse.path.rstrip("/")

TIMEOUT = 30
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Priority": "u=3",
    "Connection": "keep-alive",
}

ret = load_dotenv(".env")
if ret is False:
    Trace.fatal( ".env not found" )

credentials = {
    "user": "",
    "password": "",
}

def init_credentials( id: str ) -> None:
    if id == "":
        credentials["user"] = ""
        credentials["password"] = ""
    else:
        cred = os.getenv("CREDENTAILS_" + id)
        if cred and ":" in cred:
            user, password = cred.split(":")
            credentials["user"] = user
            credentials["password"] = password
        else:
            Trace.fatal( f"no valid credentials for '{id}'" )


def requests_get_html(url: str) -> Tuple[str, str]:
    return  requests_get( url, ["text/html", "text/html; charset=utf-8"] )

def requests_get_css(url: str) -> Tuple[str, str]:
    return  requests_get( url, ["text/css", "text/css; charset=utf-8"] )

def requests_get_js(url: str) -> Tuple[str, str]:
    return  requests_get( url, ["application/javascript", "application/javascript; charset=utf-8", "text/javascript", "text/javascript; charset=utf-8"] )

def requests_get(url: str, types: List[str] ) -> Tuple[str, str]:

    if credentials["user"]:
        auth = (credentials["user"], credentials["password"])
    else:
        auth = None

    # step 1: requests.head -> check: domain, content-type

    try:
        response = requests.head(url, auth=auth, headers=HEADERS, allow_redirects=True, timeout=TIMEOUT)
    except requests.exceptions.RequestException as err:
        Trace.error(f"{url}: {err}")
        return f"RequestException: {err}", ""

    if response.status_code in [301, 302]:
        get_url = response.url
        Trace.info(f"redirect to '{get_url}'")
    elif response.status_code == 200:
        get_url = url
    else:
        Trace.error( f"response {response} -- {response.status_code}: {url}" )
        return f"{response.status_code}", ""

    start_host = get_domain(url)
    final_host = get_domain(response.url)
    if start_host != final_host:
        Trace.info(f"redirect to another host '{final_host}'")
        return f"redirect to '{final_host}'", ""

    content_type = response.headers.get("Content-Type")
    if content_type and content_type.lower() not in types:
        Trace.warning(f"href '{url}': content-type '{content_type}' (expected '{types}')")
        return f"unexpected content-type {content_type}", ""

    # step 2: requests.get

    try:
        response = requests.get(get_url, auth=auth, headers=HEADERS, timeout=10)
    except requests.exceptions.RequestException as err:
        Trace.error(f"{err}")
        return f"{err}", ""

    if response.status_code == 200:
        return f"{response.status_code}", response.text
    else:
        Trace.error( f"response {response.status_code}: {url}" )
        return f"{response.status_code}", ""

def requests_head(url: str) -> Tuple[str, int]:

    if credentials["user"]:
        auth = (credentials["user"], credentials["password"])
    else:
        auth = None

    try:
        response = requests.head(url, auth=auth, headers=HEADERS, allow_redirects=True, timeout=TIMEOUT)
    except requests.exceptions.RequestException as err:
        Trace.error(f"{err}")
        return f"{err}", -1

    if response.status_code == 200:
        content_type = response.headers.get("Content-Type")
        if content_type:
            if "text/html" in content_type:
                return "text/html", 0
        else:
           Trace.error( f"content-type missing {url}" )
           content_type = f"none ({url.split(".")[-1]})"

        content_length = response.headers.get("Content-Length")
        if content_length:
            length = int(content_length)
            Trace.info( f"{content_type}: {url} ({format_bytes_v2(length)})" )
            return content_type, length
        else:
            Trace.warning( f"{content_type}: {url} - file size unknown" )
            return content_type, 0

    elif response.status_code == 301:
        for key, value in response.headers.items():
            print(f"{key}: {value}")

        Trace.error( f"response {response.status_code}: {url}" ) # ????
        return f"status_code: {response.status_code}", -1
    else:
        Trace.error( f"response {response.status_code}: {url}" )
        return f"status_code: {response.status_code}", -1

def get_domain(url: str) -> str:
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def read_query(query_string: str) -> Dict[str, Any]:
    return {key: value[0] if len(value) == 1 else value for key, value in parse_qs(query_string.lstrip("?")).items()}
