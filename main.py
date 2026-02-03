from fastapi import FastAPI, Header, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import base64
import binascii
import tempfile
import asyncio
from typing import Optional
import os

app = FastAPI()

# Enable CORS for all origins (allow HTML pages to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Readiness flag updated after background preload
_libs_ready = False

async def _preload_heavy_libs():
    """Background task to import heavy libs so first real request is faster."""
    global _libs_ready
    try:
        import concurrent.futures
        loop = asyncio.get_running_loop()

        def _import():
            import numpy as _np  # noqa: F401
            import librosa as _lb  # noqa: F401
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

API_KEY = os.getenv("API_KEY", "myhackathonkey123")
SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}

# ---------------------
# Request Models
# ---------------------
class VoiceDetectionRequest(BaseModel):
    language: str
    audioFormat: str = "mp3"
    audioBase64: str

    @validator("language")
    def validate_language(cls, value):
        if value not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language. Choose from: {', '.join(SUPPORTED_LANGUAGES)}."
            )
        return value

    @validator("audioFormat")
    def validate_format(cls, value):
        if value != "mp3":
            raise ValueError("Only MP3 format is supported")
        return value

# Model for hackathon tester
class TesterRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

# ---------------------
# Helper Functions
# ---------------------
def verify_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={"status": "error", "message": "Invalid API key or malformed request"}
        )

def _process_audio(audio_base64: str, language: str):
    try:
        audio_bytes = base64.b64decode(audio_base64)
    except (binascii.Error, TypeError):
        return {"status": "error", "message": "Invalid Base64 audio data"}

    try:
        import numpy as np
        import librosa

        # Save bytes to a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_path = temp_file.name
        temp_file.write(audio_bytes)
        temp_file.close()
        
        try:
            y, sr = librosa.load(temp_path, sr=None)
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass

        # Simple heuristics for AI vs Human detection
        pitch = librosa.yin(y, fmin=50, fmax=300)
        pitch_variation = float(np.std(pitch)) if hasattr(pitch, '__len__') else float(pitch)
        energy_variation = float(np.std(y))

        if pitch_variation < 10 and energy_variation < 0.01:
            classification = "AI_GENERATED"
            confidence_score = 0.91
            explanation = "Unnatural pitch consistency and robotic speech patterns detected"
        else:
            classification = "HUMAN"
            confidence_score = 0.85
            explanation = "Natural pitch variation and human-like prosody detected"

        return {
            "status": "success",
            "language": language,
            "classification": classification,
            "confidenceScore": confidence_score,
            "explanation": explanation
        }

    except Exception as e:
        return {"status": "error", "message": f"Audio processing error: {str(e)}"}

# ---------------------
# Root / Health Endpoints
# ---------------------
@app.get("/")
def root():
    return {"message": "AI Generated Voice Detection API is running"}

# ---------------------
# Hackathon Tester Endpoint (POST /)
# ---------------------
@app.post("/")
async def root_post(data: TesterRequest, x_api_key: str = Header(None)):
    """
    POST / root endpoint for hackathon tester.
    """
    verify_key(x_api_key)
    return _process_audio(data.audioBase64, data.language)

# ---------------------
# Main API Endpoints
# ---------------------
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
            detail={
                "status": "error",
                "message": f"Unsupported language. Choose from: {', '.join(SUPPORTED_LANGUAGES)}"
            }
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
