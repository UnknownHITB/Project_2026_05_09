from .registry import registry
from . import example  # Import to trigger registration

# Register vision tools (avoids circular import)
from app.vision import camera, screen
camera.register(registry)
screen.register(registry)

__all__ = ["registry"]
