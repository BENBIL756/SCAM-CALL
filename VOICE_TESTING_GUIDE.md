# How to Test Your Own Voice Sample

## Step 1: Prepare Your Voice Sample

You need an **MP3 audio file** with your own voice. Here are your options:

### Option A: Record Using Your Computer
```bash
# On Windows, use built-in Voice Recorder
# Search for "Voice Recorder" -> Click Record -> Save as MP3
```

### Option B: Use Online Tools
- **Google Recorder** (converts to MP3)
- **Audacity** (free audio editor, export to MP3)
- **Voice Memo** (on Mac/Phone, then convert)

### Option C: Download from Provided Link
From the problem statement, download the sample voice from the Drive link provided

---

## Step 2: Run the Testing Tool

### Automatic Interactive Tool:
```bash
python test_your_voice.py
```

This will:
- Show a menu with options
- Let you test with test_audio.wav (synthetic)
- Let you test with your own MP3 file
- Batch test all 5 languages

---

## Step 3: Manual Testing (cURL)

If you have your MP3 file, encode it to Base64:

**On Windows PowerShell:**
```powershell
$audioBase64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes('C:\path\to\your\voice.mp3'))
```

**Then use cURL:**
```bash
curl -X POST http://127.0.0.1:9000/api/voice-detection ^
  -H "x-api-key: myhackathonkey123" ^
  -H "Content-Type: application/json" ^
  -d "{\"language\":\"English\",\"audioFormat\":\"mp3\",\"audioBase64\":\"$audioBase64\"}"
```

---

## Step 4: Understanding the Response

### Success Response:
```json
{
  "status": "success",
  "language": "English",
  "classification": "HUMAN",
  "confidenceScore": 0.85,
  "explanation": "Natural pitch variation and human-like prosody detected"
}
```

**Classification Types:**
- **HUMAN** - Real human voice (natural pitch & energy variation)
- **AI_GENERATED** - Synthetic/AI voice (robotic patterns detected)

**Confidence Score:**
- 0.0 - 1.0 scale
- Higher = more confident in classification
- 0.85+ = High confidence

---

## Step 5: Test Results Interpretation

| Classification | What It Means |
|---|---|
| **HUMAN** (0.75-0.95) | Your voice sounds natural and human |
| **AI_GENERATED** (0.85-0.95) | Your voice sounds synthetic or AI-made |

The algorithm checks:
- ✓ Pitch consistency (AI = too consistent, HUMAN = natural variation)
- ✓ Energy variation (AI = robotic, HUMAN = natural)
- ✓ Speech patterns (AI = unnatural, HUMAN = natural)

---

## Step 6: Test with All 5 Languages

The API supports:
1. **Tamil** - தமிழ்
2. **English** - English
3. **Hindi** - हिन्दी
4. **Malayalam** - മലയാളം
5. **Telugu** - తెలుగు

Test your voice in any of these languages by changing the language parameter.

---

## Example: Full Test Session

```bash
# 1. Run interactive tool
python test_your_voice.py

# 2. Select option 2 (Test your own file)
# 3. Enter path: C:\Users\benbi\voice.mp3
# 4. Select language: English
# 5. Get result: HUMAN / AI_GENERATED with confidence score
```

---

## Troubleshooting

### "File not found"
- Make sure your MP3 file path is correct
- Use absolute path: `C:\Users\benbi\Downloads\my_voice.mp3`

### "Invalid API key"
- API Key must be: `myhackathonkey123`
- Make sure header includes: `-H "x-api-key: myhackathonkey123"`

### "Audio processing error"
- File must be valid MP3 format
- File must contain audio data (not empty)
- Try converting with Audacity if issues persist

### API not responding
- Make sure server is running: Check if you see "Uvicorn running on http://127.0.0.1:9000"
- If not, restart: `python -m uvicorn main:app --host 127.0.0.1 --port 9000`

---

## Ready to Submit?

Once you've tested your voice and confirmed the API works:
1. Ensure server is running on port 9000
2. API endpoint is: `POST http://127.0.0.1:9000/api/voice-detection`
3. All 5 languages are supported
4. Authentication working (API key validation)
5. Response format matches specification exactly

You're ready to submit!
