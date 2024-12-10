""" Module for Advent of Code Day 10.
    https://adventofcode.com/2024/day/10
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import Counter

def main(fname) -> None:

    dirs = ((-1,0),(0,-1),(0,1),(1,0))

    def find_nines_set(points, val) -> set:
        #print (f'{' ' * (val-1)}find_nines_set({points}, {val})')
        oneup = set([rc2 for rc in points for d in dirs for rc2 in [tuple([rc[xy] + d[xy] for xy in [0,1]])] if topomap.get(rc2, '.') == val])
        if val < 9:
            return find_nines_set(oneup, val+1)
        return oneup

    def find_nines_counter(points:Counter, val) -> Counter:
        #print (f'{' ' * (val-1)}find_nines_counter({points}, {val})')
        oneup = Counter([rc2 for rc,cnt in points.items() for _ in range(cnt) for d in dirs for rc2 in [tuple([rc[xy] + d[xy] for xy in [0,1]])] if topomap.get(rc2, '.') == val])
        if val < 9:
            return find_nines_counter(oneup, val+1)
        return oneup

    topomap = { (r,c) : int(h) for r,row in enumerate(fname) for c,h in enumerate(row.strip()) if h.isdigit() }
    zeroes = [k for k,v in topomap.items() if v == 0]

    scores1 = [len(set(find_nines_set(set([z]),1))) for z in zeroes]
    scores2 = [find_nines_counter(Counter([z]),1).total() for z in zeroes]

    print (f'Part 1: {sum(scores1)}')
    print (f'Part 2: {sum(scores2)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
