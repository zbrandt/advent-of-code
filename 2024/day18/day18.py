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

def ppram(w, h, ram):
    x = '\n'.join(''.join(ram[(x,y)] for x in range(w)) for y in range(h))

    if 'rich' in sys.modules:
        drich = {'.': ' ',
                '#': '[bold]#[/]',
                'o': '[bold bright_green]O[/]'
                }
        rep = dict((re.escape(k), v) for k, v in drich.items())
        pattern = re.compile("|".join(rep.keys()))
        x = pattern.sub(lambda m: rep[re.escape(m.group(0))], x)

    print (f'Ram {w}x{h}\n{x}')

def tadd (a,b):
    return (a[0]+b[0], a[1]+b[1])

def test_ram(w, h, ram, b, drop, show=False) -> bool:

    ram = defaultdict(lambda : '#')
    for x in range(w):
        for y in range(h):
            ram[(x,y)] = '.'

    for xy in b[:drop]:
        ram[xy] = '#'
    if show:
        ppram(w,h,ram)
        print ('-' * w)

    dirs = ((-1,0), (0,-1), (0,1), (1,0))

    pstart = (0,0)
    pexit = (w-1,h-1)
    seen = set()
    d = deque([(pstart,0,[])])
    while d:
        (p, steps, path) = d.popleft()
        #print (f'consider {(p,steps)}')
        if p not in seen:
            seen.add(p)
            path.append(p)
            if p == pexit:
                if show:
                    for pxy in path:
                        ram[pxy] = 'o'
                    ppram(w,h,ram)
                return steps
            adj = [(nxy,steps+1,copy(path)) for dxy in dirs for nxy in [tadd(p, dxy)] if nxy not in seen and ram[nxy] != '#']
            #print (f'{adj=}')
            d.extend(adj)
    return 0


def main(fname):
    data = fname.read().strip()
    lines = data.split('\n')
    bytes = [tuple(map(int,line.split(','))) for line in lines]
    w,h = max(xy[0] for xy in bytes)+1, max(xy[1] for xy in bytes)+1
    ram = defaultdict(lambda : '#')
    for x in range(w):
        for y in range(h):
            ram[(x,y)] = '.'

    drop = (10,1024)[w>10]
    steps = test_ram(w,h,ram,bytes,drop,True)
    print (f'Part 1: {steps} steps')
    print ('-' * 20)
    
    low,high = 0,len(bytes)
    while low < high:
        mid = (low + high) // 2 + 1
        #print (f'{low} < {mid} < {high}')
        a = test_ram(w,h,ram,bytes,mid+0)
        b = test_ram(w,h,ram,bytes,mid+1)
        #print (f'test{mid+0}={a} test{mid+1}={b}')
        if a and not b:
            test_ram(w,h,ram,bytes,mid+0,True)
            print (f'Part 2: {bytes[mid]=}')
            break
        if not a:
            high = mid-1
        else:
            low = mid
    

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
