import numpy as np
import time

def get_sin_wave_amplitude(freq, time):
    raw_amp = np.sin(2*np.pi*freq*time)
    shifted_amp = raw_amp + 1
    normalized_amp = shifted_amp/2
    return normalized_amp

def wait_for_sampling_period(sampling_frequency):
    T = (sampling_frequency)**(-1)
    time.sleep(T)