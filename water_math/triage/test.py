from triage.runge_kutta import runge_kutta
from triage.verlet import verlet
from triage.euler import euler
from triage.equation_1 import y, f

import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    avg_errors = {
        "euler": [],
        "verlet": [],
        "runge": []
    }

    hs = []

    for h in np.linspace(-5, 5, 1000):
        print(str(h))
        errors = {
            "euler": [],
            "verlet": [],
            "runge": []
        }
        prev_prev_y = y(-h)
        prev_y = {
            "euler": y(0),
            "verlet": y(0),
            "runge": y(0)
        }
        xlist = [(0 + h * i) for i in range(0, 100)]
        for x in xlist:
            real_y = y(x + h)

            new_y = {
                "euler": euler(f, prev_y["euler"], x, h),
                "verlet": verlet(f, prev_y["verlet"], prev_prev_y, x, h),
                "runge": runge_kutta(f, prev_y["runge"], x, h)
            }

            prev_y = {
                "euler": new_y["euler"],
                "verlet": new_y["verlet"],
                "runge": new_y["runge"]
            }
            prev_prev_y = prev_y["verlet"]

            errors["euler"].append(np.abs(real_y - new_y["euler"]))
            errors["verlet"].append(np.abs(real_y - new_y["verlet"]))
            errors["runge"].append(np.abs(real_y - new_y["runge"]))

        avg_errors["euler"].append(np.abs(np.log(sum(errors["euler"]) / len(errors["euler"]))))
        avg_errors["verlet"].append(np.abs(np.log(sum(errors["verlet"]) / len(errors["verlet"]))))
        avg_errors["runge"].append(np.abs(np.log(sum(errors["runge"]) / len(errors["runge"]))))
        hs.append(h)

    avg_errors["euler"] = avg_errors["euler"] / np.max(avg_errors["euler"])
    avg_errors["verlet"] = avg_errors["verlet"] / np.max(avg_errors["verlet"])
    avg_errors["runge"] = avg_errors["runge"] / np.max(avg_errors["runge"])

    plt.plot(hs, avg_errors["euler"], color="r")
    plt.plot(hs, avg_errors["verlet"], color="y")
    plt.plot(hs, avg_errors["runge"], color="g")
    plt.show()