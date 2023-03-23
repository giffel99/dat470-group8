import matplotlib.pyplot as plt

if __name__ == '__main__':
    k = ["1","2","4","8","16","32"]
    measured_times = [4.162677526473999,3.3543643951416016,1.6475944519042969,1.075671672821045,0.6489095687866211,0.3207828998565674]
    proportion = 0.99999885449  # The proportion of execution time that the part benefiting from improved resources originally occupied
    speedup = [1,2,4,8,16,32]
    theoretical_times = [measured_times[0] / (1 / ((1 - proportion) + (proportion/s))) for s in speedup] #Ahmdahl's law applied
    
    plt.plot(k,measured_times, marker="o", label="Measured time")
    plt.plot(k,theoretical_times, marker="o", label="Theoretical time")
    plt.title("Monte Carlo performance in SLURM (10M steps)")
    plt.xlabel("# of cores")
    plt.ylabel('seconds')
    plt.legend()
    plt.show()
