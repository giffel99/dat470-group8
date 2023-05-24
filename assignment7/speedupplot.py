import matplotlib.pyplot as plt

if __name__ == '__main__':
    k = ["1","2","4","8","16","32"]
    total_times = [119.96161079406738,96.68435764312744,54.37198877334595,33.25247287750244, 27.793466329574585, 19.779373168945312]    
     # Calculate the measured speedup
    measured_speedup = [total_times[0] / s for s in total_times]

    plt.plot(k, measured_speedup, marker="o", label="Measured speedup")
    plt.title("Speedup using more cores in Assignment 7")
    plt.xlabel("# of cores")
    plt.ylabel('Speedup')
    plt.legend()
    plt.show()