#!/usr/bin/env python3
"""Test script for sample voice 1.mp3"""

import base64
import requests
import json

# API Configuration
API_URL = "http://127.0.0.1:9000/api/voice-detection"
API_KEY = "myhackathonkey123"
AUDIO_FILE = "sample voice 1.mp3"

print(f"\n{'='*60}")
print(f"Testing: {AUDIO_FILE}")
print(f"{'='*60}\n")

try:
    # Read and encode audio file
    with open(AUDIO_FILE, "rb") as f:
        audio_data = f.read()
    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    
    # Prepare request
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    # Send request
    print(f"Sending audio to API...")
    response = requests.post(API_URL, json=payload, headers=headers)
    
    # Display result
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Classification: {data.get('classification')}")
        print(f"✓ Confidence: {data.get('confidenceScore')}")
        print(f"✓ Explanation: {data.get('explanation')}")
    
except FileNotFoundError:
    print(f"❌ Error: File '{AUDIO_FILE}' not found!")
except requests.exceptions.ConnectionError:
    print(f"❌ Error: Cannot connect to API at {API_URL}")
    print("Make sure the server is running on port 9000")
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\n{'='*60}\n")
