
import numpy as np


class Sun(object):
    def __init__(self,
                 base_direction=np.array([1, 0, 1], dtype=np.float32),
                 color=np.array([0.8, 0.8, 0], dtype=np.float32)):
        self.base_direction = base_direction
        self.color = color

    def direction(self, time):
        angle = np.pi * (1 + time * 0.1)
        direction = np.array([np.sin(angle), np.cos(angle), -0.5], dtype=np.float32)
        return direction / np.linalg.norm(direction)
