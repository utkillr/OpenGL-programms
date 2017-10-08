
import numpy as np


class Wave(object):

    def __init__(self, wave_vector, angular_frequency, phase, amplitude):
        self.wave_vector = wave_vector
        self.angular_frequency = angular_frequency
        self.phase = phase
        self.amplitude = amplitude


def random_wave(amplitude_normalization, max_height=0.2):
    wave_vector = 5 * (2 * np.random.rand(2) - 1)
    angular_frequency = 3 * np.random.rand()
    phase = 2 * np.pi * np.random.rand()
    amplitude = max_height * np.random.rand() / amplitude_normalization

    return Wave(wave_vector, angular_frequency, phase, amplitude)
