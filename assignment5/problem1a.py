"""(a) Implement Murmur3_32 to compute 32-bit hash values in Python. Pay special attention to making sure you use bit
operations correctly. Read input as a byte sequence. You can use to_bytes and from_bytes functions of the int class
to perform the necessary conversions. Pay attention to byte order, and remember to force the use of 32-bit arithmetic
(use & 0xffffffff where necessary). (4 points)"""
import argparse
import struct


def murmur3_32(data, seed=0):
    def scramble(k):
        k = k * 0xcc9e2d51 & 0xffffffff
        k = ((k << 15) | (k >> 17)) & 0xffffffff
        k = k * 0x1b873593 & 0xffffffff
        return k

    hash_value = seed
    length = len(data)

    # Process the 4-byte chunks
    num_chunks = length // 4
    for i in range(num_chunks):
        k = struct.unpack("@I", data[:4])[0]
        hash_value ^= scramble(k)
        hash_value = ((hash_value << 13) | (hash_value >> 19)) & 0xffffffff
        hash_value = (hash_value * 5 + 0xe6546b64) & 0xffffffff

    # Process the remaining bytes
    remaining_bytes = length % 4
    k = 0
    for i in range(remaining_bytes):
        k <<= 8
        k |= data[length - 1 - i]

    hash_value ^= scramble(k)

    hash_value ^= length
    hash_value ^= (hash_value >> 16) & 0xffffffff
    hash_value = (hash_value * 0x85ebca6b) & 0xffffffff
    hash_value ^= (hash_value >> 13) & 0xffffffff
    hash_value = (hash_value * 0xc2b2ae35) & 0xffffffff
    hash_value ^= (hash_value >> 16) & 0xffffffff

    return hash_value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Murmur3_32')
    parser.add_argument('--data', type=str, default="hello wo", help='Data to be hashed')
    parser.add_argument('--seed', type=int, default=0, help='Seed value (default: 0)')

    args = parser.parse_args()

    data_bytes = args.data.encode()  # Convert the string to bytes
    result = murmur3_32(data_bytes, args.seed)
    print('Result:', hex(result))
