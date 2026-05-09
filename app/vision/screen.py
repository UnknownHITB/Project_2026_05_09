import pyautogui
import os
import tempfile
from datetime import datetime

def capture_screen(output_path: str = None) -> str | None:
    """
    Captures a screenshot of the primary monitor.
    
    Args:
        output_path: Path to save the image. If None, creates a temp file.
        
    Returns:
        The path to the saved image, or None if it fails.
    """
    try:
        screenshot = pyautogui.screenshot()
        
        if output_path is None:
            temp_dir = tempfile.gettempdir()
            filename = f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            output_path = os.path.join(temp_dir, filename)

        screenshot.save(output_path)
        return f"IMAGE_PATH:{output_path}"
    except Exception as e:
        print(f"[Vision] Error capturing screen: {e}")
        return None


def register(registry):
    """Register the capture_screen tool with the given registry."""
    registry.register(
        name="capture_screen",
        description="Capture a screenshot of the user's screen to see what they are looking at.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        func=capture_screen
    )
