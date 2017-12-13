import numpy as np


class Base:

    def __init__(self, v=10, delta=0.1, sigma=0.1, size=(50, 50), start_h=2, borders=False):
        self.v = v
        self.delta = delta
        self.sigma = sigma
        self.size = size
        self.start_h = start_h
        self.borders = borders

    def init_h(self):
        h = np.ones(self.size, dtype=np.float32) * 0.2
        h[self.size[0] // 2, self.size[1] // 2] = self.start_h
        h[self.size[0] // 2 + 1, self.size[1] // 2] = self.start_h
        h[self.size[0] // 2, self.size[1] // 2 + 1] = self.start_h
        h[self.size[0] // 2 + 1, self.size[1] // 2 + 1] = self.start_h
        return h

    # f([h, v]) = [v, h'']
    def f(self, x):
        up = x[0]
        down = x[1]
        return np.array([down, self.derivative(up)])

    # h'' = Ldh
    def derivative(self, heights):
        der_heights = np.zeros(self.size, dtype=np.float32)

        min_i = 0
        min_k = 0
        max_i = self.size[0]
        max_k = self.size[1]

        if self.borders:
            max_i -= 1
            max_k -= 1
            min_i += 1
            min_k += 1

        for i in range(min_i, max_i):
            for k in range(min_k, max_k):
                left = heights[i][(k - 1 + self.size[1]) % self.size[1]]
                right = heights[i][(k + 1) % self.size[1]]
                up = heights[(i - 1 + self.size[0]) % self.size[0]][k]
                down = heights[(i + 1) % self.size[0]][k]
                this = heights[i][k]
                der_heights[i][k] = ((self.v ** 2) * (self.sigma ** 2) / (self.delta ** 2)) * (left + right + up + down - 4 * this)

        return der_heights


    def get_heights(self, h, h_der):
        pass

    def get_normal(self, heights):
        normal = np.zeros((self.size[0], self.size[1], 2), dtype=np.float32)
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                left = heights[i][(j - 1 + self.size[1]) % self.size[1]]
                right = heights[i][(j + 1) % self.size[1]]
                up = heights[(i - 1 + self.size[0]) % self.size[0]][j]
                down = heights[(i + 1) % self.size[0]][j]

                normal[i][j][0] = (left + right) / (2 * self.delta)
                normal[i][j][1] = (up + down) / (2 * self.delta)

        return normal
