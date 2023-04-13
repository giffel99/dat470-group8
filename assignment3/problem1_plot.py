import matplotlib.pyplot as plt

if __name__ == '__main__':
    k = ["1","2","4","8","16","32"]
    measured_times = [230.33,145.85,76.09,39.54,28.89,18.42]
    proportion = 0.9989  # The proportion of execution time that the part benefiting from improved resources originally occupied
    speedup = [1,2,4,8,16,32]
    theoretical_times = [measured_times[0] / (1 / ((1 - proportion) + (proportion/s))) for s in speedup] #Ahmdahl's law applied
    
    plt.plot(k,measured_times, marker="o", label="Measured time")
    plt.plot(k,theoretical_times, marker="o", label="Theoretical time")
    plt.title("Monte Carlo performance in SLURM (10M steps)")
    plt.xlabel("# of cores")
    plt.ylabel('seconds')
    plt.legend()
    plt.show()
