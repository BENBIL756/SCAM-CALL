#!/usr/bin/env python3
"""
Simple Voice Recording Script
Records audio and saves as MP3 for testing
"""

import subprocess
import os
import sys

def record_voice_windows():
    """Open Voice Recorder app on Windows"""
    print("=" * 60)
    print("WINDOWS VOICE RECORDING GUIDE")
    print("=" * 60)
    print("""
Steps to record your voice:
1. Press Windows + R
2. Type 'soundrecorder' and press Enter
3. Click the microphone icon to start recording
4. Speak clearly in your chosen language
5. Click the stop button
6. Save the file as 'my_voice.mp3' in:
   C:\\Users\\benbi\\OneDrive\\Documents\\hackathon\\
7. Run: python test_your_voice.py
8. Select option 2 and enter: my_voice.mp3

Alternative: Use Audacity (free)
- Download from: https://www.audacityteam.org/
- Record audio
- Export as MP3 to hackathon folder
""")

def convert_wav_to_mp3(wav_file, mp3_file):
    """Convert WAV to MP3 using ffmpeg"""
    if not os.path.exists(wav_file):
        print(f"Error: {wav_file} not found")
        return False
    
    try:
        # Check if ffmpeg is installed
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        
        # Convert
        cmd = [
            "ffmpeg", "-i", wav_file, "-b:a", "192K", "-y", mp3_file
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"Converted {wav_file} to {mp3_file}")
        return True
    except FileNotFoundError:
        print("ffmpeg not found. Install from: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"Conversion error: {e}")
        return False

def main():
    print("=" * 60)
    print("VOICE RECORDING SETUP")
    print("=" * 60)
    print("""
Choose how to record your voice:

1. Use Windows Voice Recorder (recommended)
2. Use Audacity (more control)
3. Convert existing WAV to MP3
4. Exit

Note: Your voice should be:
- Clear and audible
- In one of the 5 supported languages:
  Tamil, English, Hindi, Malayalam, Telugu
- 5-30 seconds long
- Spoken naturally (not AI-generated)
""")
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        record_voice_windows()
        
    elif choice == "2":
        print("""
Install Audacity (free audio editor):
1. Go to: https://www.audacityteam.org/
2. Download and install
3. Open Audacity
4. Click microphone icon to record
5. Speak your sample (5-30 seconds)
6. File -> Export -> Export as MP3
7. Save to: C:\\Users\\benbi\\OneDrive\\Documents\\hackathon\\my_voice.mp3
8. Run: python test_your_voice.py
9. Select option 2 and test your voice
""")
        
    elif choice == "3":
        wav_file = input("Enter WAV file path: ").strip()
        mp3_file = input("Enter MP3 output path (default: my_voice.mp3): ").strip()
        if not mp3_file:
            mp3_file = "my_voice.mp3"
        
        if convert_wav_to_mp3(wav_file, mp3_file):
            print(f"\nSuccess! Now test with:")
            print(f"  python test_your_voice.py")
        
    elif choice == "4":
        print("Goodbye!")
        sys.exit(0)
    
    else:
        print("Invalid option!")

if __name__ == "__main__":
    main()
