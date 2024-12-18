""" Module for Advent of Code Day 15.
    https://adventofcode.com/2024/day/15
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from time import sleep

#from rich import print # pylint: disable=redefined-builtin

def main(fname) -> None:

    dexp = { '#': '##', 'O': '[]', '.': '..', '@': '@.'}
    dirs = { '<':(-1,0), '>':(1,0), '^':(0,-1), 'v':(0,1) }

    def tadd(a:tuple, b:tuple) -> tuple:
        return (a[0]+b[0], a[1]+b[1])

    def tsub(a:tuple, b:tuple) -> tuple:
        return (a[0]-b[0], a[1]-b[1])

    def push_depth(g, p, dxy) -> int:
        def incd(x):
            return x + 1 * bool(x)
        def maxd(x,y):
            return (0,max(x,y))[all([x,y])]

        vert = dxy[1] != 0
        nxt = tadd(p,dxy)
        ch = g[nxt]
        if ch == '[':
            if vert:
                return incd(maxd(push_depth(g, nxt, dxy), push_depth(g, tadd(nxt,(1,0)), dxy)))
            return incd(push_depth(g, nxt, dxy))
        if ch == ']':
            if vert:
                return incd(maxd(push_depth(g, nxt, dxy), push_depth(g, tadd(nxt,(-1,0)), dxy)))
            return incd(push_depth(g, nxt, dxy))
        if ch == 'O':
            return incd(push_depth(g, nxt, dxy))
        if ch == '.':
            return 1
        return 0

    def do_push(g, p, dxy, depth, bot = False):
        if depth >= 1:
            ch = g[p]
            vert = dxy[1] != 0
            nxt = tadd(p,dxy)
            nxtch = g[nxt]
            if nxtch == '[':
                do_push(g, nxt, dxy, depth-1)
                if vert and ch != '[':
                    do_push(g, tadd(nxt,(1,0)), dxy, depth-1, True)
            if nxtch == ']':
                do_push(g, nxt, dxy, depth-1)
                if vert and ch != ']':
                    do_push(g, tadd(nxt,(-1,0)), dxy, depth-1, True)
            if nxtch == '.':
                do_push(g, nxt, dxy, 0)
            if nxtch == 'O':
                do_push(g, nxt, dxy, depth-1)
        if not bot:
            g[p] = g[tsub(p,dxy)]
            g[tsub(p,dxy)] = '.'

    def ppgrid(w, h, grid):
        x = f'{'\n'.join(''.join(grid[(x,y)] for x in range(w)) for y in range(h))}'

        if 'rich' in sys.modules:
            drich = {'.': ' ',
                    '[': '[bold bright_green]\u005D[/]',
                    ']': '[bold bright_green]\u005D[/]',
                    '@': '[bold bright_red]@[/]',
                    '#': '[bold]#[/]',
                    'O': '[bold bright_green]O[/]'
                    }
            rep = dict((re.escape(k), v) for k, v in drich.items())
            pattern = re.compile("|".join(rep.keys()))
            x = pattern.sub(lambda m: rep[re.escape(m.group(0))], x)

        print (x)

    verbose = True

    data = fname.read()
    moves = re.findall(r'([\^v<>])',data)
    grid = {(x,y):ch for y,row in enumerate(re.findall(r'([#\.O@]+)', data)) for x,ch in enumerate(row)}
    gridx = {(2*x+i,y):chx for y,row in enumerate(re.findall(r'([#\.O@]+)', data)) for x,ch in enumerate(row) for i,chx in enumerate(dexp[ch])}
    pos = [k for k,v in grid.items() if v == '@'][0]
    posx = [k for k,v in gridx.items() if v == '@'][0]
    w,h = max(k[0] for k in grid.keys())+1, max(k[1] for k in grid.keys())+1

    grids = (
        (grid, pos, w, h),
        (gridx, posx, w*2, h),
    )

    if verbose:
        ppgrid(w, h, grid)
        ppgrid(w*2, h, gridx)

    for g,p,w,h in grids:
        for j,m in enumerate(moves):
            d = dirs[m]
            dist = push_depth(g, p, d)
            if dist:
                do_push(g, p, d, dist, bot = True)
                p = tadd(p,d)
            if verbose:
                ppgrid(w, h, g)
                print (f'move "{m}" {j:5}/{len(moves):5}')

    boxsum = sum(p[1]*100 + p[0] for p,v in grid.items() if v == 'O')
    boxsum2 = sum(p[1]*100 + p[0] for p,v in gridx.items() if v == '[')
    sleep (0.01)

    print (f'Part 1: {boxsum}')
    print (f'Part 2: {boxsum2}')


if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
