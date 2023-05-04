#!/usr/bin/env python3
import numpy as np
import random
def random_32_bits(input_size):
    np.random.seed(0)
    bins = int(64/input_size)
    A = np.zeros((bins, int(2**(input_size))), dtype=np.uint32)
    for i in range(len(A)):
        for j in range(len(A[i])):
            A[i][j] = np.random.randint(low=((2**32)), dtype=np.uint32)
    return A

def tabulate_hash(input_size, input, A):
    # input_data_size = 64 bitar
    # A_data_size = 32 * 64/input_size * 2^input_size bitar
    # res = 32 bitar 
    res = np.uint32(0)
    bins = int(64/ input_size)
    for i in range(bins):
        shift = input >> np.uint32(input_size*i) 
        shift = shift & np.uint32((2**input_size)-1)
        res ^= A[i][shift]
    return res


if __name__ == '__main__':

    A8 = random_32_bits(8)
    A16 = random_32_bits(16)

    input_8 = np.uint64(200)
    input_16 = np.uint64(200)
    
    res_8 = tabulate_hash(8, input_8, A8)
    res_16 = tabulate_hash(16, input_16, A16)

    print(input_8, res_8)
    print(input_16, res_16)