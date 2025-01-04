""" Module for Advent of Code Day 24.
    https://adventofcode.com/2015/day/24
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from itertools import combinations
from math import prod

def find_smallest_nth(packages, nth):
    i = 1
    good = []
    target = sum(packages) // nth
    while not good:
        combs = list(combinations(packages, i+1))
        good = [x for x in combs if sum(x) == target]
        i += 1
    prods = [prod(g) for g in good]
    return min(prods)

def main(fname):
    packages = sorted(list(map(int,fname.read().strip().split('\n'))))
    for i in range(2):
        print (f'Part {i+1}: {find_smallest_nth(packages, 3+i)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
