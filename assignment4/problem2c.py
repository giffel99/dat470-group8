import findspark
findspark.init()
import random
from pyspark import SparkContext
import argparse


def get_bin_index(value, min_value, max_value, num_bins):
    bin_size = (max_value - min_value) / num_bins
    bin_index = int((value - min_value) // bin_size)
    return min(bin_index, num_bins - 1)

def get_bin_range(bin_index, min_value, max_value, num_bins):
    bin_size = (max_value - min_value) / num_bins
    lower_bound = min_value + bin_index * bin_size
    upper_bound = lower_bound + bin_size
    return f"{lower_bound:.2f} - {upper_bound:.2f}"

def main(data_path, min_value, max_value, num_bins):

    sc = SparkContext(master = 'local[2]')

    # Constructing an RDD from the data file 
    data = sc.textFile(data_path)

    # Extracting the value field in the data
    values = data.map(lambda line: float(line.split('\t')[2]))

    # Calculating the bin counts for the histogram by applying a map function to each value and its corresponding bin index 
    # ReduceByKey will add the counts together and sortByKey will ensure the output is in the right order. 
    histogram = (
        values.map(lambda value: (get_bin_index(value, min_value, max_value, num_bins), 1))
              .reduceByKey(lambda a, b: a + b)
              .sortByKey()
    )

    # Collect the bin counts for the histogram and printing it with value ranges for each bin
    histogram_counts = histogram.collect()
    for bin_index, count in histogram_counts:
        bin_range = get_bin_range(bin_index, min_value, max_value, num_bins)
        print(f"Bin {bin_index} ({bin_range}): {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PySpark Histogram")
    parser.add_argument('--data_path', type=str, required=True, help="Path to the input data file")
    parser.add_argument('--num_bins', type=int, default=10, help='Number of bins for histogram')
    parser.add_argument('--min_value', type=float, required=True, help='Minimum value for data')
    parser.add_argument('--max_value', type=float, required=True, help='Maximum value for data')
    args = parser.parse_args()

    main(args.data_path, args.min_value, args.max_value, args.num_bins)

