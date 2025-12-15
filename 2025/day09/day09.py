""" Module for Advent of Code Day 9.
    https://adventofcode.com/2025/day/9
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
from itertools import combinations
from bisect import bisect_left, bisect_right
import sys

def clean_pair_xxx(pair, xreds, yreds):
    minx = min(pair[0][0], pair[1][0])
    miny = min(pair[0][1], pair[1][1])
    maxx = max(pair[0][0], pair[1][0])
    maxy = max(pair[0][1], pair[1][1])
    #print (f'clean_pair ({pair}, min={minx},{miny}, max={maxx},{maxy})')

    corners = [(minx, miny), (minx, maxy), (maxx, miny), (maxx, maxy)]
    ix = bisect_left(xreds, minx, key=lambda t: t[0])
    iy = bisect_left(yreds, miny, key=lambda t: t[1])

    clean = True
    if clean:
        for xr in xreds[ix:]:
            if xr in corners:
                continue
            if xr[0] > maxx:
                break
            if miny < xr[1] < maxy:
                print (f'clean_pair: ({pair}) xr dirty {xr}: {miny} < {xr[1]} < {maxy}')
                clean = False
                break

    if clean:
        for yr in yreds[iy:]:
            if yr in corners:
                continue
            if yr[1] > maxy:
                break
            if minx < yr[0] < maxx:
                clean = False
                print (f'clean_pair: ({pair}) yr dirty {yr}: {minx} < {yr[0]} < {maxx}')
                break

    if clean:
        print (f'clean_pair: ({pair})')
    return clean

def clean_pair(pair, xreds, yreds, xs, ys):
    """
    Return True if the rectangle defined by the two points in `pair`
    contains no other red point (inside the boundary).

    pair: ((x1, y1), (x2, y2))
    xreds: all red points sorted by (x, y)
    yreds: all red points sorted by (y, x)
    xs: list of x-coordinates in the same order as xreds
    ys: list of y-coordinates in the same order as yreds
    """
    (x1, y1), (x2, y2) = pair
    minx, maxx = sorted((x1, x2))
    miny, maxy = sorted((y1, y2))

    # Only the two points in the pair are "allowed" on or in the rectangle.
    #corners = {pair[0], pair[1]}
    corners = [(minx, miny), (minx, maxy), (maxx, miny), (maxx, maxy)]

    # Scan candidates by x-range using xreds.
    ix = bisect_left(xs, minx)
    for k in range(ix, len(xreds)):
        xr = xreds[k]
        if xr[0] > maxx:
            break  # no more points with x in range
        if xr in corners:
            continue
        if minx < xr[0] < maxx and miny < xr[1] < maxy:
            print (f'clean_pair: ({pair}) xr dirty {xr}: {minx} < {xr[0]} < {maxx} && {miny} < {xr[1]} < {maxy}')
            return False

    # Scan candidates by y-range using yreds.
    iy = bisect_right(ys, miny)
    for k in range(iy, len(yreds)):
        yr = yreds[k]
        if yr[1] > maxy:
            break  # no more points with y in range
        if yr in corners:
            continue
        if minx < xr[0] < maxx and miny < xr[1] < maxy:
            print (f'clean_pair: ({pair}) yr dirty {yr}: {minx} < {yr[0]} < {maxx} && {miny} < {yr[1]} < {maxy}')
            return False

    print (f'clean_pair: ({pair})')
    return True

def clean_pair_new(pair, floor):
    minx = min(pair[0][0], pair[1][0])
    miny = min(pair[0][1], pair[1][1])
    maxx = max(pair[0][0], pair[1][0])
    maxy = max(pair[0][1], pair[1][1])
    #print (f'clean_pair ({pair}, min={minx},{miny}, max={maxx},{maxy})')

    clean = True
    for y in range(miny + 1, maxy):
        for x in range(minx + 1, maxx):
            if floor[y][x] == '.':
                #print (f'clean_pair: ({pair}) dirty at {(x,y)}')
                clean = False
                break
        if not clean:
            break

    if clean:
        #print (f'clean_pair: ({pair})')
        pass
    return clean

def main(fname):
    reds = [tuple(map(int,line.split(','))) for line in fname.read().split()]
    areas = [(abs(pair[1][0] - pair[0][0]) + 1) * (abs(pair[1][1] - pair[0][1]) + 1) for pair in combinations(reds,2)]
    #print (f'{reds=}')
    #print (f'{areas=}')

    xreds = sorted(reds, key=lambda x: (x[0], x[1]))
    yreds = sorted(reds, key=lambda x: (x[1], x[0]))
    xs = [p[0] for p in xreds]
    ys = [p[1] for p in yreds]
    print (f'{min(xs)=}, {max(xs)=}, {min(ys)=}, {max(ys)=}')

    width = max(xs) + 4
    height = max(ys) + 2
    floor = [list('.' * width) for _ in range(height)]
    #print (floor)
    #print (f'{'\n'.join(''.join(f) for f in floor)}')

    #input()
    floor[reds[0][1]][reds[0][0]] = '#'
    for i,a in enumerate(reds):
        b = reds[(i+1) % len(reds)]
        c = reds[(i+2) % len(reds)]
        if a[0] == b[0]:
            for y in range(min(a[1], b[1]) + 1, max(a[1], b[1])):
                floor[y][a[0]] = '|'
            if (a[1] < b[1]):
                floor[b[1]][b[0]] = ('J','L')[b[0] < c[0]]
            else:
                floor[b[1]][b[0]] = ('7','F')[b[0] < c[0]]
        else:
            for x in range(min(a[0], b[0]) + 1, max(a[0], b[0])):
                floor[a[1]][x] = '-'
            if (a[0] < b[0]):
                floor[b[1]][b[0]] = ('J','7')[b[1] < c[1]]
            else:
                floor[b[1]][b[0]] = ('L','F')[b[1] < c[1]]
    #print (f'{'\n'.join(''.join(f) for f in floor)}')
    #input()

    print (f'fill the insides')
    for i, row in enumerate(floor):
        #input()
        inside = False
        for j, cell in enumerate(row[:-1]):
            if inside and cell == '.':
                row[j] = 'X'            
            if cell == '|' or (cell == 'J' and turn == 'F') or (cell == '7' and turn == 'L'):
                inside = not inside
                #print (f'{"X:Entering" if inside else "X:Exiting"} at {(j,i)}')
            elif cell == 'F' or cell == 'L':
                turn = cell
        #print (f'{'\n'.join(''.join(f) for f in floor)}')
    #print (f'{'\n'.join(''.join(f) for f in floor)}')
    #input()

    print (f'restore the edges & corners')
    # restore the edges & corners
    for i, row in enumerate(floor):
        for j, cell in enumerate(row):
            if cell in ['F','L','J','7']:
                row[j] = '#'
            elif cell in ['-','|']:
                row[j] = 'X'
    #print (f'{'\n'.join(''.join(f) for f in floor)}')
    #input()

    print (f'find clean pairs')
    #print (f'{xreds=}')
    #print (f'{yreds=}')
    if False:
        if True:
            cleans = [clean_pair(pair, xreds, yreds, xs, ys) for pair in combinations(reds,2)]
        else:
            cleans = [clean_pair_xxx(pair, xreds, yreds) for pair in combinations(reds,2)]
    else:
        cleans = [clean_pair_new(pair, floor) for pair in combinations(reds,2)]

    p1 = max(areas)
    p2 = max(a for a,c in zip(areas, cleans) if c)

    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
