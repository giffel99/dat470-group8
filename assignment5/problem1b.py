import random
import string
import matplotlib.pyplot as plt
from problem1a import murmur3_32

alphanumeric_chars = string.ascii_letters + string.digits  # all alphanumeric characters

"""Create random strings in with length between 1 to 99 characters, <samples_per_length> strings of each length"""
samples_per_length = 1000
test_strings = [''.join(random.choices(alphanumeric_chars, k=length)) for length in range(1, 100) for _ in
                range(samples_per_length)]

print(test_strings)

# Calculate hash value and convert to
hash_values = [int(murmur3_32(string, seed=1234), 0) for string in test_strings]

# Plot histogram
plt.hist(hash_values, bins=100, edgecolor='black')
plt.xlabel('Hash Value')
plt.ylabel('Frequency')
plt.title('Hash value distribution')
plt.show()
