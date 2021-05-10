import numpy as np
from scipy.io import wavfile
from collections import namedtuple

import os
import sys
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(SOURCE_DIR))
sys.path.insert(0,root)

# https://en.wikipedia.org/wiki/44,100_Hz
SAMPLE_RATE = 44100

WAV = namedtuple('WAV', ['r', 'l'])
WAV.__doc__ = '''\
Sound wave sample

- r (np.ndarray): NumPy array of samples of the right channel.
- l (np.ndarray): NumPy array of samples of the left channel.
'''


def wave(f:float, a:float, t:float) -> np.ndarray:
    """Generate the samples of a sound wave.

    Args:
        f (float): Frequency of the sound wave.
        a (float): Amplitude of the sound wave.
        t (float): Duration (seconds) of the sound wave.

    Returns:
        np.ndarray: NumPy array with sample points of wave.
    """
    sample_points = np.linspace(0, t*(2*np.pi), int(t*SAMPLE_RATE))
    return a*np.sin(sample_points*f)


def wave_sequence(frequencies:np.ndarray, t) -> WAV:
    """Return a Wav sound which iterates through the given frequencies.

    Args:
        frequencies (np.ndarray): frequencies to iterate through.
        t ([type]): duration of iteration.

    Returns:
        WAV: Wav file.
    """
    d = t / len(frequencies)
    w = np.array([list(wave(f,1,d)) for f in frequencies]).flatten()
    return WAV(r=w, l=w)


def write(file_name:str, wave:WAV):
    """Write a .wav file.

    Args:
        file_name (str): Name of the .wav file to be written.
        wave (WAV): Wav file to write.
    """
    wavfile.write(file_name, SAMPLE_RATE, np.array([wave.r, wave.l]).T)
