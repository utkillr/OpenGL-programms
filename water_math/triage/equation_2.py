import math


def f(x, y):
    return 2 * math.cos(2 * x) / (math.sin(2 * x) + 4)

def ff(x, y):
    return 4 * (4 * math.sin(2 * x) + 1) / ((math.sin(2 * x) + 4) ** 2)

def y(x):
    return math.log(2 + math.cos(x) * math.sin(x))