from render.methods.base import Base
import numpy as np


class Euler(Base):
    def __init__(self, v=200, delta=1, sigma=0.02, size=(50, 50), start_h=1, borders=False):
        super().__init__(v, delta, sigma, size, start_h, borders)

    # y(x+h) = y(x) + h * f(x)
    # x is vector [h(t), v(t)]
    def euler(self, f, x, h):
        return x + h * f(x)

    def get_heights(self, h, h_der):
        # first time
        if h is None:
            h = self.init_drop(4)
            h_der = np.zeros(self.size, dtype=np.float32)
            return np.array([h, h_der])
        # other times
        else:
            return self.euler(self.f, np.array([h, h_der]), self.sigma)
