import codecs
import json
import os
from datetime import datetime
from pathlib import Path


def make_session_id() -> str:
    return f"{datetime.now():%y%m%d%H%M%S}"


def read_json(path: Path | os.PathLike[str] | str) -> list | dict:
    with codecs.open(path, "r", encoding="utf8") as file:
        return json.load(file)


def try_parse_json(text: str | None) -> str | None:
    if not text:
        return None
    if not text.startswith("{"):
        return None
    if not text.endswith("}"):
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def try_parse_int(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None


def pretty_line(text: str, cut_count: int = 100) -> str:
    if len(text) > 100:
        text_cut = text[:cut_count]
        size = len(text)
        text_pretty = f'{text_cut}..(total {size} characters)'
    else:
        text_pretty = text
    text_pretty = text_pretty.replace('\n', '\\n')
    return text_pretty
