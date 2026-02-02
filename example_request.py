#!/usr/bin/env python3
"""Example client for the AI Generated Voice Detection API.

Usage:
  python example_request.py --file path/to/audio.mp3
  python example_request.py --base64 path/to/audio.mp3

"""
import argparse
import base64
import requests
import sys

URL = "http://127.0.0.1:8001/detect"
API_KEY = "myhackathonkey123"


def do_upload(file_path: str):
    with open(file_path, "rb") as f:
        files = {"file": (file_path.split("/")[-1], f, "audio/mpeg")}
        headers = {"x-api-key": API_KEY}
        resp = requests.post(URL, headers=headers, files=files)
        print(resp.status_code)
        print(resp.text)


def do_base64(file_path: str, language: str = "en"):
    with open(file_path, "rb") as f:
        b = f.read()
        b64 = base64.b64encode(b).decode("ascii")
        payload = {"audio_base64": b64, "language": language}
        headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
        resp = requests.post(URL, headers=headers, json=payload)
        print(resp.status_code)
        print(resp.text)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", help="Path to audio file to upload (multipart)")
    p.add_argument("--base64", help="Path to audio file to send as base64 JSON")
    p.add_argument("--language", default="en")
    args = p.parse_args()

    if args.file:
        do_upload(args.file)
    elif args.base64:
        do_base64(args.base64, args.language)
    else:
        print("Specify --file or --base64")
        sys.exit(2)
