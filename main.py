from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from tts_engine import synthesize
import io
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str

class DebugLog(BaseModel):
    message: str
    userAgent: str
    timestamp: str

@app.post("/tts")
def tts(req: TTSRequest):
    mp3_path = synthesize(req.text)
    
    with open(mp3_path, "rb") as f:
        audio_bytes = f.read()
    
    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline"}
    )

@app.post("/debug-log")
def debug_log(log: DebugLog):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {log.message}")
    print(f"  User Agent: {log.userAgent}")
    print(f"  Client Timestamp: {log.timestamp}")
    return {"status": "logged"}