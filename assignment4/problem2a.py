import findspark
findspark.init()
from pyspark import SparkContext

import argparse
import math 
import time
def reduce(a,b):
   
    sum = a[0] + b[0]
    sum_sq = a[1] + b[1]
    count = a[2] + b[2]
    min_value = min(a[3],b[3])
    max_value = max(a[4],b[4])

    return (sum, sum_sq, count, min_value, max_value)

def toObject(t):
    t = float(t)
    return (t, t ** 2, 1, t, t)
def toObjectWithKey(t):
    val = float(t[1])
    return (t[0],(val, val ** 2, 1, val, val))

def main(data):
    s_time = time.time()
    
    sc = SparkContext(master = 'local[16]')
    distFile = sc.textFile(data)

    keyTuples = distFile.map(lambda l: l.split("\t")) \
    .map(lambda t: (t[1],t[2])) \
    .map(lambda t: toObjectWithKey(t))
    
    summedValuesByKey = keyTuples.reduceByKey(lambda a,b:reduce(a,b))
    summedValues = summedValuesByKey.map(lambda a:a[1]).reduce(lambda a,b: reduce(a,b))

    mean = summedValues[0] / summedValues[2]
    stdv = math.sqrt((summedValues[1] / summedValues[2]) - mean ** 2) 
    e_time = time.time() - s_time
    print("total time:", e_time)
    print(f"Mean: {mean}, standard deviation: {stdv}, min value: {summedValues[3]}, max value: {summedValues[4]} ")
     
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='problem 2a',
        epilog = 'Example: problem2a.py '
    )
    parser.add_argument('--data', '-d',
                        default='/data/2023-DAT470-DIT065/data-assignment-3-10M.dat',
                        type = str,
                        help='Number of parallel processes to use (NOT IMPLEMENTED)')
    parser.add_argument('--workers', '-w',
                        default=1,
                        type = int,
                        help='Number of parallel processes to use (NOT IMPLEMENTED)')
    args = parser.parse_args()
    main(args.data)
    
