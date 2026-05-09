import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OllamaProvider:
    def __init__(self, base_url=None, model=None):
        # Priority: constructor argument > environment variable > default value
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")

    def chat(self, messages):
        """
        Sends a list of messages to Ollama and returns the response.
        Messages should be in the format: [{"role": "user", "content": "hello"}]
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {e}"

if __name__ == "__main__":
    # Quick test
    provider = OllamaProvider()
    print(provider.chat([{"role": "user", "content": "Say hello!"}]))
