""" Module for Advent of Code Day 1.
    https://adventofcode.com/2016/day/1
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from collections import defaultdict

def dist(p):
    if p is None:
        return 0
    return int(abs(p.real) + abs(p.imag))

def main(fname):
    inst = [((-1j,1j)[t=='L'],int(d)) for t,d in re.findall(r'(R|L)(\d+)', fname.read())]
    path = defaultdict(int)
    cross = None
    pos = 0+0j
    dir = 1j
    path[pos] += 1
    for turn, steps in inst:
        dir *= turn
        for _ in range(steps):
            pos += dir
            if path[pos] and cross is None:
                cross = pos
            path[pos] += 1
    print (f'Part 1: {dist(pos)}')
    print (f'Part 2: {dist(cross)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
