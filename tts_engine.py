from piper import PiperVoice
import uuid
import os
import tempfile

# Load Piper model
voice = PiperVoice.load(
    "piper/es_MX-claude-high.onnx",
    "piper/es_MX-claude-high.onnx.json"
)

def synthesize(text: str) -> str:
    filename = f"tts_{uuid.uuid4()}.wav"
    # Use system temp directory instead of /tmp
    output_path = os.path.join(tempfile.gettempdir(), filename)

    generator = voice.synthesize(text)

    with open(output_path, "wb") as f:
        for chunk in generator:
            f.write(chunk.audio_int16_bytes)

    return output_path