from mrjob.job import MRJob
import math
import time

class MedianOfGroup(MRJob):

    def mapper(self, _, line):
        fields = line.strip().split('\t')
        if len(fields) != 3:
            print(f"Skipping bad line: {line}")
            return  # Skip this line - doesn't have the correct format
        
        group = fields[1]
        value = float(fields[2])

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

