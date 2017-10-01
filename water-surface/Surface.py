
import numpy as np

class Surface(object):

    def __init__(self, size=(100, 100)):
        self.size = size

        shape = (self.size[0], self.size[1], 2)
        self.grid = np.zeros(shape, dtype=np.float32)

    def position(self):
        x = np.linspace(-1, 1, self.size[0])
        y = np.linspace(-1, 1, self.size[1])

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.grid[i, j] = (x[i], y[j])

        return self.grid

    def height(self):
        line_height = np.linspace(-1, 1, self.size[0], dtype=np.float32)

        height = np.zeros(self.size, dtype=np.float32)

        for i in range(self.size[1]):
            height[i] = line_height

        return height

