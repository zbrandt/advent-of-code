""" Module for Advent of Code Day 16.
    https://adventofcode.com/2016/day/16
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
from itertools import batched

def dragon(x:str) -> str:
    return x + '0' + ''.join(chr(ord(ch)^1) for ch in x[-1::-1])

def checksum(x:str) -> str:
    while True:
        x = ''.join(('0','1')[p[0] == p[1]] for p in batched(x,2))
        if len(x) & 1:
            break
    return x

def main(fname):
    data, *disklen = fname.read().split()
    disklen = list(map(int,disklen))
    for i, dl in enumerate(disklen):
        while len(data) < dl:
            data = dragon(data)
        cs = checksum(data[:dl])
        print (f'Part {i+1}: {cs}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
