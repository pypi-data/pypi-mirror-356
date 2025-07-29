import json

_registry = {}

def register_tool(name, func, schema):
    _registry[name] = {"func": func, "schema": schema}

def get_registered_tools():
    return _registry

def export_tools_to_json(path="tools.json"):
    tools = {k: v["schema"] for k, v in _registry.items()}
    with open(path, "w") as f:
        json.dump(list(tools.values()), f, indent=2)
