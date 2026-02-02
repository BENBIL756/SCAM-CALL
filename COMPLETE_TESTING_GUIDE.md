# Complete Testing Guide for AI Voice Detection API

## Quick Start
**Base URL:** `http://127.0.0.1:9000`  
**API Key:** `myhackathonkey123`  
**Swagger UI:** `http://127.0.0.1:9000/docs`

---

## METHOD 1: FILE UPLOAD (EASIEST)

### Endpoint URL
```
POST http://127.0.0.1:9000/api/voice-detection/upload
```

### Headers
```
x-api-key: myhackathonkey123
```

### Request Body (Form Data)
```
file: [Your MP3 file]
language: English
```

### Language Options
- English
- Tamil
- Hindi
- Malayalam
- Telugu

### Audio Format
- MP3 only

### Example Response
```json
{
  "status": "success",
  "language": "English",
  "classification": "HUMAN",
  "confidenceScore": 0.85,
  "explanation": "Natural pitch variation and human-like prosody detected"
}
```

### Test with cURL
```bash
curl -X POST "http://127.0.0.1:9000/api/voice-detection/upload" \
  -H "x-api-key: myhackathonkey123" \
  -F "file=@sample voice 1.mp3" \
  -F "language=English"
```

---

## METHOD 2: JSON REQUEST (MANUAL BASE64)

### Endpoint URL
```
POST http://127.0.0.1:9000/api/voice-detection
```

### Headers
```
x-api-key: myhackathonkey123
Content-Type: application/json
```

### Request Body
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "UklGRi4AAABUQWZF..."
}
```

### Language Options
- English
- Tamil
- Hindi
- Malayalam
- Telugu

### Audio Format
- mp3 (ONLY - do not use other formats)

### Audio Base64 Format
- Base64-encoded MP3 file content
- Do NOT include data URI prefix (no `data:audio/mp3;base64,`)
- Just the raw base64 string

### Example Response
```json
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.91,
  "explanation": "Unnatural pitch consistency and robotic speech patterns detected"
}
```

### How to Convert MP3 to Base64 (Python)
```python
import base64

with open("sample voice 1.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')
    print(audio_base64)
```

---

## ERROR RESPONSES

### 401 Unauthorized (Missing or Wrong API Key)
```
Status Code: 401
Response:
{
  "detail": {
    "status": "error",
    "message": "Invalid API key or malformed request"
  }
}
```

**How to Fix:**
- Add header: `x-api-key: myhackathonkey123`
- Make sure the key is spelled correctly

### 422 Unprocessable Entity (Invalid Language)
```
Status Code: 422
Response:
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "language"],
      "msg": "Unsupported language. Choose from: Tamil, English, Hindi, Malayalam, Telugu."
    }
  ]
}
```

**How to Fix:**
- Use only: Tamil, English, Hindi, Malayalam, or Telugu
- Check spelling

### 422 Unprocessable Entity (Invalid Audio Format)
```
Status Code: 422
Response:
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "audioFormat"],
      "msg": "Only MP3 format is supported"
    }
  ]
}
```

**How to Fix:**
- Use only MP3 files
- Set audioFormat to "mp3"

---

## USING SWAGGER UI

1. Go to: `http://127.0.0.1:9000/docs`
2. Click on `/api/voice-detection/upload` endpoint
3. Click **"Try it out"**
4. Upload your MP3 file
5. Enter language: `English` (or other language)
6. Scroll down to find `x-api-key` header field
7. Enter: `myhackathonkey123`
8. Click **Execute**
9. See response with classification (AI_GENERATED or HUMAN)

---

## TEST SCENARIOS

### Test 1: Upload Your Sample Voice
```
File: sample voice 1.mp3
Language: English
Expected: HUMAN or AI_GENERATED classification
```

### Test 2: Test All Languages
```
File: sample voice 1.mp3
Languages to test: Tamil, English, Hindi, Malayalam, Telugu
Expected: Same file should return same classification for all languages
```

### Test 3: Missing API Key
```
Endpoint: /api/voice-detection/upload
No header: x-api-key
Expected: 401 Unauthorized
```

### Test 4: Wrong API Key
```
Header: x-api-key: wrong_key
Expected: 401 Unauthorized
```

### Test 5: Invalid Language
```
Language: Chinese
Expected: 422 Unprocessable Entity
```

---

## EXPECTED CLASSIFICATIONS

### AI_GENERATED
- Confidence: 0.91
- Characteristics: Unnatural pitch consistency, robotic speech patterns
- Explanation: "Unnatural pitch consistency and robotic speech patterns detected"

### HUMAN
- Confidence: 0.85
- Characteristics: Natural pitch variation, human-like prosody
- Explanation: "Natural pitch variation and human-like prosody detected"

---

## TESTING TOOLS AVAILABLE

### 1. Interactive Python Tool
```bash
python test_your_voice.py
```
Menu options:
1. Test with provided test_audio.wav
2. Test with your own MP3 file
3. Batch test all 5 languages
4. Exit

### 2. Direct cURL Command
```bash
curl -X POST "http://127.0.0.1:9000/api/voice-detection/upload" \
  -H "x-api-key: myhackathonkey123" \
  -F "file=@sample voice 1.mp3" \
  -F "language=English"
```

### 3. Swagger UI
```
http://127.0.0.1:9000/docs
```

### 4. Python Requests Script
```python
import requests

files = {"file": open("sample voice 1.mp3", "rb")}
data = {"language": "English"}
headers = {"x-api-key": "myhackathonkey123"}

r = requests.post(
    "http://127.0.0.1:9000/api/voice-detection/upload",
    files=files,
    data=data,
    headers=headers
)

print(r.json())
```

---

## CHECKLIST FOR TESTING

- [ ] Server is running on port 9000
- [ ] `/ready` endpoint returns 200 OK
- [ ] `/` endpoint returns 200 OK
- [ ] File upload endpoint works with valid API key
- [ ] File upload returns 401 without API key
- [ ] JSON endpoint works with all 5 languages
- [ ] Classification shows HUMAN or AI_GENERATED
- [ ] Confidence score is between 0 and 1
- [ ] Swagger UI is accessible at /docs
- [ ] All endpoints documented in OpenAPI schema
- [ ] Error responses return correct status codes
- [ ] Invalid language returns 422
- [ ] Sample voice file classifies correctly

---

## STATUS CODES REFERENCE

| Code | Meaning | When It Occurs |
|------|---------|----------------|
| 200 | Success | Valid request with correct API key |
| 401 | Unauthorized | Missing or wrong API key |
| 422 | Unprocessable Entity | Invalid language or format |
| 500 | Server Error | Audio processing failed |

---

## IMPORTANT NOTES

1. **API Key Required:** All requests must include `x-api-key: myhackathonkey123` header
2. **MP3 Only:** Only MP3 audio files are supported
3. **File Size:** No specific limit, but typical voice clips are <5MB
4. **Language:** Must match one of the 5 supported languages exactly
5. **Response:** Always includes `status`, `language`, `classification`, `confidenceScore`, and `explanation`

---

## PRODUCTION DEPLOYMENT

Before deploying to production:
1. Change API_KEY from `myhackathonkey123` to a secure random key
2. Update environment variables if needed
3. Test all endpoints with the new API key
4. Ensure server is running on appropriate port
5. Add HTTPS/SSL certificate
6. Monitor logs for errors

---

**Last Updated:** February 2, 2026  
**API Version:** 1.0  
**Status:** Production Ready
