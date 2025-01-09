""" Module for Advent of Code Day 11.
    https://adventofcode.com/2016/day/11
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re
from functools import cache
from collections import deque
from itertools import combinations, chain
from copy import copy
from periodic_table import PeriodicTable

#@cache
def powerset(iterable, limits=(1,2)):
    "Subsequences of the iterable from shortest to longest."
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(limits[0],limits[1]+1))

def main(fname):

    ordinals = ('first', 'second', 'third', 'fourth')

    def safe(floormap):
        result = True
        elems = sorted(list(set ([elem for elem,_ in floormap.keys()])))
        elemmap = {e: (floormap[(e, 'G')], floormap[(e, 'C')]) for e in elems}
        rtg = set([v[0] for k,v in elemmap.items()])
        for k,v in elemmap.items():
            if v[0] != v[1] and v[1] in rtg:
                result = False
                break
        return result

    def all_fours(floormap):
        elems = sorted(list(set ([elem for elem,_ in floormap.keys()])))
        elemmap = {e: (floormap[(e, 'G')], floormap[(e, 'C')]) for e in elems}
        return all([v[0] == 4 and v[1] == 4 for v in elemmap.values()])

    def pp(step, elev, floormap):
        elems = sorted(list(set ([elem for elem,_ in floormap.keys()])))
        print (f'==== Step {step} ====')
        for fl in [4,3,2,1]:
            print (f'F{fl} {(". ","E ")[fl == elev]  }{''.join([(f"{el}"+"G",'.'+' '*len(el))[floormap[(el,'G')] != fl]+' '+(f"{el}"+"M",'.'+' '*len(el))[floormap[(el,'C')] != fl]+'  ' for el in elems])}')


    def elevate_all(floormap, part):
        elev = 1
        step = 0
        visited = {}
        elems = sorted(list(set ([elem for elem,_ in floormap.keys()])))
        elemmap = {e: (floormap[(e, 'G')], floormap[(e, 'C')]) for e in elems}
        print(f'{floormap=}')
        print(f'{elemmap=}')
        d = deque([(step, elev, floormap)])
        while d:
            state = d.popleft()
            (step, elev, floormap) = state
            signature = tuple([elev, tuple(sorted(list(floormap.items())))])
            if signature in visited:
                if step == 777:
                    print ('skipping visited state')
                    pp(*state)
                continue
            visited[signature] = 1
            if all_fours(floormap):
                break
            objs = tuple(list([k for k,v in floormap.items() if v == elev]))
            for elev_nxt in [elev+dz for dz in [1,-1] if 4 >= elev+dz >= 1]:
                for ps in powerset(objs):
                    floormap_next = copy(floormap)
                    for o in ps:
                        floormap_next[o] = elev_nxt
                    if safe(floormap_next):
                        d.append((step+1, elev_nxt, floormap_next))
        print (f'visited {len(visited)} states')
        print (f'Part {part}: {step}')
            
    pt = PeriodicTable()
    lines = re.findall (r'(?m)^The (\w+) floor contains (.*)\.$', fname.read())
    floormap = {}
    for line in lines:
        idx = ordinals.index(line[0]) + 1
        floor = {(pt.lookup(el)[1], eltype[0].upper()):idx for el, eltype in re.findall(r' ([a-z]+)(?=[ -](generator|compatible microchip))', line[1])}
        floormap = floormap | floor

    elevate_all(floormap, 1)

    floormap[('El','G')] = 1
    floormap[('El','C')] = 1
    floormap[('Di','G')] = 1
    floormap[('Di','C')] = 1

    elevate_all(floormap, 2)


if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
