""" Module for Advent of Code Day 12.
    https://adventofcode.com/2024/day/12
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import defaultdict
from collections import deque

def main(fname) -> None:

    dirs = [(-1,0),(0,-1),(1,0),(0,1)] # right / clockwise

    def tuple_add(a:tuple[int,int], b:tuple[int,int]) -> tuple[int,int]:
        return (a[0]+b[0],a[1]+b[1])

    def matching_neigbors(p):
        return sum(grid[p] == grid[tuple_add(p,d)] for d in dirs if tuple_add(p,d) in grid)   

    def count_sides(root, area) -> int:
        horz = dict()
        vert = dict()
        sides = 0
        for p in area:
            if (p[0],p[1]-1) not in area:
                horz[p] = 1
            if (p[0],p[1]+1) not in area:
                horz[(p[0],p[1]+1)] = 2
            if (p[0]-1,p[1]) not in area:
                vert[p] = 1
            if (p[0]+1,p[1]) not in area:
                vert[(p[0]+1,p[1])] = 2
        sides += sum([horz.get(p,0) != horz.get((p[0]-1,p[1]), 0) for p in horz])
        sides += sum([vert.get(p,0) != vert.get((p[0],p[1]-1), 0) for p in vert])
        return sides


    grid = {(r,c): ch for r,row in enumerate(fname.read().split()) for c,ch in enumerate(row)}
    H = max(k[0] for k in grid.keys())+1
    W = max(k[1] for k in grid.keys())+1    
    areas = defaultdict(set)
    visited = {}

    for r in range(H):
        for c in range(W):
            root = (r,c)
            if root in visited:
                continue
            ch = grid[root]
            q = deque([root])
            while q:
                p = q.popleft()
                if p in visited:
                    continue
                q.extend(x for d in dirs for x in [tuple_add(p,d)] if x in grid and grid[x] == ch and x not in visited)
                visited[p] = True
                areas[root].add(p)
    
    perims = {k:sum(4 - matching_neigbors(p) for p in v) for k,v in areas.items()}
    sides = {k:count_sides(k, v) for k,v in areas.items()}

    prices1 = []
    for k,v in areas.items():
        prices1.append(len(v) * perims[k])
        #print (f'A region of {grid[k]} plants with price {len(v)} * {perims[k]} = {prices1[-1]}.')

    print (f'Part 1: {sum(prices1)}')

    prices2 = []
    for k,v in areas.items():
        prices2.append(len(v) * sides[k])
        #print (f'A region of {grid[k]} plants with price {len(v)} * {sides[k]} = {prices2[-1]}.')

    print (f'Part 2: {sum(prices2)}')    


if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
