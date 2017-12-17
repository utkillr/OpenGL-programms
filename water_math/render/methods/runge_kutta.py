from render.methods.base import Base
import numpy as np


class RungeKutta(Base):

    def __init__(self, method, v=100, delta=1, sigma=0.1, size=(50, 50), max_height=0.4, min_height=0.2, borders=False, is_shallow=False):
        super().__init__(method, v, delta, sigma, size, max_height, min_height, borders, is_shallow)

    # y(x+h) = y(x) + h/6 * (k1+2k2+2k3+k4)
    # x is vector [h(t), v(t)]
    def runge_kutta(self, f, x, h):
        k_1 = self.k1(f, x, h)
        k_2 = self.k2(f, x, h, k_1)
        k_3 = self.k3(f, x, h, k_2)
        k_4 = self.k4(f, x, h, k_3)
        return x + (h / 6) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)

    def k1(self, f, x, h):
        return f(x)

    def k2(self, f, x, h, k_1):
        return f(x + h * k_1 / 2)

    def k3(self, f, x, h, k_2):
        return f(x + h * k_2 / 2)

    def k4(self, f, x, h, k_3):
        return f(x + h * k_3)

    def get_heights(self, h_desc):
        if self.is_shallow:
            return self.get_shallow_heights(h_desc)
        # first time
        if h_desc is None:
            h = self.init()
            h_der = np.zeros(self.size, dtype=np.float32)
            return np.array([h, h_der])
        # other times
        else:
            return self.runge_kutta(self.f, h_desc, self.sigma)

    def get_shallow_heights(self, h_desc):
        # first time
        if h_desc is None:
            h = self.init()
            U = np.zeros(self.size, dtype=np.float32)
            V = np.zeros(self.size, dtype=np.float32)
            return np.array([h, U, V])
        # other times
        else:
            return self.runge_kutta(self.f_shallow, h_desc, self.sigma)
