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
    try:
        print(f"[{datetime.now()}] Generando TTS para: {req.text[:50]}...")
        wav_path = synthesize(req.text)
        print(f"[{datetime.now()}] Archivo generado: {wav_path}")
        
        with open(wav_path, "rb") as f:
            audio_bytes = f.read()
        
        print(f"[{datetime.now()}] Bytes leídos: {len(audio_bytes)}")
        
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/wav",
            headers={"Content-Disposition": "inline"}
        )
    except Exception as e:
        print(f"[{datetime.now()}] ERROR en /tts: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/debug-log")
def debug_log(log: DebugLog):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {log.message}")
    print(f"  User Agent: {log.userAgent}")
    print(f"  Client Timestamp: {log.timestamp}")
    return {"status": "logged"}

@app.get("/verify-wav")
def verify_wav():
    """Verifica que el último WAV generado sea válido"""
    try:
        # Generar un WAV de prueba
        wav_path = synthesize("Prueba")
        
        with open(wav_path, "rb") as f:
            data = f.read()
        
        # Verificar headers
        if data[:4] != b'RIFF':
            return {"error": "Invalid RIFF header"}
        if data[8:12] != b'WAVE':
            return {"error": "Invalid WAVE header"}
        
        riff_size = int.from_bytes(data[4:8], 'little')
        
        return {
            "status": "valid",
            "file_size": len(data),
            "riff_size": riff_size,
            "first_bytes": data[:20].hex()
        }
    except Exception as e:
        return {"error": str(e)}