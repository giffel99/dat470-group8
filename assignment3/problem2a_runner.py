#!/usr/bin/env python3
from problem2a import SummaryStatistics
import time

if __name__ == '__main__':
    mr_job = SummaryStatistics(args=['-r','local','--num-cores','2','/data/2023-DAT470-DIT065/data-assignment-3-1M.dat'])
    start = time.time()
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.cat_output():
            print(line.decode('utf-8'), end='')

        #print(next(runner.cat_output()).decode('utf-8'), end='')
        
    end = time.time()
    print(end-start)

