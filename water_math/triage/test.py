from triage.runge_kutta import runge_kutta
from triage.verlet import verlet
from triage.equation import y, f

import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    runge_errors_array = []
    verlet_errors_array = []
    h_array = []

    for h in np.linspace(-5, 5, 1000):
        print(str(h))
        errors_verlet = []
        errors_runge = []
        prev_prev_y_verlet = y(-h)
        prev_y_verlet = y(0)
        prev_y_runge = y(0)
        xlist = [(0 + h * i) for i in range(0, 100)]
        for x in xlist:
            real_y = y(x + h)

            new_y_runge = runge_kutta(f, prev_y_runge, x, h)
            prev_y_runge = new_y_runge
            errors_runge.append(np.abs(real_y - new_y_runge))

            new_y_verlet = verlet(f, prev_y_verlet, prev_prev_y_verlet, x, h)
            prev_prev_y_verlet = prev_y_verlet
            prev_y_verlet = new_y_verlet
            errors_verlet.append(np.abs(real_y - new_y_verlet))

        error_runge = np.log10(sum(errors_runge) / len(errors_runge))
        error_verlet = np.log10(sum(errors_verlet) / len(errors_verlet))

        runge_errors_array.append(error_runge)
        verlet_errors_array.append(error_verlet)
        h_array.append(h)

    runge_errors_array = runge_errors_array / np.max(runge_errors_array)
    verlet_errors_array = verlet_errors_array / np.max(verlet_errors_array)

    plt.plot(h_array, runge_errors_array, color="g")
    plt.plot(h_array, verlet_errors_array, color="r")
    plt.show()