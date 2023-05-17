#!/usr/bin/env python3

import numpy as np
import sys
import math
from random import randrange

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
    #comp_value_bin = bin(2147483648)
    #comp_value_hex = 0x80000000
    for i in range(1,33):
        if(x >= comp_value):
            return i
        comp_value = comp_value >> 1 & 0xffffffff
    return 0

def set_alpha_m(m):
    if m == 16:
        return 0.673
    if m == 32:
        return 0.697
    if m == 64:
        return 0.709
    else:
        return 0.7213 / ( 1 + ( 1.079/m ))

def hyperloglog(random_numbers, A):
    n_approx = 0
    l = 8
    # j = 2**l
    m = 2**l
    alpha_m = set_alpha_m(m)
    M = np.zeros(m)
    for y in random_numbers:
        #y = int(y,16) & 0xffffffffffffffff
        M[f(y,l)] = max(M[f(y,l)],p(h(8,y,A)))

    harmonic_mean_M = 1 / sum([ 2** -bucket  for bucket in M])
    n_approx = alpha_m * m**2 * harmonic_mean_M
    v_0 = len([bucket for bucket in M if bucket == 0])
    if(n_approx <= 5*m/2 and v_0  > 0):
        print("first case")
        n_approx = m * math.log(m/v_0)
    elif(n_approx > (2**32)/30 ):
        print("Second case")
        n_approx = -(2**32 * math.log(1- (n_approx/2**32)))
    return n_approx

def main():
    A = random_32_bits(8)

    random_numbers = [randrange(2**64) for i in range(10000)]
    total_distinct = len(set(random_numbers))
    n_hat = hyperloglog(random_numbers)
    print(total_distinct)
    print(n_hat)


if __name__ == '__main__':
    main()
