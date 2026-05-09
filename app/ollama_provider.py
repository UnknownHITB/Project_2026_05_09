import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import sys
from pathlib import Path

# Add project root to sys.path so absolute imports work regardless of how script is called
root_dir = str(Path(__file__).parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.tools import registry

class OllamaProvider:
    def __init__(self, base_url=None, model=None):
        # Priority: constructor argument > environment variable > default value
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")

    def chat(self, messages):
        """
        Sends a list of messages to Ollama and returns the response.
        Handles tool calls if the model requests them.
        """
        url = f"{self.base_url}/api/chat"
        
        while True:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "tools": registry.get_tool_definitions()
            }
            
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                response_json = response.json()
                message = response_json.get("message", {})
                
                # Add model's response to history
                messages.append(message)
                
                # Check for tool calls
                tool_calls = message.get("tool_calls")
                if not tool_calls:
                    return message.get("content", "")

                # Process each tool call
                print(f"[Tools] Model requested {len(tool_calls)} tool(s)...")
                for tool_call in tool_calls:
                    func_name = tool_call["function"]["name"]
                    func_args = tool_call["function"]["arguments"]
                    
                    print(f"[Tools] Executing: {func_name}({func_args})")
                    result = registry.call_tool(func_name, func_args)
                    
                    # Append tool result to messages
                    messages.append({
                        "role": "tool",
                        "content": result,
                        "name": func_name # Optional but helpful
                    })
                
                # After appending tool results, loop back to let the model generate the final response
                
            except requests.exceptions.RequestException as e:
                return f"Error connecting to Ollama: {e}"

if __name__ == "__main__":
    # Quick test
    provider = OllamaProvider()
    # Test tool usage
    test_messages = [{"role": "user", "content": "What time is it and what is 123 + 456?"}]
    print("User:", test_messages[0]["content"])
    response = provider.chat(test_messages)
    print("AI:", response)
