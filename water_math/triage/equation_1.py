import math


start = 0

def f(x, _y):
    return y(x) * math.cos(x)

def ff(x, _y):
    return y(x) * (math.cos(x) ** 2 - math.sin(x))

def y(x):
    return math.pow(math.e, math.sin(x))