#!/usr/bin/env python3
import sys
from problem2d import ApproximatedMedian
import time

if __name__ == '__main__':
    min_value = float(sys.argv[1])
    max_value = float(sys.argv[2])
    num_bins = int(sys.argv[3])

    data = sys.argv[4]

    mr_job = ApproximatedMedian(
        args=['-r', 'local', '--num-cores', '4', '--min_value', str(min_value), '--max_value', str(max_value),
              '--num_bins', str(num_bins), data])

    start = time.time()
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.cat_output():
            print(line.decode('utf-8'), end='')
    end = time.time()
    print("Execution Time:", end - start)
