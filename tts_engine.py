from piper import PiperVoice
import uuid
import os
import tempfile
import struct

# Load Piper model
voice = PiperVoice.load(
    "piper/es_MX-claude-high.onnx",
    "piper/es_MX-claude-high.onnx.json"
)

def create_wav_header(num_channels, sample_rate, sample_width, num_samples):
    """Crea un header WAV válido"""
    byte_rate = sample_rate * num_channels * sample_width
    block_align = num_channels * sample_width
    data_size = num_samples * num_channels * sample_width
    
    header = b'RIFF'
    header += struct.pack('<I', 36 + data_size)
    header += b'WAVE'
    
    # fmt subchunk
    header += b'fmt '
    header += struct.pack('<I', 16)  # Subchunk1Size
    header += struct.pack('<H', 1)   # AudioFormat (1 = PCM)
    header += struct.pack('<H', num_channels)
    header += struct.pack('<I', sample_rate)
    header += struct.pack('<I', byte_rate)
    header += struct.pack('<H', block_align)
    header += struct.pack('<H', sample_width * 8)  # BitsPerSample
    
    # data subchunk
    header += b'data'
    header += struct.pack('<I', data_size)
    
    return header

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
    num_samples = len(audio_data) // (channels * sample_width)

    # Create header
    header = create_wav_header(channels, sample_rate, sample_width, num_samples)

    # Write WAV file
    with open(output_path, "wb") as f:
        f.write(header)
        f.write(audio_data)

    return output_path