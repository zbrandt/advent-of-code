""" Module for Advent of Code Day 4.
    https://adventofcode.com/2025/day4
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import numpy as np
from scipy.signal import convolve2d

def main(fname):
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int8)

    cgrid = np.genfromtxt(fname, dtype='U1', delimiter=1)
    ngrid = (cgrid == '@').astype(np.int8)
    
    p1 = p2 = 0
    while True:
        neighbor_sums = convolve2d(ngrid, kernel, mode='same')
        result = ((neighbor_sums < 4) & (ngrid == 1)).astype(np.int8)
        ngrid = ngrid - result
        inc = result.sum()
        if inc == 0:
            break
        if p1 == 0:
            p1 = inc
        p2 += inc

    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
