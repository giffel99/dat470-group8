import sys
from problem2c import Histogram
import time

if __name__ == '__main__':
    min_value = float(sys.argv[1])
    max_value = float(sys.argv[2])
    data = sys.argv[3]

    mr_job = Histogram(
        args=['-r', 'local', '--num-cores', '4', '--min_value', str(min_value), '--max_value', str(max_value), data])
    start = time.time()
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.cat_output():
            print(line.decode('utf-8'), end='')
    end = time.time()
    print(end - start)
