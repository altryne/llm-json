# llm_json/json.py

import json as _json
import re

__all__ = [
    "dump",
    "dumps",
    "load",
    "loads",
    "JSONDecoder",
    "JSONEncoder",
    "JSONDecodeError",
]

JSONDecodeError = _json.JSONDecodeError
JSONDecoder = _json.JSONDecoder
JSONEncoder = _json.JSONEncoder


def loads(s, *args, **kwargs):
    """
    A drop-in replacement for `json.loads` that also tries to handle
    JSON responses wrapped in markdown code blocks or backticks.
    """
    # Attempt a direct parse first.
    try:
        return _json.loads(s, *args, **kwargs)
    except _json.JSONDecodeError as e:
        # We store the first exception to re-raise if all fallback attempts fail
        fallback_error = e

    # 1) Try triple backtick code blocks (with or without 'json' after the backticks).
    #    We use finditer to allow multiple code blocks in the string.
    triple_code_block_regex = re.compile(
        r"```(?:json)?\s*(.*?)```",
        re.DOTALL | re.IGNORECASE
    )
    for match in triple_code_block_regex.finditer(s):
        snippet = match.group(1).strip()
        try:
            return _json.loads(snippet, *args, **kwargs)
        except _json.JSONDecodeError:
            # If the code block is invalid, keep trying subsequent blocks
            pass

    # 2) If that didn't work, look for inline backtick JSON (like `{"foo":"bar"}`).
    single_backtick_regex = re.compile(r"`([^`]*)`")
    match = single_backtick_regex.search(s)
    if match:
        snippet = match.group(1).strip()
        try:
            return _json.loads(snippet, *args, **kwargs)
        except _json.JSONDecodeError:
            pass

    # If none of the above parsing worked, re-raise the original JSONDecodeError.
    raise fallback_error


def dumps(obj, *args, **kwargs):
    """Drop-in replacement for `json.dumps`."""
    return _json.dumps(obj, *args, **kwargs)


def dump(obj, fp, *args, **kwargs):
    """Drop-in replacement for `json.dump`."""
    return _json.dump(obj, fp, *args, **kwargs)


def load(fp, *args, **kwargs):
    """
    Drop-in replacement for `json.load` that also tries to handle
    JSON responses wrapped in markdown code blocks or backticks.
    """
    data = fp.read()
    return loads(data, *args, **kwargs)