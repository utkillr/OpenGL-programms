import numpy as np


class HeightsGenerator:
    def __init__(self, size):
        self.size = size

    def peak(self, params):
        min_height = params["min_height"]
        max_height = params["max_height"]
        assert min_height < max_height
        h = np.ones(self.size, dtype=np.float32) * min_height
        h[self.size[0] // 2, self.size[1] // 2] = max_height
        h[self.size[0] // 2 + 1, self.size[1] // 2] = max_height
        h[self.size[0] // 2, self.size[1] // 2 + 1] = max_height
        h[self.size[0] // 2 + 1, self.size[1] // 2 + 1] = max_height
        return h

    def bubble(self, params):
        min_height = params["min_height"]
        max_height = params["max_height"]
        part = params["part"]
        assert min_height < max_height
        h = np.ones(self.size, dtype=np.float32) * min_height
        i_center = self.size[0] // 2
        j_center = self.size[1] // 2
        for i in range(self.size[0] // part, self.size[0] * (part - 1) // part):
            for j in range(self.size[1] // part, self.size[1] * (part - 1) // part):
                r = np.sqrt((i - i_center) ** 2 + (j - j_center) ** 2)
                R = self.size[0] // part
                h[i][j] = min_height * (np.cos(np.pi * r / R) + 1) + (max_height - min_height)
        return h

    def vertical(self, params):
        min_height = params["min_height"]
        max_height = params["max_height"]
        assert min_height < max_height
        h = np.ones(self.size, dtype=np.float32) * min_height
        i_center = self.size[0] // 2
        j_center = self.size[1] // 2
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):
                r = np.sqrt((i - i_center) ** 2 + (j - j_center) ** 2)
                R = self.size[0] // 2
                h[i][j] = min_height * (np.cos(np.pi * r / R) + 1) + (max_height - min_height)
        return h