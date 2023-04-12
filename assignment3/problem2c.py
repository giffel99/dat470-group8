from mrjob.job import MRJob
import math
import time

class Histogram(MRJob):
    def configure_args(self):
        super(Histogram, self).configure_args()
        self.add_passthru_arg('--min_value', type=float, help='Minimum value for histogram binning')
        self.add_passthru_arg('--max_value', type=float, help='Maximum value for histogram binning')

    def mapper_init(self):
        self.min_value = self.options.min_value
        self.max_value = self.options.max_value
        self.num_bins = 10
        self.bin_size = (self.max_value - self.min_value) / self.num_bins

    def mapper(self, _, line):
        _, _, value = line.strip().split('\t')
        value = float(value)
        bins = [f"{i / 100:.2f} - {(i + int(self.bin_size * 100) - 1) / 100:.2f}" for i in
                range(int(self.min_value * 100), int(self.max_value * 100), int(self.bin_size * 100))]
        bin_index = int((value - self.min_value) // self.bin_size)
        bin_index = min(bin_index, self.num_bins - 1)  # In case value is equal to max_value
        yield bins[bin_index], 1

    def reducer(self, bin_index, counts):
        yield bin_index, sum(counts)

if __name__ == '__main__':
    start_time = time.time()
    Histogram.run()
    end_time = time.time()
    total_time = end_time - start_time

    print(f"Execution time: {total_time}")
