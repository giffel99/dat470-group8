from pybloom_live import BloomFilter

vocabulary_file = "/data/2023-DAT470-DIT065/vocabulary_nytimes.txt"
set_a_file = "/data/2023-DAT470-DIT065/docs_nytimes_a.txt"
set_b_file = "/data/2023-DAT470-DIT065/docs_nytimes_b.txt"

universe_size = 102660
false_positive_rate = 0.01


def read_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


def convert_to_set(lines):
    vocab_set = set()
    for line in lines:
        words = [int(word) for word in line.split()]
        vocab_set.update(words)
    return vocab_set


def get_bloom_filter(vocab_set, n, f):
    bloom_filter = BloomFilter(capacity=n, error_rate=f)

    for word in vocab_set:
        bloom_filter.add(word)

    return bloom_filter


if __name__ == "__main__":
    vocabulary_lines = read_file(vocabulary_file)
    set_a_lines = read_file(set_a_file)
    set_b_lines = read_file(set_b_file)

    vocabulary = convert_to_set(vocabulary_lines)
    set_a = convert_to_set(set_a_lines)
    set_b = convert_to_set(set_b_lines)

    bloom_filter_a = get_bloom_filter(set_a, universe_size, false_positive_rate)
    bloom_filter_b = get_bloom_filter(set_b, universe_size, false_positive_rate)
