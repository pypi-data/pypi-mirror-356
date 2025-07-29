import inspect
from .schema import generate_schema
from .registry import register_tool

def tool(func):
    """Decorator to register a function as a tool."""
    schema = generate_schema(func)
    register_tool(func.__name__, func, schema)
    return func
