""" Module for Advent of Code Day 2.
    https://adventofcode.com/2015/day/2
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from itertools import combinations
from operator import mul
from functools import reduce

def main(fname):
    boxes = [list(map(int,line.split('x'))) for line in fname.read().strip().split('\n')]
    paper = [sum(list(map(lambda x:reduce(mul,x,1),combinations(box, 2))))*2 + min(list(map(lambda x:reduce(mul,x,1),combinations(box, 2)))) for box in boxes]
    ribbon = [min(list(map(sum,combinations(box, 2))))*2 + reduce(mul, box, 1) for box in boxes]
    print (f'Part 1: {sum(paper)}')
    print (f'Part 2: {sum(ribbon)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
