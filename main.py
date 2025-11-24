from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from tts_engine import synthesize

app = FastAPI()

class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
def tts(req: TTSRequest):
    wav_path = synthesize(req.text)
    return FileResponse(wav_path, media_type="audio/wav")