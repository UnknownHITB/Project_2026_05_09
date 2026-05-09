from .ollama_provider import OllamaProvider


def run_text_chat(provider: OllamaProvider = None):
    """
    Run an interactive text-based chat session.

    Args:
        provider: An optional OllamaProvider instance. A new one is created if
                  not provided.
    """
    if provider is None:
        provider = OllamaProvider()

    print("\n--- Text Chat Mode ---")
    print("Type 'exit' or 'quit' to stop the conversation.\n")

    messages = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not user_input.strip():
            continue

        messages.append({"role": "user", "content": user_input})

        print("AI: ", end="", flush=True)
        response = provider.chat(messages)
        print(response)

        messages.append({"role": "assistant", "content": response})


# ── Standalone usage ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_text_chat()
