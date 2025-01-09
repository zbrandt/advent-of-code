""" Module for Advent of Code Day 11.
    https://adventofcode.com/2016/day/11
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re
from functools import cache
from collections import deque
from itertools import combinations, chain
from periodic_table import PeriodicTable

def powerset(iterable, limits=(1,2)):
    "Subsequences of the iterable from shortest to longest."
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(limits[0],limits[1]+1))

def deep_tuple(nested_list):
    return tuple(
      deep_tuple(l) if isinstance(l, list)
      else l for l in nested_list
    )

def main(fname):

    ordinals = ('first', 'second', 'third', 'fourth')

    @cache
    def safe(elemset):
        result = True
        rtg = [v[0] for k,v in elemset]
        for k,v in elemset:
            if v[0] != v[1] and v[1] in rtg:
                result = False
                break
        return result

    def all_fours(elemset):
        return all([v[0] == 4 and v[1] == 4 for k,v in elemset])

    def pp(step, elev, elemset):
        elems = sorted(k for k,v in elemset)
        print (f'==== Step {step} ====')
        floormap = {(elem, objtype) : flrs[i] for i, objtype in enumerate(['G', 'M']) for elem, flrs in elemset}
        for fl in [4,3,2,1]:
            print (f'F{fl} {(". ","E ")[fl == elev]  }{''.join([(f"{el}"+"G",'.'+' '*len(el))[floormap[(el,'G')] != fl]+' '+(f"{el}"+"M",'.'+' '*len(el))[floormap[(el,'M')] != fl]+'  ' for el in elems])}')

    def elevate_all(elemset, part):
        elev = 1
        step = 0
        visited = set()
        d = deque([(step, elev, elemset)])
        while d:
            state = d.popleft()
            (step, elev, elemset) = state
            signature = deep_tuple([elev, sorted([v for k,v in elemset])])
            if signature in visited:
                continue
            visited.add(signature)
            if all_fours(elemset):
                pp(*state)
                break
            objs = tuple((k,i) for k,v in elemset for i in [0,1] if v[i] == elev)
            for elev_nxt in [elev+dz for dz in [1,-1] if 4 >= elev+dz >= 1]:
                psl = list(powerset(objs))
                for ps in psl:
                    elemset_next = [[t[0],list(t[1])] for t in elemset]
                    for o in ps:
                        idx = [i for i,e in enumerate (elemset) if e[0] == o[0]][0]
                        elemset_next[idx][1][o[1]] = elev_nxt
                    elemset_next = deep_tuple(elemset_next)
                    if safe(elemset_next):
                        d.append((step+1, elev_nxt, elemset_next))
        print (f'visited {len(visited)} states')
        print (f'Part {part}: {step}')

    pt = PeriodicTable()
    lines = re.findall (r'(?m)^The (\w+) floor contains (.*)\.$', fname.read())
    floormap = {}
    for line in lines:
        idx = ordinals.index(line[0]) + 1
        floor = {(pt.lookup(el)[1], eltype[0].upper()):idx for el, eltype in re.findall(r' ([a-z]+)(?=[ -](generator|compatible microchip))', line[1])}
        floormap = floormap | floor

    elems = sorted(list(set ([elem for elem,_ in floormap.keys()])))
    elemset = tuple([(e, (floormap[(e, 'G')], floormap[(e, 'C')])) for e in elems])
    elevate_all(elemset, 1)

    floormap[('El','G')] = 1
    floormap[('El','C')] = 1
    floormap[('Di','G')] = 1
    floormap[('Di','C')] = 1

    elems = sorted(list(set ([elem for elem,_ in floormap.keys()])))
    elemset = tuple([(e, (floormap[(e, 'G')], floormap[(e, 'C')])) for e in elems])
    elevate_all(elemset, 2)

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
