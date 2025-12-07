""" Module for Advent of Code Day 7.
    https://adventofcode.com/2025/day/7
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import Counter

def main(fname):
    p1 = p2 = 0
    splits = [x for x in [set([i for i,c in enumerate(line) if c == '^' or c =='S']) for line in fname.readlines()] if len(x)]
    
    beams = splits[0]
    cbeams = Counter(beams)
    print (f'{beams=}')
    for s in splits[1:]:
        hits = beams.intersection(s)
        p1 += len(hits)
        beams = (beams - hits) | set(hit-1 for hit in hits) | set(hit+1 for hit in hits)
        for hit in hits:
            cbeams[hit-1] += cbeams[hit]
            cbeams[hit+1] += cbeams[hit]
            del cbeams[hit]
        #print (f'{cbeams=}')
    p2 = sum(cbeams.values())

    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
