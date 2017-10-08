
import numpy as np


class Sun(object):
    def __init__(self,
                 base_direction=np.array([1, 0, 1], dtype=np.float32),
                 color=np.array([0.7, 0.7, 0],dtype=np.float32)):
        self.base_direction = base_direction
        self.color = color

    def direction(self):
        return self.base_direction / np.linalg.norm(self.base_direction)