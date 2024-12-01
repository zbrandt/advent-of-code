""" Module for Advent of Code Day 1.
    https://adventofcode.com/2024/day/1
"""
import sys
from collections import Counter
import numpy as np

def main(src_file):
    """Read two colums of integers and compute total distance and similarity scores."""
    # Read all numbers
    all_nums = np.fromstring(src_file.read(), dtype=int, sep=' ')

    # Split the numbers into left and right lists
    left_nums = all_nums[0::2]
    right_nums = all_nums[1::2]

    # Calculate distances between sorted lists
    distances = np.abs(np.sort(left_nums) - np.sort(right_nums))

    # Use Counter to count occurrences in the right list
    right_counts = Counter(right_nums)

    # Calculate similarity score using numpy arrays
    right_counts_array = np.array([right_counts[x] for x in left_nums])
    similarity = left_nums * right_counts_array

    # Output results
    print(f'Part 1: total_distance = {np.sum(distances)}')
    print(f'Part 2: similarity_score = {np.sum(similarity)}')

if __name__ == "__main__":
    file = sys.stdin
    if len(sys.argv) > 1:
        # Read from the provided file
        with open(sys.argv[1], mode='r', encoding="utf-8") as file:
            main(file)
    else:
        # Read from stdin
        main(sys.stdin)
