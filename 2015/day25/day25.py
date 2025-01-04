""" Module for Advent of Code Day 25.
    https://adventofcode.com/2015/day/25
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

def get_pos(row, col):
    x = ((((row-1)+col)**2) - (row-col-1))//2
    #print (f'pos({row=}, {col=}) ==> {x}')
    return (x)

def nxt(x):
    return x * 252_533 % 33_554_393

def main(fname):

    row, col = [int(digits) for digits in re.findall(r'(\d+)', fname.read())]
    code = 20_151_125
    x = get_pos(row, col)
    for i in range(x-1):
        if i % (1000-31) == 0:
            print (f'{i+1}/{x}', end='\r')
        code = nxt(code)
    print (' '*20, end='\r')

    print (f'Part 1: {code}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
