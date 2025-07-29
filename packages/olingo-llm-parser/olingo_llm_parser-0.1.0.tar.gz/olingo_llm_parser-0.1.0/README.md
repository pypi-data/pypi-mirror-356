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
from olingo_llm_parser import parse_chat_and_schema

# Parse both template and schema
messages, response_format = parse_chat_and_schema(
    template_path="template.jinja",
    schema_path="response_schema.json",
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

## 📚 API Reference

### Core Functions

#### `parse_chat_template(template_path, variables=None)`

Parse a Jinja2 template containing `{% chat %}` blocks.

**Parameters:**
- `template_path` (str): Path to your .jinja template file
- `variables` (dict, optional): Variables to pass to the template

**Returns:**
- `List[Dict[str, str]]`: List of message dictionaries with 'role' and 'content'

#### `load_json_schema(schema_path)`

Load a JSON schema and format it for AI APIs.

**Parameters:**
- `schema_path` (str): Path to your JSON schema file

**Returns:**
- `Dict`: Formatted response_format for AI APIs

#### `parse_chat_and_schema(template_path, schema_path=None, variables=None)`

Parse both template and schema together.

**Parameters:**
- `template_path` (str): Path to your .jinja template file  
- `schema_path` (str, optional): Path to your JSON schema file
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

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📞 Support

- 📖 [Documentation](https://olingo-llm-parser.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/ollsoft-ai/olingo-llm-parser/issues)
- 💬 [Discussions](https://github.com/ollsoft-ai/olingo-llm-parser/discussions)

---

<div align="center">

**Made with ❤️ by the Ollsoft Team**

[⭐ Star us on GitHub](https://github.com/ollsoft-ai/olingo-llm-parser) • [📦 PyPI Package](https://pypi.org/project/olingo-llm-parser/)

</div> 