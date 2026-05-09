from kokoro import KPipeline
import torch
import sounddevice as sd

def test_kokoro():
    print("Initializing Kokoro...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    pipeline = KPipeline(lang_code='a', device=device)
    
    print("Generating audio...")
    generator = pipeline("Hello world", voice='af_heart', speed=1.0)
    for gs, ps, audio in generator:
        if audio is not None:
            print("Playing audio...")
            sd.play(audio, 24000)
            sd.wait()
    print("Done!")

if __name__ == "__main__":
    test_kokoro()
