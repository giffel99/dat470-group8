from mrjob.job import MRJob
import math
import time

class MedianOfGroup(MRJob):

    def mapper(self, _, line):
        id_, group, value = line.strip().split('\t')
        value = float(value)
        
        yield group, value
    
    def reducer(self, group, values):
        sorted_values = sorted(values)
        n = len(sorted_values)
        median = 0

        if n % 2 == 0:
            median = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        else:
            median = sorted_values[n // 2]

        yield f"Group {group} - Median", median

if __name__ == '__main__':
    MedianOfGroup.run()

