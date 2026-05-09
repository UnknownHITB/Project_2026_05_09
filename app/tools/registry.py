from typing import Any, Callable, Dict, List

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.functions: Dict[str, Callable] = {}

    def register(self, name: str, description: str, parameters: Dict[str, Any], func: Callable):
        """
        Registers a new tool.
        
        Args:
            name: The name of the tool (e.g., 'get_weather').
            description: What the tool does.
            parameters: JSON schema for the tool's arguments.
            func: The actual Python function to call.
        """
        self.tools[name] = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters,
            },
        }
        self.functions[name] = func

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Returns the list of tool definitions for the Ollama API."""
        return list(self.tools.values())

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Executes a tool by name with the given arguments."""
        if name not in self.functions:
            return f"Error: Tool '{name}' not found."
        
        try:
            result = self.functions[name](**arguments)
            return str(result)
        except Exception as e:
            return f"Error executing tool '{name}': {str(e)}"

# Global registry instance
registry = ToolRegistry()
