from .registry import registry
from . import example  # Import to trigger registration
from . import memory_tools

# Register vision tools (avoids circular import)
from app.vision import camera, screen
camera.register(registry)
screen.register(registry)

# Register memory tools
memory_tools.register_memory_tools()

__all__ = ["registry"]
