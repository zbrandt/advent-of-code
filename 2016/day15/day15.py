""" Module for Advent of Code Day 15.
    https://adventofcode.com/2016/day/15
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re
from math import prod

def invmod(a, f, m):
    for b in range(f):
        if (a + b*f) % m == 0:
            return b
    assert False

def time_discs(discs) -> int:
    dtime = 0
    for i,d in enumerate(discs):
        d['first'] = (d['size'] - d['pos']- d['dist']) % d['size']
        dprod = prod([1] + [d['size'] for d in discs[:i]])
        df = invmod (dtime - d['first'], dprod, d['size']) if i > 0 else d['first']
        dtime += df*dprod
        d['time'] = dtime
    return discs[-1]['time']

def main(fname):
    lines = re.findall(r'(?m)Disc #(\d) has (\d+) positions; at time=(\d), it is at position (\d).', fname.read())
    discs = [ {'dist': int(p[0]), 'size': int(p[1]), 'pos': int(p[3])} for p in lines ]

    print (f'Part 1: {time_discs(discs[0:-1])}')
    print (f'Part 2: {time_discs(discs[0:])}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
