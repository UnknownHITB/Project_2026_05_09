"""
listener.py — Continuously monitors the microphone, detects speech via
energy-based VAD, records until silence, and saves the result as a .wav file.

Public API
----------
listen_for_speech(output_path=None, threshold=None) -> str | None
    Blocks until a full utterance is captured.
    Returns the path to the saved .wav file, or None on failure.
"""

import audioop
import os
import tempfile
import wave
from collections import deque

import pyaudio

# ── Audio settings ─────────────────────────────────────────────────────────────
CHUNK       = 1024          # frames per buffer read
FORMAT      = pyaudio.paInt16
CHANNELS    = 1
RATE        = 16000         # Hz  (good for speech recognition)

# ── VAD settings ───────────────────────────────────────────────────────────────
DEFAULT_THRESHOLD      = 500   # RMS level that counts as "speech"
SILENCE_AFTER_SPEECH   = 1.5   # seconds of silence before we stop recording (faster response)
MIN_SPEECH_SECONDS     = 0.3   # ignore blips shorter than this
PRE_BUFFER_SECONDS     = 0.5   # amount of audio to keep before speech is detected


def _rms(data: bytes) -> float:
    """
    Return the RMS (loudness) of a raw PCM chunk.
    Optimized using audioop.rms for ~50x speedup over manual calculation.
    """
    if not data:
        return 0.0
    # width=2 for 16-bit audio (FORMAT = pyaudio.paInt16)
    return float(audioop.rms(data, 2))


# Global PyAudio instance to avoid overhead of re-initializing hardware
_p = None

def get_pyaudio():
    global _p
    if _p is None:
        _p = pyaudio.PyAudio()
    return _p

def listen_for_speech(output_path: str = None, threshold: int = DEFAULT_THRESHOLD) -> str | None:
    """
    Wait for the user to speak, record the utterance, then return the .wav path.

    Args:
        output_path: Where to save the .wav file. A temp file is used if None.
        threshold:   RMS value above which audio is considered speech.

    Returns:
        Path to the saved .wav file, or None if nothing was recorded.
    """
    # Prepare output file
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".wav", prefix="speech_")
        os.close(fd)

    pa = get_pyaudio()
    sample_width = pa.get_sample_size(FORMAT)

    stream = pa.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("🎙  Listening… (waiting for you to speak)")

    frames          = []
    recording       = False
    silent_chunks   = 0
    speech_chunks   = 0

    # How many consecutive silent chunks = SILENCE_AFTER_SPEECH seconds
    silence_limit = int(RATE / CHUNK * SILENCE_AFTER_SPEECH)
    # Minimum chunks to count as real speech
    min_speech    = int(RATE / CHUNK * MIN_SPEECH_SECONDS)
    # Number of chunks to keep in pre-buffer
    pre_buffer_limit = int(RATE / CHUNK * PRE_BUFFER_SECONDS)
    pre_buffer = deque(maxlen=pre_buffer_limit)

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            loud = _rms(data) > threshold

            if loud:
                if not recording:
                    print("🔴 Recording…")
                    recording    = True
                    silent_chunks = 0
                    # Prepend the pre-buffer when recording starts
                    frames.extend(list(pre_buffer))
                    pre_buffer.clear()
                
                speech_chunks += 1
                frames.append(data)

            elif recording:
                # Still append during silence so the utterance ending isn't cut off
                frames.append(data)
                silent_chunks += 1
                if silent_chunks >= silence_limit:
                    print("⏹  Speech ended.")
                    break
            else:
                # Not recording yet, keep the pre-buffer updated
                pre_buffer.append(data)

    except KeyboardInterrupt:
        print("\nListener interrupted.")
    finally:
        stream.stop_stream()
        stream.close()
        # We don't terminate _p here to keep it alive for the next call

    # Discard too-short captures (likely noise)
    if speech_chunks < min_speech:
        os.remove(output_path)
        return None

    # Save WAV
    full_audio = b"".join(frames)
    
    # --- Quality Improvement: Normalization ---
    # Boost the volume so the loudest part is at 80% of max (to avoid clipping but ensure clarity)
    try:
        max_val = audioop.max(full_audio, 2)
        if max_val > 0:
            target_max = 32767 * 0.8
            factor = target_max / max_val
            if factor > 1.0: # Only boost if it's too quiet
                full_audio = audioop.mul(full_audio, 2, factor)
    except Exception as e:
        print(f"[Listener] Normalization failed: {e}")

    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(full_audio)

    return output_path


# ── Standalone test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    path = listen_for_speech()
    if path:
        print(f"Saved: {path}")
    else:
        print("Nothing was recorded.")
