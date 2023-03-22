#!/usr/bin/env python3

import multiprocessing
import random
import argparse
from math import pi

def sample_pi(n):
    """Perform n steps of the Monte Carlo simulation for estimating Pi/4
    Returns the number of successes."""
    random.seed()
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s

def compute_pi(n,num_workers):
    m = n//num_workers
    with multiprocessing.Pool(num_workers) as p:
        s = p.map(sample_pi, [m]*num_workers)
    n_total = m*num_workers
    s_total = sum(s)
    pi_est = 4.0 * s_total / n_total
    print('Steps\t# Succ.\tPi est.\tError')
    print(f'{n_total:6d}\t{s_total:6d}\t{pi_est:1.5f}\t{pi-pi_est:1.5f}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers','-w',default=1,type=int,
                        help='Number of parallel processes')
    parser.add_argument('--steps','-s',default=1000,type=int,
                        help='Number of steps in the Monte Carlo simulation')
    args = parser.parse_args()
    compute_pi(args.steps, args.workers)
