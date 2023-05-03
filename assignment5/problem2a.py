#!/usr/bin/env python3

import sys
import numpy as np
from collections import defaultdict

count = defaultdict(int)

def get_memory_usage():

    # Size of a pointer "key" which is 64 bits (= 8 bytes) and the 32-bit integer "count" storing the count of such keys (= 4 bytes).
    key_size = 8
    count_size = 4

    # Calculate the number of cells in the hash table (least power of 2 greater than or equal to n)
    n = len(count)
    num_table_cells = 2 ** np.ceil(np.log2(n))
    
    # Calculate the memory used by the hash table elements
    table_memory = num_table_cells * (key_size + count_size)

    # Calculate the memory used by the strings (key-value pairs)
    string_memory = sum(2 * (len(key) + 1) for key in count.keys())

    # Return the total memory usage
    return table_memory + string_memory

if __name__ == '__main__':
    for line in sys.stdin:
        if 'q' == line.rstrip():
            break
        for word in line.strip().split():
            count[word] += 1

    for k,v in count.items():
        print(k, v)

    print("Approximate memory usage:", get_memory_usage(), "bytes")
