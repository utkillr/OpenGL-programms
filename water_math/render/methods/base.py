import numpy as np
from render.methods.generator import HeightsGenerator


class Base:

    def __init__(self, method, v=100, delta=1, sigma=0.1, size=(50, 50), max_height=0.4, min_height=0.2, borders=False, is_shallow=False):
        self.method = method
        self.v = v
        self.delta = delta
        self.sigma = sigma
        self.size = size
        self.max_height = max_height
        self.min_height = min_height
        self.borders = borders
        self.is_shallow = is_shallow
        self.g = 9.81
        self.generator = HeightsGenerator(size)

        self.methods = {
            "peak":         self.generator.peak,
            "bubble":       self.generator.bubble
        }

    def init(self, max_height=0.4, min_height=0.2, part=4):
        params = {
            "max_height":   max_height,
            "min_height":   min_height,
            "part":         part
        }
        return self.methods[self.method](params)

    # f([h, v]) = [v, h'']
    def f(self, x):
        return np.array([x[1], self.derivative(x[0])])

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


    def get_heights(self, h_desc):
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

    def der_x(self, x):
        der_x = np.zeros(self.size, dtype=np.float32)

        min_i = 0
        max_i = self.size[0]

        if self.borders:
            max_i -= 1
            min_i += 1

        for i in range(min_i, max_i):
            for k in range(0, self.size[1]):
                up = x[(i + 1 + self.size[0]) % self.size[0]][k]
                this = x[i][k]
                der_x[i][k] = (up - this) / self.delta

        return der_x

    def der_y(self, y):
        der_y = np.zeros(self.size, dtype=np.float32)

        min_i = 0
        max_i = self.size[0]

        if self.borders:
            max_i -= 1
            min_i += 1

        for k in range(0, self.size[1]):
            for i in range(min_i, max_i):
                right = y[k][(i + 1) % self.size[0]]
                this = y[k][i]
                der_y[k][i] = (right - this) / self.delta

        return der_y

    def f_shallow(self, x):
        h = x[0]
        U = x[1]
        V = x[2]
        Ug = np.power(U, 2) / h + self.g * np.power(h, 2) / 2
        Vg = np.power(V, 2) / h + self.g * np.power(h, 2) / 2
        UVh = np.divide(np.multiply(U, V), h)

        der_U = self.der_x(U)
        der_V = self.der_y(V)
        der_Ug = self.der_x(Ug)
        der_Vg = self.der_y(Vg)
        der_Uh = self.der_x(UVh)
        der_Vh = self.der_y(UVh)

        return np.array([-(der_U + der_V),
                         -(der_Ug + der_Uh),
                         -(der_Vg + der_Vh)]) / self.delta