import os
from app.tools.registry import registry

def launch_steam_game(app_id: str) -> str:
    """
    Launches a Steam game using its AppID.
    """
    try:
        url = f"steam://launch/{app_id}"
        os.startfile(url)
        return f"Success: Sent launch command for Steam AppID {app_id}."
    except Exception as e:
        return f"Error: Could not launch Steam game {app_id}. {str(e)}"

def register_game_tools():
    registry.register(
        name="launch_steam_game",
        description="Launches a Steam game using its numerical AppID (e.g., '730' for CS:GO).",
        parameters={
            "type": "object",
            "properties": {
                "app_id": {
                    "type": "string",
                    "description": "The Steam AppID of the game."
                }
            },
            "required": ["app_id"]
        },
        func=launch_steam_game
    )
