""" Module for Advent of Code Day 19.
    https://adventofcode.com/2015/day/19
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from functools import cache


# This answer per askalski
# https://www.reddit.com/r/adventofcode/comments/3xflz8/comment/cy4etju/
def smart_solve(molecule:str):
    elements = len(re.findall(r'([A-Z])', molecule))
    cnt_Rn = molecule.count('Rn')
    cnt_Y = molecule.count('Y')
    cnt_Ar = molecule.count('Ar')
    answer = elements - cnt_Rn - cnt_Ar - 2*cnt_Y - 1
    print (f'molecule: {elements} - {cnt_Rn} - {cnt_Ar} - 2 * {cnt_Y} - 1 = {elements - cnt_Rn - cnt_Ar - 2*cnt_Y - 1}')
    print (f'Part 2: {answer}')

@cache
def stepdown(molecule, steps=0) -> set[int]:
    global SHRINK
    
    shrink = SHRINK
    #print (f'{steps:3d} {' ' * steps}stepdown({molecule}, {steps})')
    if molecule == 'e':
        print (f'{steps:3d} {' ' * steps}stepdown: FINISH')
        input()
        return set([steps])
    solns = set()
    nmols = set()
    for k,v in shrink.items():
        if v == 'e' and molecule != k:
            continue
        for m in re.finditer(k, molecule):
            result = molecule[:m.start()] + v + molecule[m.end():]
            nmols.add(result)
            break
    print (f'{steps:3d} {' ' * steps}{len(nmols)} next molecules {nmols}')
    for nm in nmols:
        solns = solns | stepdown(nm, steps+1)
    if len(solns) > 0:
        #print (f'{steps:3d} {' ' * steps}stepdown: {solns=}')
        pass
    return solns

def main(fname):
    global SHRINK

    brute_force = False
    data = fname.read()
    grow = [(k,v) for k,v in re.findall(r'(?m)^(\S+) => (\S+)$', data)]
    SHRINK = {k:v for v,k in re.findall(r'(?m)^(\S+) => (\S+)$', data)}
    target = re.findall(r'\n\n(\S+)', data)[0]

    results = set()
    for k,v in grow:
        for m in re.finditer(k, target):
            res = target[:m.start()] + v + target[m.end():]
            results.add(res)
    print (f'Part 1: {len(results)}')

    smart_solve(target)

    if brute_force:
        solns = stepdown(target)
        print (f'{solns=}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
