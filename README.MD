# llm-json
[![PyPI version](https://img.shields.io/pypi/v/llm-json)](https://pypi.org/project/llm-json)
[![Build Status](https://github.com/altryne/llm-json/actions/workflows/tests.yml/badge.svg)](https://github.com/altryne/llm-json/actions)
[![Coverage Status](https://coveralls.io/repos/github/altryne/llm-json/badge.svg)](https://coveralls.io/github/altryne/llm-json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**llm-json** is a Python package that acts as a drop-in replacement for the standard \json\ library. It automatically handles JSON strings that are often returned by Large Language Models (LLMs) wrapped in Markdown code fences or backticks—so you don’t have to beg the AI to always produce “valid JSON.”

## Why This Project?
After repeatedly struggling with LLMs returning JSON (but *also* including backticks, code fences, or extraneous text), I got fed up. Structured output is nice, but it’s not always possible (or desirable) to force the LLM to output *perfect* JSON. Rather than overcomplicating prompt engineering, **llm-json** does the messy cleanup for you.

## Installation
Grab the latest release from PyPI:

```bash
uv pip install llm-json
```

## Usage
The core idea is that **llm-json** works exactly like the standard Python `json` library, but with automatic fallback parsing for those pesky backticks:

```python
from llm_json import json

# A string returned by an LLM, might be in triple-backtick code blocks or inline backticks
s = """
```json
{
  "hello": "world"
}
```"""

data = json.loads(s)
print(data)  # => {'hello': 'world'}
```

All other functions (`json.dump`, `json.dumps`, `json.load`) also work the same way. Just replace your existing `import json` with `from llm_json import json`, and you’re good to go.

### Handling Extra Text
**llm-json** will ignore extraneous text before and after the code fences and attempt to parse the first valid snippet it finds. It also handles inline backticks (like \`\`\`{"hello":"world"}\`\`\`).

## Contributing
Pull requests and issues are very welcome! Check out the [GitHub repo](https://github.com/altryne/llm-json) to file issues or propose changes.

## Testing
We use [pytest](https://pytest.org/). To run tests locally:

```bash
git clone https://github.com/altryne/llm-json.git
cd llm-json
pip install -e .
pip install pytest
pytest tests
```

You should see something like:

```
============================= test session starts =============================
platform darwin -- Python 3.x, pytest-8.x, ...
collected 9 items

tests/test_json.py .........                                                 [100%]

============================== 9 passed in 0.02s ==============================
```

## License
This project is licensed under the [MIT License](LICENSE).

## Author
Made with ❤️ by [@altryne](https://x.com/altryne).  
- GitHub: [github.com/altryne](https://github.com/altryne)  
- X (formerly Twitter): [x.com/altryne](https://x.com/altryne)

