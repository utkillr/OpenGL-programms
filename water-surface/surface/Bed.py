from surface.Surface import Surface
import numpy as np


class Bed(object):
    def __init__(self):
        super().__init__()
        self.random_wave_surface = Surface((100, 100), 5, 0.3).normal(0)[:, :, 0]

    def new_random_surface(self):
        self.random_wave_surface = Surface((100, 100), 5, 0.3).normal(0)[:, :, 0]

    def bed_depths(self, shape):
        depths = np.ndarray([100, 100], dtype=np.float32)
        if shape == "straight":
            for i in range(depths.shape[0]):
                for j in range(depths.shape[1]):
                    if i <= 19:
                        depths[i][j] = 1
                    elif i >= 80:
                        depths[i][j] = 5
                    else:
                        depths[i][j] = (i - 20) * 4 / 58 + 1

        if shape == "random":
            depths = self.random_wave_surface

        if shape == "linspace":
            depths = np.linspace(-1.2, -0.6, 10000, dtype=np.float32).reshape([100, 100])

        if shape == "beach":
            depths = np.linspace(-0.3, 0.3, 10000, dtype=np.float32).reshape([100, 100])

        return depths