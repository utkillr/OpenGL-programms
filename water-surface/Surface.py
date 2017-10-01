
import numpy as np

import Wave


class Surface(object):

    def __init__(self, size=(100, 100), nwave=5):
        self.size = size

        self.waves = []
        for each in range(nwave):
            self.waves.append(Wave.random_wave(nwave))

        shape = (self.size[0], self.size[1], 2)
        self.grid = np.zeros(shape, dtype=np.float32)

    def position(self):
        x = np.linspace(-1, 1, self.size[0])
        y = np.linspace(-1, 1, self.size[1])

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.grid[i, j] = (x[i], y[j])

        return self.grid

    def height(self, time=0):
        height = np.zeros(self.size, dtype=np.float32)
        x = np.linspace(-1, 1, self.size[0])[:, None]
        y = np.linspace(-1, 1, self.size[1])[None, :]

        for wave in self.waves:
            height[:, :] += wave.amplitude * \
                            np.cos(wave.phase +
                                   x * wave.wave_vector[0] +
                                   y * wave.wave_vector[1] +
                                   time * wave.angular_frequency)

        return height

