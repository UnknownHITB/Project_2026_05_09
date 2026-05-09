"""
main.py — Entry point for the AI chat assistant.

Choose your input mode:
  1. Voice  — listener detects speech → saves .wav → stt converts → AI responds
  2. Text   — type your prompt
"""

import os
from app.ollama_provider import OllamaProvider


def pick_mode() -> str:
    print("╔══════════════════════════════╗")
    print("║      AI Chat Assistant       ║")
    print("╠══════════════════════════════╣")
    print("║  1.  Voice (speak)           ║")
    print("║  2.  Text  (type)            ║")
    print("╚══════════════════════════════╝")
    while True:
        choice = input("Select mode [1/2]: ").strip()
        if choice in ("1", "2"):
            return "voice" if choice == "1" else "text"
        print("Please enter 1 or 2.")


def run_voice_chat(provider: OllamaProvider):
    """
    Continuous voice loop:
      listener captures speech → saves .wav → stt transcribes → AI responds
    """
    from app.listener import listen_for_speech
    from app.stt import transcribe_wav

    print("\n--- Voice Chat Mode ---")
    print("Speak naturally. Say 'exit' or 'quit' to stop. Press Ctrl+C to cancel.\n")

    messages = []

    while True:
        try:
            # 1. Capture speech → .wav
            wav_path = listen_for_speech()

            if wav_path is None:
                print("[Listener] Nothing captured, trying again…\n")
                continue

            # 2. Convert .wav → text
            user_input = transcribe_wav(wav_path)

            # Clean up the temp file
            try:
                os.remove(wav_path)
            except OSError:
                pass

            if user_input.startswith("Error:"):
                print(f"[STT] {user_input}\n")
                continue

            print(f"You said: {user_input}")

            if user_input.strip().lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            # 3. Send to AI
            messages.append({"role": "user", "content": user_input})
            print("AI: ", end="", flush=True)
            response = provider.chat(messages)
            print(response, "\n")

        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
            break


def main():
    provider = OllamaProvider()
    mode = pick_mode()

    if mode == "voice":
        run_voice_chat(provider)
    else:
        from app.text import run_text_chat
        run_text_chat(provider)


if __name__ == "__main__":
    main()
