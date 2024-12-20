""" Module for Advent of Code Day 3.
    https://adventofcode.com/2015/day/3
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import defaultdict

dlook = { '^':(0,-1), '>':(1,0), 'v':(0,1), '<':(-1,0) }

def tadd(a,b):
    return (a[0]+b[0], a[1]+b[1])

def main(fname):
    dxys = [dlook[ch] for ch in list(fname.read().strip())]

    for movers in [1,2]:
        santa = [(0,0) for _ in range(movers)]
        gifts = defaultdict(int)
        for dxy in santa:
            gifts[dxy] += 1
        for i, dxy in enumerate(dxys):
            santa[i % movers] = tadd(santa[i % movers],dxy)
            gifts[santa[i % movers]] += 1
        print (f'Part {movers}: {len(gifts)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
