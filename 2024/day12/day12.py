""" Module for Advent of Code Day 12.
    https://adventofcode.com/2024/day/12
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import defaultdict
from collections import deque
from functools import reduce
from operator import or_

class GardenGroups:
    def __init__(self, data):
        self.grid = {(r,c): ch for r,row in enumerate(data.split()) for c,ch in enumerate(row)}
        self.areas = self.find_areas()
        self.perims = {k:sum(4 - self.friends(p) for p in v) for k,v in self.areas.items()}
        self.sides = {k:self.count_sides(v) for k,v in self.areas.items()}

    dirs = [(-1,0),(0,-1),(1,0),(0,1)] # right / clockwise

    @staticmethod
    def tuple_add(a:tuple, b:tuple) -> tuple:
        return tuple([a+b for a,b in zip(a,b)])

    def friends(self, p) -> int:
        return sum(self.grid[p] == self.grid[self.tuple_add(p,d)] for d in self.dirs if self.tuple_add(p,d) in self.grid)

    def count_sides(self, area) -> int:
        mask = {p: reduce(or_, [(1 << i) for i,d in enumerate(self.dirs) if self.tuple_add(p,d) not in area], 0) for p in area}
        sides =  sum([v & bit != mask.get((k[0]-1,k[1]-0), 0) & bit for bit in [1<<1,1<<3] for k,v in mask.items()])
        sides += sum([v & bit != mask.get((k[0]-0,k[1]-1), 0) & bit for bit in [1<<0,1<<2] for k,v in mask.items()])
        return sides

    def find_areas(self) -> defaultdict:
        areas = defaultdict(set)
        visited = set()
        for root in self.grid.keys():
            if root in visited:
                continue
            ch = self.grid[root]
            q = deque([root])
            while q:
                p = q.popleft()
                if p in visited:
                    continue
                q.extend(x for d in self.dirs for x in [self.tuple_add(p,d)] if x in self.grid and self.grid[x] == ch and x not in visited)
                visited.add(p)
                areas[root].add(p)
        return areas

    def price_list(self, factor, verbose=False) -> int:
        prices = []
        for k,v in self.areas.items():
            prices.append(len(v) * factor[k])
            if verbose:
                print (f'A region of {self.grid[k]} plants with price {len(v)} * {factor[k]} = {prices[-1]}.')
        return sum(prices)

def main(fname) -> None:
    gg = GardenGroups(fname.read())
    print (f'Part 1: {gg.price_list(gg.perims, True)}')
    print (f'Part 2: {gg.price_list(gg.sides, True)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
