from piper import PiperVoice
import uuid
import os
import tempfile
import wave
import numpy as np
from scipy.io import wavfile

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

    # Combine all chunks into a single bytes object
    audio_data = b"".join(audio_chunks)
    
    # Convert bytes to numpy array (int16)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # If stereo, reshape appropriately
    if channels == 2:
        audio_array = audio_array.reshape(-1, 2)
    
    # Write WAV file using scipy
    wavfile.write(output_path, sample_rate, audio_array)

    return output_path