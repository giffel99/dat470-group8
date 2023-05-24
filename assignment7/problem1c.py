import findspark
findspark.init()
from pyspark import SparkContext
import numpy as np
import math
from random import randrange
import time

def random_32_bits(input_size):
    np.random.seed(1)
    bins = int(64/input_size)
    A = np.zeros((bins, int(2**(input_size))), dtype=np.uint32)
    for i in range(len(A)):
        for j in range(len(A[i])):
            A[i][j] = np.random.randint(low=((2**32)), dtype=np.uint32)
    return A

def h(input_size, input, A):
    res = np.uint32(0)
    bins = int(64/ input_size)
    for i in range(bins):
        shift = input >> np.uint32(input_size*i) 
        shift = shift & np.uint32((2**input_size)-1)
        res ^= A[i][shift]
    return res

def f(x,l):
    return (((x*0xbc164501) & 0xffffffff) >> (32-l)) & 0xffffffff

def p(x):
    comp_value = 2147483648
   
    for i in range(1,33):
        if(x >= comp_value):
            return i & 0xff
        comp_value = comp_value >> 1 & 0xffffffff
    return 0 & 0xff

def set_alpha_m(m):
    if m == 16:
        return 0.673
    if m == 32:
        return 0.697
    if m == 64:
        return 0.709
    else:
        return 0.7213 / ( 1 + ( 1.079/m ))

def hyperloglog_on_partition(partition, broadcast_A):
    n_approx = 0
    l = 8
    m = 2**l
    alpha_m = set_alpha_m(m)
    M = np.zeros(m, dtype=np.uint8)
    for y in partition:
        M[f(y,l)] = max(M[f(y,l)],p(h(8,y,broadcast_A.value)))

    harmonic_mean_M = 1 / sum([ 2** -bucket.astype(float)  for bucket in M])
    n_approx = alpha_m * m**2 * harmonic_mean_M
    v_0 = len([bucket for bucket in M if bucket == 0])

    if(n_approx <= 5*m/2 and v_0  > 0):
        n_approx = m * math.log(m/v_0)
    elif(n_approx > (2**32)/30 ):
        n_approx = -(2**32 * math.log(1- (n_approx/2**32)))
    yield n_approx

def main():
    sc = SparkContext(master = 'local[32]')

    A = random_32_bits(8)

    # Creating a broadcast variable to distribute 'A' across the Spark cluster
    A_broadcasted = sc.broadcast(A)

    random_numbers = [randrange(2**64) for i in range(1000000)]

    # Constructing an RDD of the random numbers
    rdd = sc.parallelize(random_numbers)

    # Counting the true number of distinct elements for comparision
    total_distinct = rdd.distinct().count()

    # Performing hyperloglog algorithm to every partition of the RDD and then combining the results 
    n_hat = rdd.mapPartitions(lambda partition: hyperloglog_on_partition(partition, A_broadcasted)).reduce(lambda a,b: a+b)
    print(total_distinct)
    print(n_hat)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    total_time = end - start

    print(f'Total execution time is: {total_time}')

# Execution times for 100000 random numbers
# Total execution time is: 13.93044662475586 (1 core)
# Total execution time is: 10.718540668487549 (2 cpres)
# Total execution time is: 8.37300419807434 (4 cores)
# Total execution time is: 7.9815497398376465 (8 cores)
# Total execution time is: 7.747605323791504 (16 cores)
# Total execution time is: 8.63371753692627 (32 cores)

# Execution times for 1000000 random numbers
# Total execution time is: 82.16899871826172 (1 core)
# Total execution time is: 38.74206256866455 (2 cpres)
# Total execution time is: 23.30802869796753 (4 cores)
# Total execution time is: 16.739031314849854 (8 cores)
# Total execution time is: 13.05227255821228 (16 cores)
# Total execution time is: 12.738852977752686 (32 cores)