""" Module for Advent of Code Day 1.
    https://adventofcode.com/2024/day/1
"""
import sys
import numpy as np

def main(fname):
    """Read two colums of integers and compute total distance and similarity scores."""
    # Read a table of numbers, transpose, and sort
    left, right = np.sort(np.loadtxt(fname, int).T)

    # Part 1 is sum of distance between left & right values
    print(f'Part 1: total_distance = {np.sum(np.abs(left-right))}')

    # Part 2 is sum of all right values found in left
    print(f'Part 2: similarity_score = {np.sum(np.isin(right, left) * right)}')

if __name__ == "__main__":
    arg = sys.stdin
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    main(arg)
