from render.methods.base import Base
from render.methods.range_kutta import RangeKutta
import numpy as np

class Verlet(Base):

    def __init__(self, v=200, delta=1, sigma=0.05, size=(50, 50), start_h=1, borders=False):
        super().__init__(v, delta, sigma, size, start_h, borders)
        self.prev = []

    # y(x+h) = 2y(x) - y(x-h) + f(f(x))h^2
    # x is vector [h(t), v(t)]
    def verlet(self, f, x, prev, h):
        return 2 * x - prev + h * h * f(f(x))

    def get_heights(self, h, h_der):
        # first time
        if h is None:
            h = self.init_drop(4)
            h_der = np.zeros(self.size, dtype=np.float32)
            return np.array([h, h_der])
        # second time
        elif np.array_equal(h, self.init_drop(4)):
            new_h, new_h_der = RangeKutta(self.v, self.delta, self.sigma, self.size, self.start_h, self.borders).get_heights(h, h_der)
            self.prev = np.array([h, h_der])
            return np.array([new_h, new_h_der])
        # other times
        else:
            new_h, new_h_der = self.verlet(self.f, np.array([h, h_der]), self.prev, self.sigma)
            self.prev = np.array([h, h_der])
            return np.array([new_h, new_h_der])