#!/usr/bin/env python3
"""Test the API"""
import time
import requests
import json

time.sleep(3)

# Test /ready endpoint
try:
    r = requests.get('http://localhost:8001/ready')
    print("[PASS] /ready endpoint: Status " + str(r.status_code))
    print("  Response: " + str(r.json()))
except Exception as e:
    print("[FAIL] /ready endpoint: " + str(e))

# Test / endpoint
try:
    r = requests.get('http://localhost:8001/')
    print("[PASS] / endpoint: Status " + str(r.status_code))
    print("  Response: " + str(r.json()))
except Exception as e:
    print("[FAIL] / endpoint: " + str(e))

# Test /detect endpoint with file
try:
    with open('test_audio.wav', 'rb') as f:
        files = {'file': ('test_audio.wav', f, 'audio/wav')}
        headers = {'x-api-key': 'myhackathonkey123'}
        r = requests.post('http://localhost:8001/detect', headers=headers, files=files)
        print("[PASS] /detect endpoint: Status " + str(r.status_code))
        print("  Response: " + str(r.json()))
except Exception as e:
    print("[FAIL] /detect endpoint: " + str(e))

print("\nAll tests completed!")

