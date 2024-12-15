""" Module for Advent of Code Day 14.
    https://adventofcode.com/2024/day/14
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
import operator
from functools import reduce
from blockify import blockify
from time import sleep

import numpy as np
from scipy.stats import entropy

def calc_entropy(pos):
    hist, _, _ = np.histogram2d([x for x,y in pos], [y for x,y in pos], bins=10)
    prob = hist / np.sum(hist)
    return entropy(prob.flatten())

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
    entr = sum_entropy = min_entropy = mean_entropy = calc_entropy(pos)
    posx = pos
    while entr / mean_entropy > 0.8 and steps < w*h :  # look for 20% drop in entropy
        steps += 1
        posx = do_steps(w, h, pos, vel, steps)
        entr = calc_entropy(posx)
        sum_entropy += entr
        mean_entropy = sum_entropy / (steps+1)
        min_entropy = min(min_entropy, entr)
        ppgrid(blockify(gridify(w, h, posx)))
        print (f'{steps=:6d} {entr=:7.4f} mean={mean_entropy:7.4f} min={min_entropy:7.4f}\n')
        if entr / mean_entropy < 0.98:
            sleep(0.1)

    #ppgrid(gridify(w, h, posx))
    #ppgrid(blockify(gridify(w, h, posx)))

    print ('-' * (w//2))
    print (f'Part 1: {factor} safety factor')
    print (f'Part 2: {steps} steps to Christmas')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
