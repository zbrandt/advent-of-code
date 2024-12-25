""" Module for Advent of Code Day 25.
    https://adventofcode.com/2024/day/25
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from itertools import product

def main(fname):
    w,h = 5,7
    data = fname.read()
    all_keys = []
    all_locks = []
    for keylock in re.findall(r'((?:[#\.]{5}\s){7})', data):
        grid = {(x,y):ch for y,row in enumerate(keylock.split('\n')) for x,ch in enumerate(row)}
        top = ''.join(grid[(x,0)] for x in range(w))
        if top == '#' * w:
            heights = [''.join(grid[(col,y)] for y in range(h)).index('.')-1 for col in range(w)]
            all_locks.append(heights)
        else:
            heights = [''.join(grid[(col,y)] for y in reversed(range(h))).index('.')-1 for col in range(w)]
            all_keys.append(heights)

    combos = product(all_locks, all_keys)
    print (f'{len(all_locks)} locks * {len(all_keys)} keys')
    fits = [all([l+k<=5 for l,k in zip(*c)]) for c in combos]
    print (f'Part 1: {sum(fits)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
