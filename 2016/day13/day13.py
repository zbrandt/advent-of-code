""" Module for Advent of Code Day 13.
    https://adventofcode.com/2016/day/13
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import string
import re
from collections import deque

def main(fname):

    grid:dict[complex,int] = {}

    def onoff(pos:complex, fav:int) -> int:
        bc = 1
        x,y = int(pos.real), int(pos.imag)
        if x >= 0 and y >= 0:
            val = x*x + 3*x + 2*x*y + y + y*y
            val += fav
            bc = val.bit_count()
            grid[pos] = bc & 1
        return bc & 1

    def pp(grid:dict[complex, int], path:list[complex]):
        xmax = max(int(p.real) for p in grid)+1
        ymax = max(int(p.imag) for p in grid)+1
        disp = ['   ' + string.digits * (xmax // 10) + string.digits[:xmax % 10]]
        for y in range(ymax):
            line = f'{y:2} '
            for x in range(xmax):
                pos = x+y*1j
                ch = ('.','O')[pos in path]
                line += (ch,'#')[grid[pos]] if pos in grid else ' '
            disp.append(line)
        return disp

    def execute(fav, end, maxdist):
        print (f'Execute: Favorite: {fav}, End: ({int(end.real)},{int(end.imag)}), Max: {maxdist}')
        pos = 1+1j
        dirs = [-1j**i for i in range(4)]
        path:list[complex] = []
        visited:set[complex] = set()
        d:deque[list[complex]] = deque([[pos]])
        while d:
            path = d.popleft()
            pos = path[-1]
            if pos in visited or onoff(pos, fav) or (maxdist is not None and len(path) > maxdist+1):
                continue
            visited.add(pos)
            if pos == end:
                print (f'Made it to ({int(pos.real)},{int(pos.imag)})')
                break
            for dxy in dirs:
                d.append(path + [pos+dxy])

        print('\n'.join(pp(grid, path if maxdist is None else list(visited))))
        return len(path)-1 if maxdist is None else len(visited)

    params = list(map(int,re.findall(r'(\d+)', fname.read())))
    fav = params[0]
    end = complex(params[1], params[2])

    grid = {}
    print(f'Part 1: {execute(fav, end, None)}')
    grid = {}
    print(f'Part 2: {execute(fav, -1+-1j, 50)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
