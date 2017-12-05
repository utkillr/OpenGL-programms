import math
from equation import *

# y(x+h) = y(x) + h/6 * (k1+2k2+2k3+k4)
def runge_kutta(f, y, x, h):
    return y + (h / 6) * (k1(f, y, x, h) + 2 * k2(f, y, x, h) + k3(f, y, x, h) + k4(f, y, x ,h))


def k1(f, y, x, h):
    return f(x, y)


def k2(f, y, x, h):
    return f(x + h / 2, y + h * k1(f, y, x, h) / 2)


def k3(f, y, x, h):
    return f(x + h / 2, y + h * k2(f, y, x, h) / 2)


def k4(f, y, x, h):
    return f(x + h, y + h * k2(f, y, x, h))


if __name__ == "__main__":
    h = 0.0001
    xlist = [(0 + h * i) for i in range(0, 100)]

    prev_y = 1
    for x in xlist:
        real_y = y(x + h)
        new_y = runge_kutta(f, prev_y, x, h)
        prev_y = new_y
        print("Error: " + str((math.fabs(real_y - new_y)) / math.fabs(real_y)))
