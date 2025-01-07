""" Module for Advent of Code Day 8.
    https://adventofcode.com/2016/day/8
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re
import numpy as np

def main(fname):

    def pp(disp:np.array):
        return '\n'.join(''.join((' ','\u2588')[val] for val in row) for row in disp)

    lines = fname.read().strip().split('\n')
    cmds:list[tuple[re.Match]] = [(re.match(r'rect (\d+)x(\d+)', line), re.match(r'rot.* (x|y)=(\d+) by (\d+)', line)) for line in lines]
    cmds = [((np.s_[:int(rect.group(2)), :int(rect.group(1))] if rect else None), ((np.s_[int(rot.group(2)),:], np.s_[:,int(rot.group(2))])[rot.group(1) == 'x'], int(rot.group(3))) if rot else None) for rect, rot in cmds]
    disp = np.zeros([6, 50], dtype=int) if len(cmds) > 10 else np.zeros([3, 7], dtype=int)

    for rect, rot in cmds:
        if rect:
            disp[rect] = 1
        elif rot:
            disp[rot[0]] = np.roll(disp[rot[0]], rot[1])

    print (f'Part 1: {np.sum(disp)}')
    print (f'Part 2:\n{pp(disp)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
