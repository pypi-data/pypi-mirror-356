import inspect

def get_type_name(t):
    return t.__name__.lower() if hasattr(t, '__name__') else str(t)

def generate_schema(func):
    """Generates OpenAI-compatible JSON schema from a function signature."""
    sig = inspect.signature(func)
    properties = {}
    required = []

    for name, param in sig.parameters.items():
        param_type = get_type_name(param.annotation) if param.annotation != inspect.Parameter.empty else "string"
        properties[name] = {"type": param_type}
        if param.default == inspect.Parameter.empty:
            required.append(name)

    return {
        "name": func.__name__,
        "description": func.__doc__ or "",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }
