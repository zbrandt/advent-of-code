""" Module for Advent of Code Day 9.
    https://adventofcode.com/2016/day/9
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re

re.DEBUG = False

def decomp(x, recur = True) -> int:
    expansion = 0
    pos = 0
    while m := re.search(r'(\((\d+)x(\d+)\))', x[pos:]):
        span = m.span(0)
        pos += span[1]
        width, mult = int(m.group(2)), int(m.group(3))
        subexp = width
        if recur:
            subexp = decomp(x[pos:pos+width], recur)
        expansion += subexp * mult - width - len(m.group(1))
        pos += width
    return len(x) + expansion

def main(fname):

    inp = fname.read().strip()
    print (f'Part 1: {decomp(inp, False)}')
    print (f'Part 1: {decomp(inp, True)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
