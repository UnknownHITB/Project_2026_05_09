from .registry import registry

def get_current_time():
    """Returns the current system time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Register the tool
registry.register(
    name="get_current_time",
    description="Get the current system date and time.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
    func=get_current_time
)

def add_numbers(a: float, b: float):
    """Adds two numbers together."""
    return a + b

registry.register(
    name="add_numbers",
    description="Add two numbers together.",
    parameters={
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "The first number"},
            "b": {"type": "number", "description": "The second number"},
        },
        "required": ["a", "b"],
    },
    func=add_numbers
)
