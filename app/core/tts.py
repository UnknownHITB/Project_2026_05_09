import logging
import queue
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KokoroTTS:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(KokoroTTS, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, lang_code='a', voice='af_heart'):
        if self._initialized:
            return
        
        # Late imports to prevent conflicts at module level
        from kokoro import KPipeline
        import torch

        # Clear cache to free up VRAM from Ollama/Whisper usage
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        # Detect device
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Initializing Kokoro TTS Pipeline on {device.upper()}...")
        
        try:
            import sounddevice as sd
            self.sd = sd
            try:
                self.pipeline = KPipeline(lang_code=lang_code, device=device)
            except Exception as e:
                if device == 'cuda':
                    logger.warning(f"CUDA initialization failed, falling back to CPU: {e}")
                    device = 'cpu'
                    self.pipeline = KPipeline(lang_code=lang_code, device=device)
                else:
                    raise e
            
            self.voice = voice
            self.sample_rate = 24000
            self._initialized = True
            logger.info(f"Kokoro TTS initialized with voice: {voice} on {device.upper()}")
        except Exception as e:
            logger.error(f"Failed to initialize Kokoro TTS: {e}")
            self._initialized = False

    def speak(self, text):
        """
        Converts text to speech and plays it using a streaming approach.
        Starts playing as soon as the first segment is ready.
        """
        if not self._initialized:
            logger.error("TTS not initialized.")
            return

        if not text or not text.strip():
            return

        logger.info(f"Speaking (streaming): {text[:50]}...")
        
        audio_queue = queue.Queue()
        
        def producer():
            """Generates audio segments and puts them in the queue."""
            try:
                generator = self.pipeline(text, voice=self.voice, speed=1.0)
                for gs, ps, audio in generator:
                    if audio is not None:
                        audio_queue.put(audio)
            except Exception as e:
                logger.error(f"Error in TTS producer: {e}")
            finally:
                # Signal the end of the stream
                audio_queue.put(None)

        # Start the generation in a background thread
        producer_thread = threading.Thread(target=producer, daemon=True)
        producer_thread.start()

        # Consume and play segments as they become available
        try:
            while True:
                audio = audio_queue.get()
                if audio is None:  # End of stream signal
                    break
                
                # Play the segment
                self.sd.play(audio, self.sample_rate)
                self.sd.wait() # Wait for this segment to finish
                audio_queue.task_done()
        except Exception as e:
            logger.error(f"Error during streaming playback: {e}")

def speak(text):
    """
    Convenience function to speak text using the KokoroTTS singleton.
    """
    tts = KokoroTTS()
    tts.speak(text)

if __name__ == "__main__":
    # Test the TTS
    speak("Hello! This is a test of the Kokoro Text to Speech system.")
