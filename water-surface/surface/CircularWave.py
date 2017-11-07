
import numpy as np


class CircularWave:
    def __init__(self, amplitude, omega, center, speed):
        self.amplitude = amplitude
        self.omega = omega
        self.center = center
        self.speed = speed


def random_wave(max_height=0.1, wave_length=0.3, center=(0., 0.), speed=3):
    amplitude = max_height
    omega = 2 * np.pi / wave_length
    center = np.asarray(center, dtype=np.float32)
    speed = speed

    return CircularWave(amplitude, omega, center, speed)