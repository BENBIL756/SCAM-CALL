#!/usr/bin/env python3
"""
Custom Voice Testing Tool
Upload your own voice sample and test AI vs Human detection
"""

import requests
import base64
import json
import os
from pathlib import Path

BASE_URL = "http://127.0.0.1:9000"
API_KEY = "myhackathonkey123"

def load_audio_file(file_path):
    """Load audio file and encode to base64"""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        return None
    
    try:
        with open(file_path, 'rb') as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        return audio_base64
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def test_voice(file_path, language):
    """Send audio to API and get classification"""
    audio_base64 = load_audio_file(file_path)
    if not audio_base64:
        return None
    
    request_body = {
        "language": language,
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    print(f"\nTesting: {file_path}")
    print(f"Language: {language}")
    print("-" * 60)
    
    try:
        r = requests.post(
            f"{BASE_URL}/api/voice-detection",
            headers={"x-api-key": API_KEY, "Content-Type": "application/json"},
            json=request_body,
            timeout=15
        )
        
        if r.status_code == 200:
            resp = r.json()
            if resp.get("status") == "success":
                print(f"Status: SUCCESS")
                print(f"Classification: {resp['classification']}")
                print(f"Confidence Score: {resp['confidenceScore']}")
                print(f"Explanation: {resp['explanation']}")
                print(f"Language Detected: {resp['language']}")
                return resp
            else:
                print(f"Error: {resp.get('message', 'Unknown error')}")
                return None
        else:
            print(f"HTTP Error {r.status_code}")
            print(r.text)
            return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def main():
    print("=" * 70)
    print("CUSTOM VOICE DETECTION TOOL")
    print("=" * 70)
    
    # List of supported languages
    languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    
    print("\nSupported Languages:")
    for i, lang in enumerate(languages, 1):
        print(f"  {i}. {lang}")
    
    # Interactive mode
    while True:
        print("\n" + "=" * 70)
        print("Options:")
        print("  1. Test with test_audio.wav")
        print("  2. Test your own MP3 file")
        print("  3. Batch test all languages (using test_audio.wav)")
        print("  4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            lang = input("Enter language (Tamil/English/Hindi/Malayalam/Telugu): ").strip()
            if lang in languages:
                test_voice("test_audio.wav", lang)
            else:
                print("Invalid language!")
        
        elif choice == "2":
            file_path = input("Enter path to your MP3 file: ").strip()
            lang = input("Enter language (Tamil/English/Hindi/Malayalam/Telugu): ").strip()
            if lang in languages:
                test_voice(file_path, lang)
            else:
                print("Invalid language!")
        
        elif choice == "3":
            print("\nTesting all languages with test_audio.wav...")
            for lang in languages:
                result = test_voice("test_audio.wav", lang)
                if result:
                    input("Press Enter to continue...")
        
        elif choice == "4":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
