import matplotlib.pyplot as plt

if __name__ == '__main__':
    k = ["1","2","4","8","16","32"]
    #measured_times = [88.35131430625916,52.10178589820862,32.72658681869507,22.43439745903015,20.462034225463867,15.717040538787842] #10M data file
    measured_times = [1400.1933352947235,603.6104681491852,418.5761251449585,364.52511644363403,226.1906807422638,212.77759456634521] #100M data file
    speedup = [1,2,4,8,16,32]
    
    # Calculate the measured speedup
    measured_speedup = [measured_times[0]/s for s in measured_times]
    
    plt.plot(k, measured_speedup, marker="o", label="Measured speedup")
    plt.title("Speedup of SummaryStatistics Program")
    plt.xlabel("# of cores")
    plt.ylabel('Speedup')
    plt.legend()
    plt.show()