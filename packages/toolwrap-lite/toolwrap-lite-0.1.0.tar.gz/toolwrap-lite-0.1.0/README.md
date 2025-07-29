# toolwrap-lite

**toolwrap-lite** is a lightweight Python package that automatically converts your Python functions into OpenAI-compatible function calling schemas using a simple decorator.

With Toolwrap-Lite, you can effortlessly expose any Python function — whether it's for CRM APIs, database queries, business logic, or custom tools — to modern AI agents, LLM frameworks, and autonomous systems that rely on structured tool schemas.

No more manually writing JSON schemas. Just decorate your function, and Toolwrap-Lite takes care of the rest.

## Features
- No manual JSON writing
- Auto-extracts type hints and docstrings
- Export all tools into `tools.json`
- Plug into OpenAI, LangChain, or CrewAI easily

## Example Use Cases
- Autonomous agents calling real APIs (CRM, finance, weather, analytics, etc.)
- RAG systems with dynamic function augmentation
- LangChain or CrewAI toolchains
- Backend SaaS tools exposed to AI copilots
- AI-powered automation platforms
- Self-hosted AI assistants with external tool access

## Installation
```bash
pip install toolwrap-lite
```

## Usage
```python
from toolwrap_lite import tool, get_registered_tools

@tool
def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y

print(get_registered_tools())
```

## Export to JSON
```python
from toolwrap_lite import export_tools_to_json
export_tools_to_json("tools.json")
```

## Example Tool
```python
@tool
def summarize_tweets(username: str, count: int = 5, language: str = "en") -> str:
    """Summarize tweets from a username."""
    return "Summary..."
```
