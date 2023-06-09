#!/usr/bin/env python3

import multiprocessing
import random
import argparse
from math import pi
import time

def sample_pi(seed, input_queue, output_queue):
    """Perform n steps of the Monte Carlo simulation for estimating Pi/4
    Returns the number of successes."""
    random.seed(seed)
    while True:
        m = input_queue.get()
        if m is None:
            break
        
        s = 0
        for i in range(m):
            x = random.random()
            y = random.random()
            if x**2 + y**2 <= 1.0:
                s += 1
        output_queue.put(s)

def compute_pi(accuracy ,num_workers, seed):

    n = 1000000
    s_total = 0
    total_time = 0
    iterations = 0

    input_queues = [multiprocessing.Queue() for _ in range(num_workers)]
    output_queue = multiprocessing.Queue()

    processes = [multiprocessing.Process(target=sample_pi, args=(seed + i, input_queues[i], output_queue)) for i in range(num_workers)]
    
    for process in processes:
        process.start()

    while True:
        
        m = n // num_workers

        time_start = time.time()

        for input_queue in input_queues:
            input_queue.put(m)

        s = [output_queue.get() for _ in range(num_workers)]
        
        time_elapsed = time.time() - time_start
        total_time += time_elapsed
        iterations += 1
        n_total = m * num_workers * iterations
        s_total += sum(s)
        pi_est = 4.0 * s_total / n_total 
        error = abs(pi - pi_est)

        if error <= accuracy:
            break
    
    for input_queue in input_queues:
        input_queue.put(None)

    for process in processes:
        process.join()

    samples_per_second = n_total / total_time
    print(f'Accuracy: {accuracy:1.5f}, Workers: {num_workers}, Seed: {seed}, Pi Estimate: {pi_est:1.6f}, Error: {error:1.6f}, Samples/s: {samples_per_second:1.5f}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers','-w',default=1,type=int,
                        help='Number of parallel processes'),
    parser.add_argument('--accuracy', '-a', default=0.00001, type=float, 
                        help='Accuracy goal for approximating Pi')
    parser.add_argument('--seed',default=1,type=int,
                        help='The seed')
    
    args = parser.parse_args()
    compute_pi(args.accuracy, args.workers, args.seed)
