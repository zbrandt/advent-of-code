""" Module for Advent of Code Day 1.
    https://adventofcode.com/2015/day/1
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys

def main(fname):
    parens = list(fname.read().strip())
    depth, basement = 0, 0
    for i,p in enumerate(parens):
        depth += (-1,+1)[p =='(']
        if depth < 0 and basement == 0:
            basement = i+1
    print (f'Part 1: {depth}')
    print (f'Part 2: {basement}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
