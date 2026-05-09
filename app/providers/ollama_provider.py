import requests
import json
import os
import sys
import base64
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to sys.path so absolute imports work regardless of how script is called
root_dir = str(Path(__file__).parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.tools import registry

class OllamaProvider:
    def __init__(self, base_url=None, model=None):
        # Priority: constructor argument > environment variable > default value
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")

    def _get_memory_context(self):
        """Retrieves and formats current memory state for injection into the prompt."""
        try:
            from app.core.memory import memory
            
            # Semantic: User Facts
            facts = memory.get_facts(entity='user')
            semantic_text = "KNOWN FACTS ABOUT USER:\n" + ("\n".join([f"- {a}: {v}" for a, v in facts]) if facts else "- None yet.")
            
            # Episodic: Recent summaries
            episodes = memory.get_recent_episodes(limit=3)
            episodic_text = "PAST CONVERSATION SUMMARIES:\n" + ("\n".join([f"- {s}" for s, _ in episodes]) if episodes else "- No past history.")
            
            # Procedural: System Rules
            rules = memory.get_all_rules()
            procedural_text = "CORE SYSTEM RULES:\n" + ("\n".join([f"- {r}" for r in rules]) if rules else "- Be helpful and concise.")
            
            return f"{procedural_text}\n\n{semantic_text}\n\n{episodic_text}"
        except Exception as e:
            print(f"[Memory] Error loading context: {e}")
            return "Be a helpful assistant."

    def chat(self, messages):
        """
        Sends a list of messages to Ollama and returns the response.
        Handles tool calls if the model requests them.
        """
        url = f"{self.base_url}/api/chat"
        
        # Inject memory context as a system message if not present
        memory_ctx = self._get_memory_context()
        
        # Check if first message is system, if so update it, otherwise insert
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = memory_ctx
        else:
            messages.insert(0, {"role": "system", "content": memory_ctx})

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
                    
                    # Check if the result is an image path (from vision tools)
                    if isinstance(result, str) and result.startswith("IMAGE_PATH:"):
                        img_path = result.replace("IMAGE_PATH:", "")
                        if os.path.exists(img_path):
                            try:
                                with open(img_path, "rb") as img_file:
                                    img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                                
                                # Ollama expects images on user/assistant messages, not tool messages.
                                # Append a tool result first, then a user message with the image.
                                messages.append({
                                    "role": "tool",
                                    "content": f"Image captured and attached from {func_name}.",
                                    "name": func_name
                                })
                                messages.append({
                                    "role": "user",
                                    "content": "Here is the captured image. Describe what you see.",
                                    "images": [img_base64]
                                })
                                print(f"[Vision] Attached image to message: {img_path}")
                                continue  # skip the normal tool_message append below

                            except Exception as e:
                                print(f"[Vision] Error encoding image: {e}")
                                result = f"Error encoding image: {e}"
                        else:
                            result = f"Image file not found at {img_path}"

                    # Append tool result to messages (non-image tools, or fallback)
                    messages.append({
                        "role": "tool",
                        "content": result,
                        "name": func_name
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
