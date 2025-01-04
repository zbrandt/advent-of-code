""" Module for Advent of Code Day 25.
    https://adventofcode.com/2015/day/25
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

def get_pos(row, col):
    return ((((row-1)+col)**2) - (row-col-1))//2

def nxt(x):
    return x * 252533 % 33554393

def main(fname):
    row, col = [int(digits) for digits in re.findall(r'(\d+)', fname.read())]
    code = 20151125
    x = get_pos(row, col)
    for _ in range(x-1):
        code = nxt(code)

    print (f'Part 1: {code}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
