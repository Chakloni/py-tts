from piper import PiperVoice
import uuid
import os
import tempfile
import wave
import io

# Load Piper model
voice = PiperVoice.load(
    "piper/es_MX-claude-high.onnx",
    "piper/es_MX-claude-high.onnx.json"
)

def synthesize(text: str) -> str:
    filename = f"tts_{uuid.uuid4()}.wav"
    output_path = os.path.join(tempfile.gettempdir(), filename)

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

    # Write proper WAV file
    with wave.open(output_path, "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data)

    return output_path