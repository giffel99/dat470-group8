#!/usr/bin/env python3

import numpy as np
import sys

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

def main():
    A = random_32_bits(8)
    l = 2
    j = 2**l
    M = np.zeros(j)
    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        for y in line.strip().split():
            y = int(y,16) & 0xffffffffffffffff
            M[f(y,l)] = max(M[f(y,l)],p(h(8,y,A)))








if __name__ == '__main__':
    main()