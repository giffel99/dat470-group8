from mrjob.job import MRJob
from mrjob.step import MRStep


class ApproximatedMedian(MRJob):
    """Most of the code in this function is the same as in task 2c. It makes a histogram out of the values in the
    dataset, then, it calculates the cumulative sum of the bin counts and identifies the bin
    where half of the total count lies. Finally, the approximated median is calculated
    as the midpoint of the identified bin range."""

    def configure_args(self):
        super(ApproximatedMedian, self).configure_args()
        self.add_passthru_arg('--min_value', type=float, help='Minimum value for data')
        self.add_passthru_arg('--max_value', type=float, help='Maximum value for data')
        self.add_passthru_arg('--num_bins', type=int, help='Number of bins for histogram')

    def mapper_init(self):
        self.min_value = self.options.min_value
        self.max_value = self.options.max_value
        self.num_bins = self.options.num_bins
        self.bin_size = (self.max_value - self.min_value) / self.num_bins
        self.bins = [f"{i / 100:.2f} - {(i + int(self.bin_size * 100) - 1) / 100:.2f}" for i in
                     range(int(self.min_value * 100), int(self.max_value * 100), int(self.bin_size * 100))]

    def mapper(self, _, line):
        _, _, value = line.strip().split('\t')
        value = float(value)
        bin_index = int((value - self.min_value) // self.bin_size)
        bin_index = min(bin_index, self.num_bins - 1)  # In case value is equal to max_value
        yield self.bins[bin_index], 1

    def reducer(self, bin_range, counts):
        yield None, (bin_range, sum(counts))

    def reducer_find_median(self, _, histogram_bins):
        total_count = 0
        bins_cumulative_sums = []

        # calculate the cumulative sum for each histogram bin
        for bin_range, count in histogram_bins:
            total_count += count
            bins_cumulative_sums.append((bin_range, total_count))

        median_count = total_count / 2
        median_bin = next(
            (bin_range for bin_range, cumulative_count in bins_cumulative_sums if cumulative_count >= median_count),
            None)

        # Approximate the median by taking the mean of the bin range
        lower, upper = [float(x) for x in median_bin.split(" - ")]
        approx_median = (lower + upper) / 2
        yield "Approximated Median", approx_median

    def steps(self):
        return [MRStep(mapper_init=self.mapper_init, mapper=self.mapper, reducer=self.reducer),
                MRStep(reducer=self.reducer_find_median)]


if __name__ == '__main__':
    ApproximatedMedian.run()
