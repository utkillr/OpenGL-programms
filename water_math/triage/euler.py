from triage.equation_1 import *


# y(x+h) = y(x) + h * f(x)
def euler(f, y, x, h):
    return y + h * f(x, y)


if __name__ == "__main__":
    h = 0.0001
    xlist = [(0 + h * i) for i in range(0, 100)]


    prev_y = 1
    for x in xlist:
        real_y = y(x + h)
        new_y = euler(f, prev_y, x, h)
        prev_prev_y = prev_y
        prev_y = new_y
        print("Error: " + str((math.fabs(real_y - new_y)) / math.fabs(real_y)))
