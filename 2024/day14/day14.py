""" Module for Advent of Code Day 14.
    https://adventofcode.com/2024/day/14
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
import operator
from functools import reduce
from blockify import blockify

def gridify(w, h, pos):
    grid = [[0] * w for y in range(h)]
    for p in pos:
        grid[p[1]][p[0]] += 1
    return grid

def ppgrid(grid):
    print ('\n'.join(''.join(list(map(str,row))).replace('0','.') for row in grid))
    print ('-' * len(grid[0]))

def xmastree(pos):
    return len(pos) == len(set(pos))

def do_steps(w, h, pos, vel, cnt=1):
    return [((p[0] + cnt * v[0]) % w, (p[1] + cnt * v[1]) % h)  for p,v in zip(pos,vel)]
    
def main(fname) -> None:
    nums = re.findall(r'p=([-+]?\d+),([-+]?\d+) v=([-+]?\d+),([-+]?\d+)', fname.read())
    pos = [(int(n[0]),int(n[1])) for n in nums]
    vel = [(int(n[2]),int(n[3])) for n in nums]

    w,h = 11,7
    if len(pos) > 20:
        w,h = 101,103

    # Part 1
    pos100 = do_steps(w, h, pos, vel, 100)
    quad = [0] * 4
    for p in pos100:
        idx = (1<<0 & int(p[0] > w//2)<<0) | (1<<1 & int(p[1] > h//2)<<1)
        quad[idx] += (0,1)[p[0] != w//2 and p[1] != h//2]
    factor = reduce(operator.mul, quad, 1)

    # Part 2
    steps = 0
    posx = pos
    while not xmastree(posx):
        steps += 1
        posx = do_steps(w, h, pos, vel, steps)

    #ppgrid(gridify(w, h, posx))
    ppgrid(blockify(gridify(w, h, posx)))

    print (f'Part 1: {factor}')
    print (f'Part 2: {steps}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
