#!/usr/bin/env python3
"""Test only - assumes server is already running"""
import time
import requests
import json
import sys

def main():
    time.sleep(2)
    
    print("="*60)
    print("RUNNING API TESTS")
    print("="*60)
    
    base_url = 'http://127.0.0.1:9000'
    all_passed = True
    
    # Test 1: /ready endpoint
    try:
        r = requests.get(base_url + '/ready', timeout=5)
        status = "PASS" if r.status_code == 200 else "FAIL"
        print("[" + status + "] GET /ready")
        print("  Status: " + str(r.status_code))
        print("  Response: " + str(r.json()))
        if status == "FAIL":
            all_passed = False
    except Exception as e:
        print("[FAIL] GET /ready")
        print("  Error: " + str(e))
        all_passed = False

    print()

    # Test 2: / endpoint
    try:
        r = requests.get(base_url + '/', timeout=5)
        status = "PASS" if r.status_code == 200 else "FAIL"
        print("[" + status + "] GET /")
        print("  Status: " + str(r.status_code))
        print("  Response: " + str(r.json()))
        if status == "FAIL":
            all_passed = False
    except Exception as e:
        print("[FAIL] GET /")
        print("  Error: " + str(e))
        all_passed = False

    print()

    # Test 3: /detect endpoint with file
    try:
        with open('test_audio.wav', 'rb') as f:
            files = {'file': ('test_audio.wav', f, 'audio/wav')}
            headers = {'x-api-key': 'myhackathonkey123'}
            r = requests.post(base_url + '/detect', headers=headers, files=files, timeout=10)
            status = "PASS" if r.status_code == 200 else "FAIL"
            print("[" + status + "] POST /detect")
            print("  Status: " + str(r.status_code))
            resp = r.json()
            print("  Classification: " + resp.get('classification', 'N/A'))
            print("  Confidence: " + str(resp.get('confidence', 'N/A')))
            if status == "FAIL":
                all_passed = False
    except Exception as e:
        print("[FAIL] POST /detect")
        print("  Error: " + str(e))
        all_passed = False

    print()
    print("="*60)
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
