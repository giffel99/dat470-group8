#!/usr/bin/env python3
from problem1 import SingleStepKMeans
import time

if __name__ == '__main__':
    mr_job = SingleStepKMeans(args=['-r','local','--num-cores','8','data_in.txt'])
    start = time.time()
    with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.cat_output():
            print(line.decode('utf-8'), end='')

        #print(next(runner.cat_output()).decode('utf-8'), end='')
        
    end = time.time()
    print(end-start)