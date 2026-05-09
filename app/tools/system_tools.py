import os
import subprocess
import shutil
try:
    from AppOpener import open as open_app
except ImportError:
    open_app = None
from app.tools.registry import registry

def open_program(program_name: str) -> str:
    """
    Attempts to open a program by its name using multiple system methods.
    Tries different approaches until one succeeds or all options are exhausted.
    """
    # Normalize name (remove extension for which() check if needed)
    base_name = program_name.replace(".exe", "")
    
    # Strategy 1: os.startfile (The "Windows Magic" way)
    try:
        os.startfile(program_name)
        return f"Success: Opened '{program_name}' using os.startfile."
    except Exception:
        try:
            os.startfile(f"{base_name}.exe")
            return f"Success: Opened '{base_name}.exe' using os.startfile."
        except Exception:
            pass

    # Strategy 2: AppOpener (Best for installed apps like Spotify, Chrome, etc.)
    if open_app:
        try:
            # We use match_closest=True to be flexible with names
            open_app(program_name, match_closest=True)
            # AppOpener doesn't return a status, but if it doesn't raise, we assume it worked
            return f"Success: Opened '{program_name}' using AppOpener."
        except Exception:
            pass

    # Strategy 3: shutil.which (Find in PATH)
    path = shutil.which(program_name) or shutil.which(f"{base_name}.exe")
    if path:
        try:
            subprocess.Popen([path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            return f"Success: Opened via PATH at '{path}'."
        except Exception:
            pass

    # Strategy 4: Windows 'start' command
    try:
        # Use subprocess.run with check=True to see if 'start' actually found something
        # Note: 'start' returns immediately, so we just check if the command itself was valid
        subprocess.run(f"start \"\" \"{program_name}\"", shell=True, check=True, capture_output=True)
        return f"Success: Opened '{program_name}' via Windows 'start' command."
    except Exception:
        pass

    # Strategy 5: Shell execution (Last resort)
    # Only try this if the name looks like an executable
    if shutil.which(program_name):
        try:
            subprocess.Popen(program_name, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            return f"Success: Opened '{program_name}' using shell execution."
        except Exception:
            pass

    return f"Error: Could not find or open '{program_name}' using any available method."

def register_system_tools():
    registry.register(
        name="open_program",
        description="Opens a program on the computer by its name (e.g., 'notepad', 'chrome', 'calc').",
        parameters={
            "type": "object",
            "properties": {
                "program_name": {
                    "type": "string", 
                    "description": "The name of the program to open."
                }
            },
            "required": ["program_name"]
        },
        func=open_program
    )
