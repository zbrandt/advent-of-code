""" Module for Advent of Code Day 14.
    https://adventofcode.com/2016/day/14
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
from collections import defaultdict
import hashlib
import re

def nlets(triplets, pentuplets, salt:str, idx:int, stretch:int) -> bool:
    inpx = salt + str(idx)
    result = hashlib.md5(inpx.encode("utf-8")).hexdigest()
    for _ in range(stretch):
        result = hashlib.md5(result.encode("utf-8")).hexdigest()
    for m in re.finditer(r'(([a-z0-9])\2\2)', result):
        ch = m.group(2)
        triplets[idx].add(ch)
        break
    for m in re.finditer(r'(([a-z0-9])\2\2\2\2)', result):
        ch = m.group(2)
        pentuplets[ch].append(idx)

def execute(salt, stretch):
    idx = 0
    keys = []
    triplets = defaultdict(set)
    pentuplets = defaultdict(list)
    while len(keys) < 64:
        nlets(triplets, pentuplets, salt, idx, stretch)
        if idx >= 1000:
            midx = idx - 1000
            iskey = False
            for t in triplets[midx]:
                iskey |= any(p for p in pentuplets[t] if midx < p <= idx)
            if iskey:
                #print (f'found key {midx=} {idx=} {triplets[midx]=} {pentuplets[list(triplets[midx])[0]]=}')
                keys.append(midx)
        idx += 1
    return keys[-1]

def main(_):
    #salt = 'abc'
    salt = 'ihaygndm'
    print (f'Part 1: {execute(salt, 0)}')
    print (f'Part 1: {execute(salt, 2016)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
