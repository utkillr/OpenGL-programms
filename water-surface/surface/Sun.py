
import numpy as np


class Sun(object):
    def __init__(self, base_direction=np.array([1, 0, 1], dtype=np.float32)):
        self.base_direction = base_direction

    def direction(self, time):
        angle = np.pi * (1 + time * 0.1)
        direction = np.array([np.sin(angle), np.cos(angle), -0.5], dtype=np.float32)
        return direction / np.linalg.norm(direction)

    def normalized_direction(self):
        return self.base_direction / np.sqrt(np.sum(self.base_direction * self.base_direction, axis=-1))[..., None]

    def diffused_color(self):
        return [1, 0.8, 1]

    def reflected_color(self):
        return [1, 0.8, 0.6]
