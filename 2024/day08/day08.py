""" Module for Advent of Code Day 8.
    https://adventofcode.com/2024/day/8
"""
# pylint: disable=line-too-long, missing-function-docstring
import sys
from collections import defaultdict
from itertools import combinations
import numpy as np

def main(fname) -> None:

    def pp_map() -> None:
        print (f'City Map {len(citymap[0])}x{len(citymap)}')
        print ('\n'.join(''.join(ch for ch in row) for row in citymap))

    def clip_to_city_limits(nodes):
        return np.unique(nodes[(nodes[:, 0] >= 0) & (nodes[:, 0] < len(citymap)) &
                               (nodes[:, 1] >= 0) & (nodes[:, 1] < len(citymap[0]))], axis=0)

    data = fname.read().strip()
    citymap = [list(row) for row in data.split()]
    freqs = defaultdict(list)
    for r,row in enumerate(citymap):
        for c,cell in enumerate(row):
            if cell != '.' and cell != '#':
                freqs[cell].append(np.array([r,c]))

    antinodes = np.array([p[1] + ((p[1] - p[0]) * mults) for v in freqs.values() for p in combinations(v,2) for mults in (1,-2)])
    antinodes = clip_to_city_limits(antinodes)

    diag = len(citymap) + len(citymap[0])
    antinodes2 = np.array([p[1] + ((p[1] - p[0]) * mults) for v in freqs.values() for p in combinations(v,2) for mults in range(-diag,diag)])
    antinodes2 = clip_to_city_limits(antinodes2)

    for p in antinodes2:
        if citymap[p[0]][p[1]] == '.':
            citymap[p[0]][p[1]] = '#'
    pp_map()

    print (f'Part 1: {len(antinodes)}')
    print (f'Part 1: {len(antinodes2)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
