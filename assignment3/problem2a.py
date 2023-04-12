from mrjob.job import MRJob
import math
import time

class SummaryStatistics(MRJob):

    #def configure_args(self):
    #    super(SummaryStatistics, self).configure_args()
    #    self.add_passthru_arg('--num-cores', type=int, default=1, help='Number of cores')

    def mapper(self, _, line):
        fields = line.strip().split('\t')
        if len(fields) != 3:
            print(f"Skipping bad line: {line}")
            return  # Skip this line - doesn't have the correct format
        
        id_, group, value = map(float, fields)

        yield None, (value, value**2, 1, value, value)
    
    def reducer(self, _, values):
        sum_, sum_sq, count, min_value, max_value = 0, 0, 0, float('inf'), float('-inf')
        for value, value_sq, n, min_val, max_val in values:
            sum_ += value
            sum_sq += value_sq
            count += n
            min_value = min(min_value, min_val)
            max_value = max(max_value, max_val)

        mean = sum_ / count
        std_dev = math.sqrt((sum_sq / count) - mean**2)
        yield "Mean", mean
        yield "Standard Deviation", std_dev
        yield "Minimum", min_value
        yield "Maximum", max_value

if __name__ == '__main__':
    start_time = time.time()
    SummaryStatistics.run()
    end_time = time.time()
    total_time = end_time - start_time

    print(f"Execution time: {total_time}")


