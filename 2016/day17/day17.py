""" Module for Advent of Code Day 17.
    https://adventofcode.com/2016/day/17
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import hashlib
from collections import deque

dirs = [-1j**i for i in range(4)]
dirs_map = dict(zip(dirs,'LURD'))
lurd_map = dict(zip('LURD', dirs))
dirs = [lurd_map[ch] for ch in 'UDLR']

def get_doors (pos:complex, inp:str, path:str) -> list[complex]:
    hd = hashlib.md5((inp+path).encode("utf-8")).hexdigest()
    doors = [dxy for i, dxy in enumerate(dirs) if int(hd[i], 16) > 10 and 0 <= (pos+dxy).real < 4 and 0 <= (pos+dxy).imag < 4]
    return doors

def main(inp):
    end = 3+3j
    d = deque([(0j, '')])
    solns = []
    while d:
        pos, path = d.popleft()
        if pos == end:
            solns.append(path)
            continue
        for dxy in get_doors(pos, inp, path):
            d.append((pos+dxy, path + dirs_map[dxy]))

    print (f'For input "{inp}", there are {len(solns)} good paths.')
    if solns:
        shortest = min(solns, key=len)
        longest = max(solns, key=len)
        print (f'Part 1: shortest path "{shortest}" has length {len(shortest)}.')
        print (f'Part 2: longest test path has length {len(longest)}.')

if __name__ == "__main__":
    main(sys.argv[1])
