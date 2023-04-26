import findspark

findspark.init()

from pyspark import SparkContext
import argparse


def main(data_path, min_value, max_value, num_bins):
    sc = SparkContext(master='local[2]')

    # Constructing an RDD from the data file
    data = sc.textFile(data_path)

    # Extracting the value field in the data
    values = data.map(lambda line: float(line.split('\t')[2]))

    # Calculate the bin counts for the histogram
    histogram = (
        values.map(lambda value: (get_bin_index(value, min_value, max_value, num_bins), 1))
        .reduceByKey(lambda a, b: a + b)
        .sortByKey()
    )

    # Collect the bin counts for the histogram
    histogram_counts = histogram.collect()

    # Calculate the total count
    total_count = sum(count for _, count in histogram_counts)

    # Calculate the cumulative sum for each histogram bin
    bins_cumulative_sums = []
    cumulative_sum = 0
    for bin_range, count in histogram_counts:
        cumulative_sum += count
        bins_cumulative_sums.append((bin_range, cumulative_sum))

    # Find the median bin
    median_count = total_count / 2
    median_bin_range = next(
        (bin_range for bin_range, cumulative_count in bins_cumulative_sums if cumulative_count >= median_count),
        None)

    # Approximate the median by taking the mean of the median bin range
    lower, upper = [float(x) for x in median_bin_range.split(" - ")]
    approx_median = (lower + upper) / 2

    print(f"Approximated Median: {approx_median}")


def get_bin_index(value, min_value, max_value, num_bins):
    bin_size = (max_value - min_value) / num_bins
    bin_index = int((value - min_value) // bin_size)
    bin_index = min(bin_index, num_bins - 1)

    lower = min_value + bin_index * bin_size
    upper = min_value + (bin_index + 1) * bin_size
    return f"{lower} - {upper}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PySpark Approximated Median")
    parser.add_argument('--data_path', type=str, required=True, help="Path to the input data file")
    parser.add_argument('--num_bins', type=int, default=10, help='Number of bins for histogram')
    parser.add_argument('--min_value', type=float, required=True, help='Minimum value for data')
    parser.add_argument('--max_value', type=float, required=True, help='Maximum value for data')
    args = parser.parse_args()

    main(args.data_path, args.min_value, args.max_value, args.num_bins)
