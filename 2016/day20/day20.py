""" Module for Advent of Code Day 20.
    https://adventofcode.com/2016/day/20
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
from operator import sub

def main(fname):
    blacklist = sorted([x for line in fname.readlines() for x in list(zip(map(int, line.strip().split('-')),(+1,-1))) ])
    max = (10-1,2**32-1)[len(blacklist) > 100]
    blacklist += [[max+1,0]]

    xpos = 0
    height = 0
    good = []
    for dz in blacklist:
        if xpos+1 <= dz[0]-1:
            if height == 0:
                good += [[xpos+1, dz[0]]]
        xpos = dz[0]
        height += dz[1]
    total = sum(-sub(*p) for p in good)
    print (f'Part 1: {good[0][0]}')
    print (f'Part 1: {total}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
