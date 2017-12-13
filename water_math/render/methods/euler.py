from render.methods.base import Base
import numpy as np


class Euler(Base):
    def __init__(self, v=10, delta=0.05, sigma=0.01, size=(50, 50), start_h=1, borders=False):
        super().__init__(v, delta, sigma, size, start_h, borders)

    # y(x+h) = y(x) + h * f(x)
    # x is vector [h(t), v(t)]
    def euler(self, f, x, h):
        return x + h * f(x)

    def get_heights(self, h, h_der):
        # first time
        if h is None:
            h = self.init_h()
            h_der = np.zeros(self.size, dtype=np.float32)
            return np.array([h, h_der])
        # other times
        else:
            return self.euler(self.f, np.array([h, h_der]), self.sigma)
