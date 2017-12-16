from render.methods.base import Base
from render.methods.range_kutta import RangeKutta
import numpy as np

class Verlet(Base):

    def __init__(self, method, v=200, delta=1, sigma=0.05, size=(50, 50), max_height=0.4, min_height=0.2, borders=False, is_shallow=False):
        super().__init__(method, v, delta, sigma, size, max_height, min_height, borders, is_shallow)
        self.prev = []

    # y(x+h) = 2y(x) - y(x-h) + f(f(x))h^2
    # x is vector [h(t), v(t)]
    def verlet(self, f, x, prev, h):
        return 2 * x - prev + h * h * f(f(x))

    def get_heights(self, h_desc):
        # first time
        if h_desc is None:
            h = self.init()
            h_der = np.zeros(self.size, dtype=np.float32)
            return np.array([h, h_der])
        # second time
        elif np.array_equal(h_desc[0], self.init()):
            new_h_desc = RangeKutta(self.method, self.v, self.delta, self.sigma, self.size, self.max_height, self.min_height, self.borders, self.is_shallow).get_heights(h_desc)
            self.prev = h_desc
            return new_h_desc
        # other times
        else:
            new_h, new_h_der = self.verlet(self.f, h_desc, self.prev, self.sigma)
            self.prev = h_desc
            return np.array([new_h, new_h_der])