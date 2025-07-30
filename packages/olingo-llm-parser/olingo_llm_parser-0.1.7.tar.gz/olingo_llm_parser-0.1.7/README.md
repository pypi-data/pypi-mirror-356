# 🤖 Olingo LLM Parser

> **Elegant Jinja2-based chat template parser for AI applications**

[![PyPI version](https://badge.fury.io/py/olingo-llm-parser.svg)](https://badge.fury.io/py/olingo-llm-parser)
[![Python Support](https://img.shields.io/pypi/pyversions/olingo-llm-parser.svg)](https://pypi.org/project/olingo-llm-parser/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Transform your Jinja2 templates into structured chat conversations for OpenAI API spec. Perfect for OpenAI, Anthropic, and other chat-based language models.

## ✨ Features

- 🎯 **Simple & Elegant**: Clean syntax with custom `{% chat %}` blocks
- 🔧 **Jinja2 Powered**: Full support for variables, loops, conditionals
- 📋 **Schema Integration**: Automatic JSON schema loading for structured responses
- 🚀 **AI Ready**: Perfect for OpenAI, Anthropic, and other chat APIs
- 🎨 **Flexible**: Use anywhere - scripts, web apps, AI agents
- 📦 **Minimal Dependencies**: Just Jinja2, nothing else

## 🚀 Quick Start

### Installation

```bash
pip install olingo-llm-parser
```

### Basic Usage

**1. Create a template (`chat_template.jinja`):**

```jinja2
{% chat role="system" %}
You are a helpful AI assistant specializing in {{ domain }}.
{% endchat %}

{% chat role="user" %}
{{ user_question }}
{% endchat %}
```

**2. Parse and use:**

```python
from olingo_llm_parser import parse_chat_template

# Parse template with variables
messages = parse_chat_template("chat_template.jinja", {
    "domain": "data science",
    "user_question": "What is machine learning?"
})

# Use with OpenAI
import openai
response = openai.chat.completions.create(
    model="gpt-4",
    messages=messages
)
```

**Output:**
```python
[
    {"role": "system", "content": "You are a helpful AI assistant specializing in data science."},
    {"role": "user", "content": "What is machine learning?"}
]
```

## 🎨 Advanced Examples

### With Loops and Conditions

```jinja2
{% chat role="system" %}
You are an expert {{ role }}.
{% endchat %}

{% for example in examples %}
{% chat role="user" %}
Example: {{ example.question }}
{% endchat %}

{% chat role="assistant" %}
{{ example.answer }}
{% endchat %}
{% endfor %}

{% chat role="user" %}
Now answer: {{ final_question }}
{% endchat %}
```

### With JSON Schema

```python
from olingo_llm_parser import parse_template_and_schema

# Parse both template and schema from files
messages, response_format = parse_template_and_schema(
    template="template.jinja",
    schema="response_schema.json",
    variables={"topic": "AI"}
)

# Or use strings/dictionaries directly
template_string = """{% chat role="system" %}
You are an expert on {{ topic }}.
{% endchat %}"""

schema_dict = {"type": "object", "properties": {"answer": {"type": "string"}}}

messages, response_format = parse_template_and_schema(
    template=template_string,
    schema=schema_dict,
    variables={"topic": "AI"}
)

# Use with OpenAI structured output
response = openai.chat.completions.create(
    model="gpt-4",
    messages=messages,
    response_format=response_format  # Automatic structured JSON
)
```

### Schema-Aware Templates

Your templates can even reference the schema:

```jinja2
{% chat role="system" %}
Respond in JSON format following this schema:
{{ json_schema }}
{% endchat %}

{% chat role="user" %}
Generate data about {{ topic }}.
{% endchat %}
```

### Flexible Input Types

The new `parse_template_and_schema` function supports multiple input formats:

```python
from olingo_llm_parser import parse_template_and_schema

# Template as file path, schema as file path  
messages, format = parse_template_and_schema("template.jinja", "schema.json")

# Template as string, schema as dictionary
template_str = """{% chat role="user" %}Hello!{% endchat %}"""
schema_dict = {"type": "string"}
messages, format = parse_template_and_schema(template_str, schema_dict)

# Template as string, schema as JSON string
schema_json = '{"type": "object", "properties": {"name": {"type": "string"}}}'
messages, format = parse_template_and_schema(template_str, schema_json)

# Template only (no schema)
messages, format = parse_template_and_schema(template_str)  # format will be None
```

## 📚 API Reference

### Core Functions

#### `parse_chat_template(template, variables=None)`

Parse a Jinja2 template containing `{% chat %}` blocks.

**Parameters:**
- `template` (str|Path): Either a file path or template string content
- `variables` (dict, optional): Variables to pass to the template

**Returns:**
- `List[Dict[str, str]]`: List of message dictionaries with 'role' and 'content'

#### `load_json_schema(schema_path)`

Load a JSON schema and format it for AI APIs.

**Parameters:**
- `schema_path` (str): Path to your JSON schema file

**Returns:**
- `Dict`: Formatted response_format for AI APIs

#### `parse_template_and_schema(template, schema=None, variables=None)`

Parse both template and schema together with flexible input types.

**Parameters:**
- `template` (str|Path): Either a file path or template string content
- `schema` (str|Path|Dict, optional): Either a file path, JSON string, or schema dictionary
- `variables` (dict, optional): Variables to pass to the template

**Returns:**
- `Tuple[List[Dict], Dict]`: (messages, response_format) ready for AI APIs

## 🏗️ Template Syntax

### Chat Blocks

```jinja2
{% chat role="system" %}
Your system message here
{% endchat %}

{% chat role="user" %}
Your user message here  
{% endchat %}

{% chat role="assistant" %}
Your assistant message here
{% endchat %}
```

### Variables

```jinja2
{% chat role="user" %}
Hello {{ name }}, tell me about {{ topic }}.
{% endchat %}
```

### Loops

```jinja2
{% for item in items %}
{% chat role="user" %}
Process this: {{ item }}
{% endchat %}
{% endfor %}
```

### Conditionals

```jinja2
{% chat role="system" %}
{% if expert_mode %}
You are an expert assistant with advanced capabilities.
{% else %}
You are a helpful general assistant.
{% endif %}
{% endchat %}
```

## 🎯 Use Cases

- **AI Chat Applications**: Structure conversations for any chat API
- **Prompt Engineering**: Create reusable, dynamic prompt templates  
- **AI Agents**: Build complex conversational flows
- **Data Generation**: Generate structured training data
- **API Integration**: Seamless integration with OpenAI, Anthropic, etc.

## 🤝 Why Choose Olingo LLM Parser?

| Feature | Olingo LLM Parser | Manual String Building | Other Solutions |
|---------|-------------------|------------------------|-----------------|
| **Readability** | ✅ Clean template syntax | ❌ Messy string concat | ⚠️ Complex APIs |
| **Maintainability** | ✅ Separate logic & content | ❌ Mixed code/content | ⚠️ Vendor lock-in |
| **Flexibility** | ✅ Full Jinja2 power | ❌ Limited logic | ⚠️ Restricted features |
| **AI Integration** | ✅ Perfect API format | ❌ Manual formatting | ⚠️ API-specific |
| **Schema Support** | ✅ Built-in JSON schema | ❌ No schema support | ❌ No schema support |

## 📋 Requirements

- Python 3.8+
- Jinja2 3.0+

## 🛠️ Development

```bash
# Clone repository
git clone https://github.com/ollsoft-ai/olingo-llm-parser.git
cd olingo-llm-parser

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .
```

### 📦 Building and Publishing New Versions

#### 1. **Update Version Number**

**🎯 Recommended: Automated Version Bumping**

We use `bump2version` for automated version management:

```bash
# Install bump2version (one-time setup)
pip install bump2version

# Bump patch version (0.1.2 → 0.1.3)
bump2version patch

# Bump minor version (0.1.3 → 0.2.0)  
bump2version minor

# Bump major version (0.2.0 → 1.0.0)
bump2version major
```

This automatically:
- ✅ Updates version in `olingo_llm_parser/__init__.py`
- ✅ Creates a git commit with the version bump
- ✅ Creates a git tag (e.g., `v0.1.3`)
- ✅ Single source of truth (version only in `__init__.py`)

**Manual Alternative:**
If you prefer manual updates, just edit the version in `olingo_llm_parser/__init__.py`:
```python
__version__ = "0.1.3"  # Update this line only
```

**Semantic Versioning Guidelines:**
- **Patch** (0.1.1 → 0.1.2): Bug fixes, no breaking changes
- **Minor** (0.1.2 → 0.2.0): New features, backward compatible  
- **Major** (0.2.0 → 1.0.0): Breaking changes

#### 2. **Install Build Tools**
```bash
pip install build twine
```

#### 3. **Run Tests**
Make sure all tests pass before publishing:
```bash
python -m pytest -v
```

#### 4. **Clean Previous Builds**
```bash
# PowerShell (Windows)
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Bash (Linux/Mac)
rm -rf dist/ build/ *.egg-info/
```

#### 5. **Build the Package**
```bash
python -m build
```

This creates two files in `dist/`:
- `olingo-llm-parser-X.X.X.tar.gz` (source distribution)
- `olingo_llm_parser-X.X.X-py3-none-any.whl` (wheel distribution)

#### 7. **Upload to PyPI**
Once verified on TestPyPI:
```bash
python -m twine upload dist/*
```

#### 8. **Tag the Release**
```bash
git add .
git commit -m "chore: bump version to X.X.X"
git tag vX.X.X
git push origin main --tags
```

### 🔐 **PyPI Authentication**

**Option A: API Token (Recommended)**
1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Create an API token
3. Use `__token__` as username and your token as password

**Option B: Configure ~/.pypirc**
```ini
[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
username = __token__
password = pypi-your-testpypi-token-here
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by the Ollsoft Team**

</div> 