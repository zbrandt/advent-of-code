""" Module for Advent of Code Day 18.
    https://adventofcode.com/2015/day/18
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from io import StringIO
import numpy as np

def ppgrid(grid: np.ndarray) -> None:
    w, h = grid.shape
    print ('\n'.join(''.join(('.','#')[grid[y, x]] for x in range(1,w-1)) for y in range(1,h-1)), '\n' + '=' * (w-2))

def set_corners(grid: np.ndarray, on = True):
    if on:
        w, h = grid.shape
        grid[  1,  1] = 1
        grid[w-2,  1] = 1
        grid[  1,h-2] = 1
        grid[w-2,h-2] = 1

def epoch(grid: np.ndarray, corners) -> np.ndarray:
    ngrid = np.zeros(grid.shape, dtype=int)
    w, h = grid.shape
    for x in range(1,w-1):
        for y in range(1,h-1):
            light = grid[x, y]
            nearby = grid[x-1:x+2 , y-1:y+2]
            ngrid[x, y] = np.sum(nearby) == 3 or (np.sum(nearby) == 4 and light)
    set_corners(ngrid, corners)
    return ngrid

def main(fname):
    ogrid = np.pad(np.loadtxt(StringIO(fname.read().strip().replace('.', ' 0').replace('#', ' 1')), dtype=int), 1)

    grids = []
    for part in range(2):
        grid = ogrid.copy()
        set_corners(grid, part)
        for _ in range (100):
            ppgrid (grid)
            grid = epoch(grid, part)
        grids.append(grid)

    for part in range(2):
        print (f'Part {part+1}: {np.sum(grids[part])}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
