"""
stt.py — Speech-to-text conversion from a .wav file.

Public API
----------
transcribe_wav(wav_path: str) -> str
    Transcribes the given .wav file and returns the text.
    On failure, returns a string starting with 'Error:'.
"""
import os

# Global model instance for lazy initialization
_model = None

def get_model():
    """
    Lazy load the Whisper model.
    Initializes on CUDA by default for maximum performance.
    """
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        import torch
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # float16 is best for CUDA, int8 for CPU
        compute_type = "float16" if device == "cuda" else "int8"
        
        _model = WhisperModel("base", device=device, compute_type=compute_type)
    return _model

def transcribe_wav(wav_path: str) -> str:
    """
    Convert a .wav file to text using faster-whisper.

    Args:
        wav_path: Absolute or relative path to the .wav file.

    Returns:
        Transcribed text, or an error string beginning with 'Error:'.
    """
    if not os.path.exists(wav_path):
        return f"Error: File not found: {wav_path}"

    try:
        model = get_model()
        segments, info = model.transcribe(wav_path, beam_size=5)
        
        # Combine segments into a single string
        text = " ".join([segment.text for segment in segments]).strip()
        return text

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
