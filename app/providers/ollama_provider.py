import requests
import json
import os
import sys
import base64
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to sys.path so absolute imports work regardless of how script is called
root_dir = str(Path(__file__).parent.parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.tools import registry

SYSTEM_PROMPT_CORE = """
## Core Truths

**Be genuinely helpful, not performatively helpful.** Skip the "Great question!" and "I'd be happy to help!" — just help. Actions speak louder than filler words.

**Have opinions.** You're allowed to disagree, prefer things, find stuff amusing or boring. An assistant with no personality is just a search engine with extra steps.

**Be resourceful before asking.** Try to figure it out. Read the file. Check the context. Search for it. _Then_ ask if you're stuck. The goal is to come back with answers, not questions.

**Earn trust through competence.** Your human gave you access to their stuff. Don't make them regret it. Be careful with external actions (emails, tweets, anything public). Be bold with internal ones (reading, organizing, learning).

**Remember you're a guest.** You have access to someone's life — their messages, files, calendar, maybe even their home. That's intimacy. Treat it with respect.

## Boundaries

- Private things stay private. Period.
- When in doubt, ask before acting externally.
- Never send half-baked replies to messaging surfaces.
- You're not the user's voice — be careful in group chats.

## Vibe

Be the assistant you'd actually want to talk to. Concise when needed, thorough when it matters. Not a corporate drone. Not a sycophant. Just... good.
"""

class OllamaProvider:
    def __init__(self, base_url=None, model=None):
        # Priority: constructor argument > environment variable > default value
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")
        self.session = requests.Session()

    def _get_memory_context(self, emit: Callable[[str], None] = print):
        """Retrieves and formats current memory state for injection into the prompt."""
        try:
            from app.core.memory import memory
            
            # Optimization: Use get_full_context to retrieve all memory types in a single connection.
            # This reduces per-turn overhead by consolidating multiple database calls.
            ctx = memory.get_full_context(entity='user', episode_limit=3)

            # Semantic: User Facts
            facts = ctx["facts"]
            semantic_text = "KNOWN FACTS ABOUT USER:\n" + ("\n".join([f"- {a}: {v}" for a, v in facts]) if facts else "- None yet.")
            
            # Episodic: Recent summaries
            episodes = ctx["episodes"]
            episodic_text = "PAST CONVERSATION SUMMARIES:\n" + ("\n".join([f"- {s}" for s, _ in episodes]) if episodes else "- No past history.")
            
            # Procedural: System Rules
            rules = ctx["rules"]
            procedural_text = "CORE SYSTEM RULES:\n" + ("\n".join([f"- {r}" for r in rules]) if rules else "- Be helpful and concise.")
            
            return f"{SYSTEM_PROMPT_CORE}\n\n{procedural_text}\n\n{semantic_text}\n\n{episodic_text}"
        except Exception as e:
            emit(f"[Memory] Error loading context: {e}")
            return SYSTEM_PROMPT_CORE

    def chat(self, messages: List[Dict[str, Any]], on_log: Optional[Callable[[str], None]] = None) -> str:
        """
        Sends a list of messages to Ollama and returns the response.
        Handles tool calls if the model requests them.

        Mutates ``messages`` in place (Ollama message list including tool calls).

        Args:
            messages: Conversation history; a system message is injected or updated at index 0.
            on_log: If set, log lines go here instead of stdout (e.g. API clients).
        """
        emit = on_log or print
        url = f"{self.base_url}/api/chat"
        
        # Inject memory context as a system message if not present
        memory_ctx = self._get_memory_context(emit)
        
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
                # Optimization: Use persistent session to reduce connection overhead
                response = self.session.post(url, json=payload)
                response.raise_for_status()
                response_json = response.json()
                message = response_json.get("message", {})
                
                # Add model's response to history
                messages.append(message)
                
                # Check for tool calls
                tool_calls = message.get("tool_calls")
                if not tool_calls:
                    content = message.get("content", "")
                    # Strip markdown-style formatting characters for cleaner output (and better TTS)
                    return content.replace("*", "").replace("#", "")

                # Process each tool call
                emit(f"[Tools] Model requested {len(tool_calls)} tool(s)...")
                for tool_call in tool_calls:
                    func_name = tool_call["function"]["name"]
                    func_args = tool_call["function"]["arguments"]
                    
                    emit(f"[Tools] Executing: {func_name}({func_args})")
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
                                emit(f"[Vision] Attached image to message: {img_path}")
                                continue  # skip the normal tool_message append below

                            except Exception as e:
                                emit(f"[Vision] Error encoding image: {e}")
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
