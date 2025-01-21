import pytest
from llm_json import json  # Our custom wrapper

def test_pure_json():
    """Test that pure valid JSON is parsed normally."""
    s = '{"a": 1, "b": [2, 3], "c": null}'
    data = json.loads(s)
    assert data == {"a": 1, "b": [2, 3], "c": None}

def test_valid_code_block():
    """Test that triple-backtick code block with 'json' fence is correctly parsed."""
    s = """
    ```json
    {
      "b": 2
    }
    ```
    """
    data = json.loads(s)
    assert data == {"b": 2}

def test_valid_code_block_no_json_identifier():
    """Test that triple-backtick code block without 'json' in the fence is also handled."""
    s = """
    ```
    {
      "c": true
    }
    ```
    """
    data = json.loads(s)
    assert data == {"c": True}

def test_inline_backticks():
    """Test that inline backticks containing valid JSON are parsed."""
    s = "Here's the data: `{\"foo\": \"bar\"}` End of message."
    data = json.loads(s)
    assert data == {"foo": "bar"}

def test_extra_text_around_code_block():
    """Test that extra text around the JSON code block doesn't break parsing."""
    s = """
    Here is some info:

    ```json
    {
      "nested": {
        "hello": "world"
      }
    }
    ```

    Hope that helps!
    """
    data = json.loads(s)
    assert data == {"nested": {"hello": "world"}}

def test_multiple_code_blocks():
    """Test that if there are multiple code blocks, it parses the first valid one."""
    s = """
    ```json
    invalid json block
    ```
    Another block:
    ```json
    {
      "ok": 123
    }
    ```
    """
    data = json.loads(s)
    # We expect it to fail on the first code block, but succeed on the second.
    assert data == {"ok": 123}

def test_invalid_json_raises():
    """Test that invalid JSON (with no valid fallback) raises JSONDecodeError."""
    s = "Not even close to JSON."
    with pytest.raises(json.JSONDecodeError):
        json.loads(s)

def test_partial_valid_json_raises():
    """Test that partial or invalid JSON inside code block also raises JSONDecodeError."""
    s = """
    ```json
    { "foo": "bar", }
    ```
    """
    # There's a trailing comma which is invalid in standard JSON
    with pytest.raises(json.JSONDecodeError):
        json.loads(s)

def test_dump_and_dumps():
    """Test that dump/dumps work the same as the standard json library."""
    obj = {"hello": "world", "numbers": [1, 2, 3]}
    s = json.dumps(obj)
    assert '"hello": "world"' in s
    assert '"numbers": [1, 2, 3]' in s

    # Also verify dump() by writing to a temporary file
    import io
    buf = io.StringIO()
    json.dump(obj, buf)
    buf.seek(0)
    dumped_str = buf.read()
    assert '"hello": "world"' in dumped_str
    assert '"numbers": [1, 2, 3]' in dumped_str
