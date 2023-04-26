import matplotlib.pyplot as plt

if __name__ == '__main__':
    k = ["1","2","4","8","16","32"]
    total_times = [314.75547766685486,305.4027359485626,167.0578248500824,93.26351284980774, 69.52318000793457, 69.41683793067932]    
     # Calculate the measured speedup
    measured_speedup = [s / total_times[0] for s in total_times]

    plt.plot(k, measured_speedup, marker="o", label="Measured speedup")
    plt.title("Speedup using more cores in problem 2a")
    plt.xlabel("# of cores")
    plt.ylabel('Speedup')
    plt.legend()
    plt.show()