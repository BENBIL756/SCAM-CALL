#!/usr/bin/env python3
"""Run the full test suite with server and client"""
import subprocess
import time
import requests
import sys
import threading
import random

PORT = random.randint(8100, 8999)

def run_server():
    """Run the FastAPI server"""
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn',
            'main:app',
            '--host', '127.0.0.1',
            '--port', str(PORT),
            '--log-level', 'info'
        ])
    except KeyboardInterrupt:
        pass

def run_tests():
    """Run the test suite"""
    time.sleep(3)
    
    print("\n" + "="*50)
    print("RUNNING API TESTS")
    print("="*50)
    
    base_url = f'http://127.0.0.1:{PORT}'
    
    # Test /ready endpoint
    try:
        r = requests.get(base_url + '/ready')
        print("[PASS] GET /ready - Status " + str(r.status_code))
        print("  Response: " + str(r.json()))
    except Exception as e:
        print("[FAIL] GET /ready - " + str(e))
        return False

    # Test / endpoint
    try:
        r = requests.get(base_url + '/')
        print("[PASS] GET / - Status " + str(r.status_code))
        print("  Response: " + str(r.json()))
    except Exception as e:
        print("[FAIL] GET / - " + str(e))
        return False

    # Test /detect endpoint with file
    try:
        with open('test_audio.wav', 'rb') as f:
            files = {'file': ('test_audio.wav', f, 'audio/wav')}
            headers = {'x-api-key': 'myhackathonkey123'}
            r = requests.post(base_url + '/detect', headers=headers, files=files)
            print("[PASS] POST /detect - Status " + str(r.status_code))
            resp_json = r.json()
            print("  Classification: " + resp_json.get('classification', 'N/A'))
            print("  Confidence: " + str(resp_json.get('confidence', 'N/A')))
    except Exception as e:
        print("[FAIL] POST /detect - " + str(e))
        return False

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)
    return True

if __name__ == '__main__':
    # Start server in a thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Run tests in main thread
    success = run_tests()
    
    sys.exit(0 if success else 1)

