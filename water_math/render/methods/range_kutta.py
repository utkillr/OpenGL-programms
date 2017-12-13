from render.methods.base import Base
import numpy as np


class RangeKutta(Base):

    def __init__(self, v=10, delta=0.1, sigma=0.1, size=(50, 50), start_h=2, borders=False):
        super().__init__(v, delta, sigma, size, start_h, borders)

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

    def get_heights(self, h, h_der):
        # first time
        if h is None:
            h = self.init_h()
            h_der = np.zeros(self.size, dtype=np.float32)
            return np.array([h, h_der])
        # other times
        else:
            return self.runge_kutta(self.f, np.array([h, h_der]), self.sigma)