from mrjob.job import MRJob
import math
import time


class Histogram(MRJob):
    def configure_args(self):
        super(Histogram, self).configure_args()
        self.add_passthru_arg('--min_value', type=float, help='Minimum value for data')
        self.add_passthru_arg('--max_value', type=float, help='Maximum value for data')

    def mapper_init(self):
        self.min_value = self.options.min_value
        self.max_value = self.options.max_value
        self.num_bins = 10
        self.bin_size = (self.max_value - self.min_value) / self.num_bins
        self.bins = [f"{i / 100:.2f} - {(i + int(self.bin_size * 100) - 1) / 100:.2f}" for i in
                     range(int(self.min_value * 100), int(self.max_value * 100), int(self.bin_size * 100))]

    def mapper(self, _, line):
        _, _, value = line.strip().split('\t')
        value = float(value)
        bin_index = int((value - self.min_value) // self.bin_size)
        bin_index = min(bin_index, self.num_bins - 1)  # In case value is equal to max_value
        yield self.bins[bin_index], 1

    def reducer(self, bin_index, counts):
        yield bin_index, sum(counts)


if __name__ == '__main__':
    Histogram.run()
