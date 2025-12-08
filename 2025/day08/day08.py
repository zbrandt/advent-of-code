""" Module for Advent of Code Day 8.
    https://adventofcode.com/2025/day/8
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import math
import numpy as np
from itertools import combinations

def group_connected_pairs(pairs, checkpoint):
    groups = []
    p1 = p2 = 0

    for pc, (a, b) in enumerate(pairs):
        found_in_groups = []
        fa = fb = False
        for i, group in enumerate(groups):
            if a in group or b in group:
                found_in_groups.append(i)
            fa = fa or a in group
            fb = fb or b in group
        
        if not fa or not fb:
            p2 = list(a)[0] * list(b)[0]

        if not found_in_groups:
            # Neither 'a' nor 'b' found in existing groups, create a new one
            groups.append({a, b})
        elif len(found_in_groups) == 1:
            # One group contains either 'a' or 'b', add the other element
            groups[found_in_groups[0]].add(a)
            groups[found_in_groups[0]].add(b)
        else:
            # Both 'a' and 'b' (or their connected elements) are in different groups,
            # merge these groups and add any new elements
            merged_group = set()
            for index in sorted(found_in_groups, reverse=True):
                merged_group.update(groups.pop(index))
            merged_group.add(a)
            merged_group.add(b)
            groups.append(merged_group)
        
        if pc+1 == checkpoint:
            p1 = math.prod(sorted([len(x) for x in groups], reverse=True)[:3])

    return p1, p2

def main(fname):
    boxes = np.genfromtxt(fname, dtype=int, delimiter=",")
    d2s = [((tuple(map(int,pair[0])),tuple(map(int,pair[1]))), np.sum(np.square(pair[1] - pair[0]))) for pair in combinations(boxes, 2)]
    d2s.sort(key=lambda x : x[1])

    checkpoint = (1000,10)[len(boxes) <= 20]
    p1, p2 = group_connected_pairs([x[0] for x in d2s], checkpoint)

    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
