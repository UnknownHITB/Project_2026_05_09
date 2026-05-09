import cv2
import os
import tempfile
from datetime import datetime

def capture_camera(output_path: str = None) -> str | None:
    """
    Captures a single frame from the default camera.
    
    Args:
        output_path: Path to save the image. If None, creates a temp file.
        
    Returns:
        The path to the saved image, or None if it fails.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Vision] Error: Could not open camera.")
        return None

    # Let the camera warm up/auto-adjust
    for _ in range(5):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("[Vision] Error: Could not read frame.")
        return None

    if output_path is None:
        temp_dir = tempfile.gettempdir()
        filename = f"camera_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        output_path = os.path.join(temp_dir, filename)

    cv2.imwrite(output_path, frame)
    return f"IMAGE_PATH:{output_path}"


def register(registry):
    """Register the capture_camera tool with the given registry."""
    registry.register(
        name="capture_camera",
        description="Capture an image from the webcam to see the physical environment.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
        },
        func=capture_camera
    )
