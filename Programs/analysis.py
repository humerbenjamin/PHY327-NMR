import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats
from scipy.optimize import curve_fit


def fun_T1(t, T1, c, Mo):
    return np.exp((-1)*(t+c)/T1) + Mo

def fun_T2(t, T2, c, d):
    return np.exp((-1)*(2*(t+c))/T2) + d

def get_chisquare(datax, datay, coeffs, fun):
    expected = fun(datax, coeffs[0], coeffs[1], coeffs[2])
    chi_square_test_statistic, p_value = stats.chisquare(datay, expected)
    return chi_square_test_statistic, p_value

def get_data(filename, coeff, type):
    data = pd.read_csv(filename)
    data.columns
    if coeff == "T1":
        if type == "both":
            x1 = np.array(data["t sec l"])
            y1 = np.array(data["Mz(t) Volts l"])
            plt.plot(x1, y1, "o")
            params, cov = curve_fit(fun_T1, x1, y1, [0.01, 0, 0.01])
            print(params)
            x2 = np.linspace(x1[0]-(x1[0]/2), x1[-1]+(x1[0]/2), 10000)
            y2 = fun_T1(x2, params[0], params[1], params[2])
            plt.plot(x2, y2, "r")
            x1 = np.array(data["t sec h"])
            y1 = np.array(data["Mz(t) Volts h"])
            plt.plot(x1, y1, "o")
            params2, cov = curve_fit(fun_T1, x1[:50], y1[:50], [0.01, 0, 0.01])
            print(params2)
            x2 = np.linspace(x1[0]-(x1[0]/2), x1[49]+(x1[0]/2), 10000)
            y2 = fun_T1(x2, params2[0], params2[1], params2[2])
            plt.plot(x2, y2, "k")
            plt.legend(["Light Mineral Oil", "Light Mineral Oil Fit", "Heavy Mineral Oil", "Heavy Mineral Oil Fit"])
            plt.xlabel("Time (seconds)")
            plt.ylabel("Signal Strength (Volts)")
            plt.title("Spin-Lattice Relaxation Time for Heavy and Light Mineral Oil")
            plt.show()
            return
        else:
            x1 = np.array(data["t sec"])
            y1 = np.array(data["Mz(t) Volts"])
            plt.plot(x1, y1, "o")
            params, cov = curve_fit(fun_T1, x1, y1, [0.01, 0, 0.01])
            print(params)
            x2 = np.linspace(x1[0]-(x1[0]/2), x1[-1]+(x1[0]/2), 10000)
            y2 = fun_T1(x2, params[0], params[1], params[2])
            print(get_chisquare(x1, y1, params, fun_T1))
            plt.plot(x2, y2, "k")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Signal Strength (Volts)")
            if type == "heavy":
                plt.title("Spin-Lattice Relaxation Time for Heavy Mineral Oil")
            if type == "light":
                plt.title("Spin-Lattice Relaxation Time for Light Mineral Oil")
            plt.show()
    if coeff == "T2":
        x1 = np.array(data["Pulse Number"])
        y1 = np.array(data["Max Volts"])
        t1 = x1 * 0.0025
        plt.plot(t1, y1, "o",)
        params, cov = curve_fit(fun_T2, t1, y1, [0.02, 0, 0.1])
        print(params)
        x2 = np.linspace(t1[0]-(t1[0]/2), t1[-1]+(t1[0]/2), 10000)
        y2 = fun_T2(x2, params[0], params[1], params[2])
        print(get_chisquare(x1, y1, params, fun_T2))
        plt.plot(x2, y2, "k")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Signal Strength (Volts)")
        if type == "heavy":
            plt.title("Spin-Spin Relaxation Time for Heavy Mineral Oil")
        if type == "light":
            plt.title("Spin-Spin Relaxation Time for Light Mineral Oil")
        plt.show()
    return

if __name__ == "__main__":
    # get_data("Data\T1_heavy-min-oil.csv", "T1", "heavy")
    # get_data("Data\T1_light-min-oil.csv", "T1", "light")
    get_data("Data\T2_heavy-min-oil.csv", "T2", "heavy")
    get_data("Data\T2_light-min-oil.csv", "T2", "light")
    # get_data("Data\T1_both-min-oil.csv", "T1", "both")