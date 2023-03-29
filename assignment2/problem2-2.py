#!/usr/bin/env python3

import multiprocessing
import random
import argparse
from math import pi
import time

def sample_pi(n,seed, queue):
    """Perform n steps of the Monte Carlo simulation for estimating Pi/4
    Returns the number of successes."""
    random.seed(seed)
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    queue.put(s)

def compute_pi(accuracy ,num_workers, seed):

    n = 1000
    s_total = 0
    total_time = 0
    iterations = 0

    while True:
        queue = multiprocessing.Queue()
        m = n // num_workers

        time_start = time.time()

        processes = [multiprocessing.Process(target=sample_pi, args=(m, seed + i + iterations * num_workers, queue)) for i in range(num_workers)]
        for process in processes:
            process.start()

        s = [queue.get() for _ in range(num_workers)]

        for process in processes:
            process.join()

        time_elapsed = time.time() - time_start
        total_time += time_elapsed
        iterations += 1
        n_total = m * num_workers * iterations
        s_total += sum(s)
        pi_est = 4.0 * s_total / n_total 
        error = abs(pi - pi_est)

        if error <= accuracy:
            break

    samples_per_second = n_total / total_time
    print(f'Accuracy: {accuracy}, Workers: {num_workers}, Seed: {seed}, Pi Estimate: {pi_est:1.5f}, Error: {error:1.5f}, Samples/s: {samples_per_second:1.5f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers','-w',default=1,type=int,
                        help='Number of parallel processes'),
    parser.add_argument('--accuracy', '-a', default=0.001, type=float, 
                        help='Accuracy goal for approximating Pi')
    parser.add_argument('--seed',default=1,type=int,
                        help='The seed')
    
    args = parser.parse_args()
    compute_pi(args.accuracy, args.workers, args.seed)
