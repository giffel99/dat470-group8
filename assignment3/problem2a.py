from mrjob.job import MRJob
import math
import time


class SummaryStatistics(MRJob):

    def mapper(self, _, line):
        id_, group, value = line.strip().split('\t')
        value = float(value)
        yield None, (value, value ** 2, 1, value, value)

    def combiner(self, _, values):
        sum_, sum_sq, count, min_value, max_value = 0, 0, 0, float('inf'), float('-inf')
        for value, value_sq, n, min_val, max_val in values:
            sum_ += value
            sum_sq += value_sq
            count += n
            min_value = min(min_value, min_val)
            max_value = max(max_value, max_val)

        yield None, (sum_, sum_sq, count, min_value, max_value)

    def reducer(self, _, values):
        sum_, sum_sq, count, min_value, max_value = 0, 0, 0, float('inf'), float('-inf')
        for value, value_sq, n, min_val, max_val in values:
            sum_ += value
            sum_sq += value_sq
            count += n
            min_value = min(min_value, min_val)
            max_value = max(max_value, max_val)

        mean = sum_ / count
        std_dev = math.sqrt((sum_sq / count) - mean ** 2)
        yield "Mean", mean
        yield "Standard Deviation", std_dev
        yield "Minimum", min_value
        yield "Maximum", max_value


if __name__ == '__main__':
    SummaryStatistics.run()
