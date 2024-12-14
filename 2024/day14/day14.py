""" Module for Advent of Code Day 14.
    https://adventofcode.com/2024/day/14
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
import operator
from functools import reduce
import blockify

def gridify(robots):
    grid = []
    for y in range(max(p[1] for p,v in robots)):
        grid.append([])
        for x in range(max(p[0] for p,v in robots)):
            bots = sum([p == (x,y) for p,v in robots])
            grid[-1].append(('.',f'{bots}')[bots > 0])
    return grid

def ppgrid(grid):
    print ('\n'.join(''.join(row) for row in grid))
    print ('-' * len(grid[0]))

def xmastree(robots):
    return len(robots) == len(set([p for p,_ in robots]))

def main(fname) -> None:
    factor = 0
    robots = []
    for px, py, vx, vy in re.findall(r'p=([-+]?\d+),([-+]?\d+) v=([-+]?\d+),([-+]?\d+)', fname.read()):
        p = (int(px),int(py))
        v = (int(vx),int(vy))
        robots.append((p,v))

    w,h = 11,7
    if len(robots) > 20:
        w,h = 101,103

    # Part 1
    steps = 100
    final = [(((p[0] + steps * v[0]) % w, (p[1] + steps * v[1]) % h ),v)  for r in robots for p,v in [r]]
    quad = [0] * 4
    for p,v in final:
        idx = (1 & int(p[0] > w//2)<<0) | (1<<1 & int(p[1] > h//2)<<1)
        quad[idx] += (0,1)[p[0] != w//2 and p[1] != h//2]
    factor = reduce(operator.mul, quad, 1)

    steps = 0
    manual = robots
    while True:
        steps += 1
        manual = [(((p[0] + v[0]) % w, (p[1] + v[1]) % h ),v)  for r in manual for p,v in [r]]
        xmas = xmastree(manual)
        if xmas:
            ppgrid(blockify.blockify(gridify(manual), fx=lambda x: x != '.'))
            break

    print (f'Part 1: {factor}')
    print (f'Part 2: {steps}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
