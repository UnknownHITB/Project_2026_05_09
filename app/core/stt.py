"""
stt.py — Speech-to-text conversion from a .wav file.

Public API
----------
transcribe_wav(wav_path: str) -> str
    Transcribes the given .wav file and returns the text.
    On failure, returns a string starting with 'Error:'.
"""

import speech_recognition as sr


def transcribe_wav(wav_path: str) -> str:
    """
    Convert a .wav file to text using Google Web Speech API.

    Args:
        wav_path: Absolute or relative path to the .wav file.

    Returns:
        Transcribed text, or an error string beginning with 'Error:'.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)

        return recognizer.recognize_google(audio)

    except FileNotFoundError:
        return f"Error: File not found: {wav_path}"
    except sr.UnknownValueError:
        return "Error: Could not understand the audio."
    except sr.RequestError as e:
        return f"Error: Speech Recognition service unavailable; {e}"
    except Exception as e:
        return f"Error: {e}"


# ── Standalone test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python stt.py path/to/file.wav")
        sys.exit(1)

    result = transcribe_wav(sys.argv[1])
    print(f"Transcribed: {result}")
