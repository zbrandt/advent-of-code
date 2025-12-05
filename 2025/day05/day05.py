""" Module for Advent of Code Day 5.
    https://adventofcode.com/2025/day/5
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
#mport numpy as np
#from scipy.signal import convolve2d

def main(fname):
    lines = [line.split('-') for line in fname.read().split()]
    ranges = [list(map(int,x)) for x in lines if len(x) == 2]
    ingredients = [int(x[0]) for x in lines if len(x) == 1]

    p1 = sum( any(lo <= i <= hi for lo, hi in ranges) for i in ingredients)

    updown = [(r[0], 1) for r in ranges] + [(r[1], -1) for r in ranges]
    updown.sort(key=lambda x: (x[0], -x[1]))

    elev = last = p2 = 0
    for pos, delta in updown:
        elev += delta
        if elev > 0:
            p2 +=  pos - last + 1 * (elev - delta == 0)
        last = pos

    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
