import math
from equation import *

# y(x+h) = 2y(x) - y(x-h) + f(x, y)h^2
def verlet(f, y, y_prev, x, h):
    return 2 * y - y_prev + f(x, y) * h * h


if __name__ == "__main__":
    h = 0.0001
    xlist = [(0 + h * i) for i in range(0, 100)]

    prev_prev_y = y(-h)
    prev_y = 1
    for x in xlist:
        real_y = y(x + h)
        new_y = verlet(f, prev_y, prev_prev_y, x, h)
        prev_prev_y = prev_y
        prev_y = new_y
        print("Error: " + str((math.fabs(real_y - new_y)) / math.fabs(real_y)))
