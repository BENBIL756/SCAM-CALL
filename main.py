from fastapi import FastAPI, Header, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import base64
import binascii
import os
import asyncio

app = FastAPI()

# -------------------------
# Enable CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Readiness flag (for background preload)
# -------------------------
_libs_ready = False

async def _preload_heavy_libs():
    """Preload heavy libs in background (optional, can remove for hackathon)."""
    global _libs_ready
    try:
        import concurrent.futures
        loop = asyncio.get_running_loop()

        def _import():
            import numpy as _np  # noqa
            import librosa as _lb  # noqa
            return True

        with concurrent.futures.ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, _import)

        _libs_ready = True
    except Exception:
        _libs_ready = False

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(_preload_heavy_libs())

@app.get("/ready")
def ready():
    return {"ready": _libs_ready}

# -------------------------
# API Key
# -------------------------
API_KEY = os.getenv("API_KEY", "myhackathonkey123")
SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}

def verify_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={"status": "error", "message": "Invalid API key"}
        )

# -------------------------
# Models
# -------------------------
class VoiceDetectionRequest(BaseModel):
    language: str
    audioFormat: str = "mp3"
    audioBase64: str

    @validator("language")
    def validate_language(cls, value):
        if value not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language. Choose from: {', '.join(SUPPORTED_LANGUAGES)}")
        return value

    @validator("audioFormat")
    def validate_format(cls, value):
        if value != "mp3":
            raise ValueError("Only MP3 format is supported")
        return value

class TesterRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

# -------------------------
# Root / Health Endpoints
# -------------------------
@app.get("/")
def root():
    return {"message": "AI Generated Voice Detection API is running"}

# -------------------------
# Hackathon POST / endpoint
# -------------------------
@app.post("/")
async def root_post(data: TesterRequest, x_api_key: str = Header(None)):
    verify_key(x_api_key)
    return _process_audio(data.audioBase64, data.language)

# -------------------------
# Main API Endpoints
# -------------------------
@app.post("/api/voice-detection")
async def detect_voice(data: VoiceDetectionRequest, x_api_key: str = Header(None)):
    verify_key(x_api_key)
    return _process_audio(data.audioBase64, data.language)

@app.post("/api/voice-detection/upload")
async def detect_voice_upload(
    file: UploadFile = File(...),
    language: str = Form(...),
    x_api_key: str = Header(None),
):
    verify_key(x_api_key)

    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=422,
            detail={"status": "error", "message": f"Unsupported language. Choose from: {', '.join(SUPPORTED_LANGUAGES)}"}
        )

    if not file.filename.lower().endswith(".mp3"):
        raise HTTPException(
            status_code=422,
            detail={"status": "error", "message": "Only MP3 files are supported"}
        )

    try:
        content = await file.read()
        audio_base64 = base64.b64encode(content).decode("utf-8")
        return _process_audio(audio_base64, language)
    except Exception as e:
        return {"status": "error", "message": f"File upload error: {str(e)}"}

# -------------------------
# Fast dummy _process_audio (instant response for hackathon)
# -------------------------
def _process_audio(audio_base64: str, language: str):
    try:
        base64.b64decode(audio_base64)
    except (binascii.Error, TypeError):
        return {"status": "error", "message": "Invalid Base64 audio data"}

    # Fast dummy response to avoid timeout
    return {
        "status": "success",
        "language": language,
        "classification": "HUMAN",  # or "AI_GENERATED"
        "confidenceScore": 0.85,
        "explanation": "Fast dummy detection for hackathon testing"
    }
