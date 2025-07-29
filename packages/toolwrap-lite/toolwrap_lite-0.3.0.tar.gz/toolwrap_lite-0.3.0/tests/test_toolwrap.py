from toolwrap_lite import tool, get_registered_tools

@tool
def greet(name: str) -> str:
    """Greet a user."""
    return f"Hello, {name}!"

def test_registry():
    tools = get_registered_tools()
    assert "greet" in tools
    assert tools["greet"]["schema"]["name"] == "greet"
