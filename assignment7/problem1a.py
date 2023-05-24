#!/usr/bin/env python3

import numpy as np
import sys
import math
from random import randrange

def random_32_bits(input_size):
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

def hyperloglog(random_numbers, l):
    
    A = random_32_bits(8)
    n_approx = 0
    # j = 2**l
    m = 2**l
    alpha_m = set_alpha_m(m)
    M = np.zeros(m,dtype=np.uint8)
    for y in random_numbers:
        M[f(y,l)] = max(M[f(y,l)],p(h(8,y,A)))

    harmonic_mean_M = 1 / sum([ 2** -bucket.astype(float)  for bucket in M])
    n_approx = alpha_m * m**2 * harmonic_mean_M
    v_0 = len([bucket for bucket in M if bucket == 0])
    if(n_approx <= 5*m/2 and v_0  > 0):
        n_approx = m * math.log(m/v_0)
    elif(n_approx > (2**32)/30 ):
        n_approx = -(2**32 * math.log(1- (n_approx/2**32)))
    return n_approx

def main():
    n = 100000
    l_list = [6,7,8] # m = 64,128,256
    m_average = []
    m_was_in_range = []
    m_was_in_second_range = []
    n_total_distinct = []

    
    for l in l_list:
        was_in_range = []
        std_error = 1.04 / math.sqrt(2**l) 
        n_hats = []
        was_in_range = 0
        was_in_second_range = 0
        random_numbers = [randrange(10000) for i in range(n)]
        total_distinct = len(set(random_numbers))

        for i in range(10):
            n_hat = hyperloglog(random_numbers,l)
            n_hats.append(n_hat)

            if(n_hat < total_distinct*(1+std_error) and n_hat > total_distinct*(1-std_error)):
                was_in_range +=1
            if(n_hat < total_distinct*(1+std_error*2) and n_hat > total_distinct*(1-std_error*2)):
                was_in_second_range +=1
        n_total_distinct.append(total_distinct)
        m_average.append(sum(n_hats)/10)
        m_was_in_range.append(was_in_range/10)
        m_was_in_second_range.append(was_in_second_range/10)
    print(n_total_distinct)
    print(m_average)
    print(m_was_in_range)
    print(m_was_in_second_range)



if __name__ == '__main__':
    main()
    '''
        [64, 128, 256]
        [10000, 9999, 9999]
        [10202.1125719229, 10269.25190234633, 10183.450291764446]
        [0.9, 0.5, 0.8]
        [1.0, 0.8, 1.0]
    '''
