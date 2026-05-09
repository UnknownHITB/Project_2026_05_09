# AI Chat Assistant

A simple AI assistant supporting both voice and text input, powered by Ollama.

## Project Structure

- `main.py`: Entry point for the application.
- `app/`: Core logic and providers.
  - `ollama_provider.py`: Interface for communicating with the Ollama API (supports tool calling).
  - `stt.py`: Speech-to-text conversion.
  - `text.py`: Text chat interface.
  - `listener.py`: Voice detection and recording logic.
  - `tools/`: Extensible tool system.
    - `registry.py`: Central registry for tool definitions and functions.
    - `example.py`: Sample tools (e.g., `get_current_time`).
- `.env`: Configuration for Ollama URL and model.
- `requirements.txt`: Python dependencies.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Configure your `.env` file:
    ```env
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL=llama3
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

## Usage

Select between **Voice** or **Text** mode at startup.
- In **Voice** mode, speak naturally. The assistant detects when you stop speaking and transcribes the audio.
- In **Text** mode, type your prompts directly.
- Say or type `exit` or `quit` to end the session.

## Adding Tools

To add a new tool:
1. Create a function in a new file (e.g., `app/tools/weather.py`) or in `example.py`.
2. Use `registry.register()` to define the tool name, description, and JSON parameters.
3. Import your file in `app/tools/__init__.py`.

The AI will automatically see these tools and call them when needed!
