""" Module for Advent of Code Day 18.
    https://adventofcode.com/2016/day/18
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
from functools import cache

def triplewise(iterable):
    iterator = iter(iterable)
    a,b = next(iterator, None), next(iterator, None)
    yield '.', a, b
    for c in iterator:
        yield a, b, c
        a,b = b,c
    yield a, b, '.'

@cache
def convolve(t) -> bool:
    t = list(map(ord,t))
    return ('.','^')[bool((t[0] ^ t[1]) ^ (t[1] ^ t[2]))]

def main(fname):
    first = fname.read().strip()
    rowcounts = (10, 40, 400000)
    for i, rowcount in enumerate(rowcounts):
        row = first
        rows = [row] + [row := ''.join(convolve(t) for t in triplewise(row)) for _ in range(rowcount-1)]
        print (f'Part {i}: {rowcount} rows have safe tiles: {''.join(rows).count('.')}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
