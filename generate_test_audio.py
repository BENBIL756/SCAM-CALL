import numpy as np
import soundfile as sf

sr = 22050
t = np.linspace(0,1,sr,endpoint=False)
# simple sine wave 220 Hz
y = 0.1 * np.sin(2*np.pi*220*t)
sf.write('test_audio.wav', y, sr)
print('Wrote test_audio.wav (1s 220Hz)')
