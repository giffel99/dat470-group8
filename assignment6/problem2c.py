from pybloom_live import BloomFilter

vocabulary_path = "/data/2023-DAT470-DIT065/vocabulary_nytimes.txt"
set_a_path = "/data/2023-DAT470-DIT065/docs_nytimes_a.txt"
set_b_path = "/data/2023-DAT470-DIT065/docs_nytimes_b.txt"

universe_size = 102660
false_positive_rate = 0.01


def get_set(filepath: str) -> set:
    vocab_set = set()
    with open(filepath, 'r') as file:
        for line in file:
            words = [int(word) for word in line.strip().split()]
            vocab_set.update(words)
    return vocab_set


def get_bloom_filter(vocabulary_set: set, n: int, f: float) -> BloomFilter:
    bloom_filter = BloomFilter(capacity=n, error_rate=f)

    for word in vocabulary_set:
        bloom_filter.add(word)

    return bloom_filter


def get_vocabulary() -> set:
    # Just disregard the actual word and just use the number
    vocab_set = set()

    with open(vocabulary_path, "r") as file:
        for line in file:
            word_number = int(line.strip().split()[0])
            vocab_set.add(word_number)
    return vocab_set


def calculate_false_positive_rate(vocabulary: set, bloom_filter: BloomFilter, actual_set: set) -> float:
    false_positives = 0
    for word in vocabulary:
        if word not in actual_set and word in bloom_filter:
            false_positives += 1

    total_negatives = len(vocabulary) - len(actual_set)

    return false_positives / total_negatives


if __name__ == "__main__":
    vocabulary = get_vocabulary()
    set_a = get_set(set_a_path)
    set_b = get_set(set_b_path)

    bloom_filter_a = get_bloom_filter(set_a, universe_size, false_positive_rate)
    bloom_filter_b = get_bloom_filter(set_b, universe_size, false_positive_rate)

    false_positive_rate_a = calculate_false_positive_rate(vocabulary, bloom_filter_a, set_a)
    false_positive_rate_b = calculate_false_positive_rate(vocabulary, bloom_filter_b, set_b)

    print("Empirical false positive rate, set A:", false_positive_rate_a)
    print("Empirical false positive rate, set B:", false_positive_rate_b)
