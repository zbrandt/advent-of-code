""" Module for Advent of Code Day 8.
    https://adventofcode.com/2024/day/8
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import defaultdict
from itertools import combinations
import numpy as np

class CityMap:

    def pp(self) -> None:
        print (f'City Map {self.w}x{self.h}')
        print ('\n'.join(''.join(ch for ch in row) for row in self.grid))

    def clip_to_city_limits(self, nodes):
        return np.unique(nodes[(nodes[:, 0] >= 0) & (nodes[:, 0] < self.h) &
                               (nodes[:, 1] >= 0) & (nodes[:, 1] < self.w)], axis=0)

    def mark_antinodes(self, nodes):
        for p in nodes:
            if self.grid[p[0]][p[1]] == '.':
                self.grid[p[0]][p[1]] = '#'

    def __init__(self, fname):
        data = fname.read().strip()
        self.grid = [list(row) for row in data.split()]
        self.h = len(self.grid)
        self.w = len(self.grid[0])
        self.freqs = defaultdict(list)
        for r,row in enumerate(self.grid):
            for c,cell in enumerate(row):
                if cell != '.' and cell != '#':
                    self.freqs[cell].append(np.array([r,c]))

        self.antinodes = np.array([p[1] + ((p[1] - p[0]) * mults) for v in self.freqs.values() for p in combinations(v,2) for mults in (1,-2)])
        self.antinodes = self.clip_to_city_limits(self.antinodes)

        diag = self.w + self.h
        self.antinodes2 = np.array([p[1] + ((p[1] - p[0]) * mults) for v in self.freqs.values() for p in combinations(v,2) for mults in range(-diag,diag)])
        self.antinodes2 = self.clip_to_city_limits(self.antinodes2)


def main(fname) -> None:

    city = CityMap(fname)

    city.mark_antinodes(city.antinodes2)
    city.pp()

    print (f'Part 1: {len(city.antinodes)}')
    print (f'Part 1: {len(city.antinodes2)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
