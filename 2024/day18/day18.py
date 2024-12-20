""" Module for Advent of Code Day 18.
    https://adventofcode.com/2024/day/18
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from collections import deque
from collections import defaultdict
from copy import copy
from rich import print # pylint: disable=redefined-builtin

def tadd (a,b):
    return (a[0]+b[0], a[1]+b[1])
class RamRun:
    def __init__(self, data):
        self.bytes = [tuple(map(int,line.split(','))) for line in data.split('\n')]
        self.w = max(xy[0] for xy in self.bytes)+1
        self.h = max(xy[1] for xy in self.bytes)+1

    def pp(self, ram, path):

        if not ram:
            ram = {(x,y):'.' for x in range(self.w) for y in range(self.h)}
        x = '\n'.join(''.join((ram[(x,y)],'o')[(x,y) in path] for x in range(self.w)) for y in range(self.h))

        if 'rich' in sys.modules:
            drich = { '.': ' ', '#': '[bold]#[/]', 'o': '[bold bright_green]O[/]' }
            rep = dict((re.escape(k), v) for k, v in drich.items())
            pattern = re.compile("|".join(rep.keys()))
            x = pattern.sub(lambda m: rep[re.escape(m.group(0))], x)

        print (x)

    def ram_run(self, drop, show=False) -> bool:

        ram = defaultdict(lambda : '#', {(x,y):'.' for x in range(self.w) for y in range(self.h)})
        for xy in self.bytes[:drop]:
            ram[xy] = '#'

        dirs = ((-1,0), (0,-1), (0,1), (1,0))

        pstart = (0,0)
        pexit = (self.w-1, self.h-1)
        seen = set()
        exit_path = []
        d = deque([(pstart, [])])
        while d:
            (p, path) = d.popleft()
            if p not in seen:
                seen.add(p)
                path.append(p)
                if p == pexit:
                    exit_path = path
                    break
                adj = [(nxy, copy(path)) for dxy in dirs for nxy in [tadd(p, dxy)] if nxy not in seen and ram[nxy] != '#']
                d.extend(adj)
        if show:
            self.pp(ram, path)
        return len(exit_path)

def main(fname):
    data = fname.read().strip()
    rr = RamRun(data)

    drop = (10,1024)[rr.w > 10]
    steps = rr.ram_run(drop, True)
    print ('-' * rr.w)

    low,mid,high = 0,0,len(rr.bytes)
    while low < high:
        mid = (low + high) // 2 + 1
        a = rr.ram_run(mid+0)
        b = rr.ram_run(mid+1)
        if a and not b:
            rr.ram_run(mid+0, True)
            break
        if not a:
            high = mid-1
        else:
            low = mid

    print ('=' * rr.w)
    print (f'Part 1: {steps} steps')
    print (f'Part 2: {rr.bytes[mid]}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
