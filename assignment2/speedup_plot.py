import matplotlib.pyplot as plt

if __name__ == '__main__':
    k = ["1","2","4","8","16","32"]
    #measured_samples_per_second = [2462590.88292,3013478.24272,4921279.72281,8488604.93700,12229349.17888,12294340.31324]
    measured_samples_per_second = [2552645.05546,3257913.81806,6474116.31302,12269114.59902,13885550.17587,31880237.77120]
    proportion = 0.9985218 # The proportion of execution time that the part benefiting from improved resources originally occupied
    speedup = [1,2,4,8,16,32]
    
     # Calculate the measured speedup
    measured_speedup = [s / measured_samples_per_second[0] for s in measured_samples_per_second]

    # Calculate the theoretical speedup using Amdahl's law
    theoretical_speedup = [((1 - proportion) + (proportion * s)) for s in speedup]
    #theoretical_samples_per_second = [measured_speedup[0] * s for s in theoretical_speedup]
    
    plt.plot(k, measured_speedup, marker="o", label="Measured speedup using samples/s")
    #plt.plot(k, theoretical_speedup, marker="o", label="Theoretical speedup using samples/s")
    plt.title("Monte Carlo simulation for computing Pi \n with accuracy goal 0.00001")
    plt.xlabel("# of cores")
    plt.ylabel('Speedup')
    plt.legend()
    plt.show()