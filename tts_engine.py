from piper import PiperVoice
import uuid
import os
import tempfile
import wave
from pydub import AudioSegment

# Load Piper model
voice = PiperVoice.load(
    "piper/es_MX-claude-high.onnx",
    "piper/es_MX-claude-high.onnx.json"
)

def synthesize(text: str) -> str:
    # First create WAV file
    wav_filename = f"tts_{uuid.uuid4()}.wav"
    wav_path = os.path.join(tempfile.gettempdir(), wav_filename)

    generator = voice.synthesize(text)

    # Collect all audio chunks
    audio_chunks = []
    sample_rate = None
    sample_width = None
    channels = None

    for chunk in generator:
        audio_chunks.append(chunk.audio_int16_bytes)
        sample_rate = chunk.sample_rate
        sample_width = chunk.sample_width
        channels = chunk.sample_channels

    # Combine all chunks
    audio_data = b"".join(audio_chunks)

    # Write WAV file
    with wave.open(wav_path, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data)

    # Convert WAV to MP3
    mp3_filename = f"tts_{uuid.uuid4()}.mp3"
    mp3_path = os.path.join(tempfile.gettempdir(), mp3_filename)
    
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3", bitrate="192k")
    
    # Clean up WAV file
    os.remove(wav_path)

    return mp3_path