from .registry import registry
from . import example  # Import to trigger registration
from . import memory_tools
from . import system_tools
from . import search_tools
from . import game_tools

# Register vision tools (avoids circular import)
from app.vision import camera, screen
camera.register(registry)
screen.register(registry)

# Register memory tools
memory_tools.register_memory_tools()

# Register system tools
system_tools.register_system_tools()

# Register search tools
search_tools.register_search_tools()

# Register game tools
game_tools.register_game_tools()

__all__ = ["registry"]
