#!/usr/bin/env python3
"""Send JSON base64 audio to /detect and print result"""
import base64
import json
import requests

URL = "http://127.0.0.1:9000/detect"
API_KEY = "myhackathonkey123"
AUDIO_PATH = "test_audio.wav"

with open(AUDIO_PATH, "rb") as f:
    b = f.read()
    b64 = base64.b64encode(b).decode("ascii")

payload = {"audio_base64": b64, "language": "English"}
headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

try:
    r = requests.post(URL, headers=headers, json=payload, timeout=15)
    print("Status:", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print(r.text)
except Exception as e:
    print("Request failed:", e)
