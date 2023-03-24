#!/usr/bin/env python3

import multiprocessing
import random
import argparse
from math import pi
import time

def sample_pi(n,seed):
    """Perform n steps of the Monte Carlo simulation for estimating Pi/4
    Returns the number of successes."""
    random.seed(seed)
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s

def compute_pi(n,num_workers, seed):
    # Executed serially
    serial_time = time.time()
    m = n//num_workers
    time_parallell_start = time.time()
    # Parallell part of the script.
    with multiprocessing.Pool(num_workers) as p:
        s = p.starmap(sample_pi,[(m,seed)]*num_workers )
    # Parallell part is complete
    clocked_time_parallell = (time.time() - time_parallell_start)
    n_total = m*num_workers
    s_total = sum(s)
    pi_est = 4.0 * s_total / n_total

    serial_time = (time.time() - serial_time - clocked_time_parallell)
    print('Seed\tClocked_time_start\tclocked_time_parallell\tNum_workers\tSteps\t# Succ.\tPi est.\tError')
    print(f'{seed}\t{serial_time}\t{clocked_time_parallell}\t{num_workers}\t{n_total:6d}\t{s_total:6d}\t{pi_est:1.5f}\t{pi-pi_est:1.5f}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers','-w',default=1,type=int,
                        help='Number of parallel processes')
    parser.add_argument('--steps','-s',default=1000,type=int,
                        help='Number of steps in the Monte Carlo simulation')
    parser.add_argument('--seed',default=1,type=int,
                        help='The seed')
    
    args = parser.parse_args()
    compute_pi(args.steps, args.workers, args.seed)
