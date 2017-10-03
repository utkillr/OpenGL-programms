
import numpy as np

import Wave


class Surface(object):

    def __init__(self, size=(100, 100), nwave=5):
        assert isinstance(size, tuple)

        self.size = size

        # retrieve nwave random waves and store it
        self.waves = []
        for each in range(nwave):
            self.waves.append(Wave.random_wave(nwave))

    def position(self):
        x, y = self.coords()

        # last 2 is to store 2d coords of each point
        shape = (self.size[0], self.size[1], 2)
        grid = self.empty_arr(shape)

        # grid[i][j].x = x[i][0]
        grid[..., 0] = x
        # grid[i][j].y = y[0][j]
        grid[..., 1] = y
        return grid

    def coords(self):
        # N x 1 array
        x = np.linspace(-1, 1, self.size[0])[:, np.newaxis]
        # 1 x N array
        y = np.linspace(-1, 1, self.size[1])[np.newaxis, :]

        return x, y

    def empty_arr(self, shape):
        # each cell equals 0
        return np.zeros(shape, dtype=np.float32)

    def height(self, time=0):
        x, y = self.coords()
        height = self.empty_arr(self.size)

        # counts height contribution of each wave for each pixel
        for wave in self.waves:
            height[:, :] += wave.amplitude * \
                            np.cos(wave.phase +
                                   x * wave.wave_vector[0] +
                                   y * wave.wave_vector[1] +
                                   time * wave.angular_frequency)

        return height

    def wireframe(self):
        # generates array with 2 cells
        # first cell is 2D array with x of each cell of original NxM array
        # for N = 3, M = 3 it's [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
        # second - y
        # for N = 3, M = 3 it's [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
        left = np.indices((self.size[0] - 1, self.size[1]))
        # creates array [[[1]], [[0]]]
        # that way, for each x we add 1, for each y we add 0
        right = left + np.array([1, 0])[:, np.newaxis, np.newaxis]

        horizontal = self.make_pairs(left, right, self.size)

        # same for vertical lines
        bottom = np.indices((self.size[0], self.size[1]-1))
        top = bottom + np.array([0, 1])[:, np.newaxis, np.newaxis]
        vertical = self.make_pairs(bottom, top, self.size)

        return np.concatenate((horizontal, vertical), axis=0).astype(np.uint32)

    @staticmethod
    def make_pairs(pts1, pts2, size):
        # convert 3D array to 2D array of [[all x], [all y]]
        # -1 means that length is inferred from the length of original array
        pts1 = pts1.reshape((2, -1))
        pts2 = pts2.reshape((2, -1))

        # from 2D NxM array get 1D array, where arr[i * M + j] = old[i][j]
        pts1 = np.ravel_multi_index(pts1, size)
        pts2 = np.ravel_multi_index(pts2, size)

        # For both arrays make 2D array, where each inner array contains single number from the original one
        # Concatenate arrays so there will be [[l0, r0], ..., [li, ri]] array
        return np.concatenate((pts1[..., np.newaxis], pts2[..., np.newaxis]), axis=-1)


