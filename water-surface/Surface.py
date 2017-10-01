
import numpy as np

import Wave


class Surface(object):

    def __init__(self, size=(100, 100), nwave=5):
        self.size = size

        self.waves = []
        for each in range(nwave):
            self.waves.append(Wave.random_wave(nwave))

    def position(self):
        x, y = self.coords()

        shape = (self.size[0], self.size[1], 2)
        grid = self.empty_arr(shape)

        grid[..., 0] = x
        grid[..., 1] = y
        return grid

    def coords(self):
        x = np.linspace(-1, 1, self.size[0])[:, None]
        y = np.linspace(-1, 1, self.size[1])[None, :]

        return x, y

    def empty_arr(self, shape):
        return np.zeros(shape, dtype=np.float32)

    def height(self, time=0):
        x, y = self.coords()
        height = self.empty_arr(self.size)

        for wave in self.waves:
            height[:, :] += wave.amplitude * \
                            np.cos(wave.phase +
                                   x * wave.wave_vector[0] +
                                   y * wave.wave_vector[1] +
                                   time * wave.angular_frequency)

        return height

