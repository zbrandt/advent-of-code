""" Module for Advent of Code Day 19.
    https://adventofcode.com/2024/day/19
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import functools
from collections import deque
from copy import copy

def cmp(full, pre) -> bool:
    #print (f'cmp({full}, {pre:4}) = {full[:len(pre)] == pre}')
    return full[:len(pre)] == pre

class LinenLayout:
    def __init__(self):
        self.targets = []
        self.designs = []
        self.redundants = {}
        self.maxred = 0
        self.current_target = None
        self.current_comps = set()
    
    def read(self, fname):
        self.designs = [x.strip() for x in fname.readline().strip().split(',')]
        self.designs = sorted(self.designs, key=lambda x: f'{len(x):03d}' + x, reverse=True)
        print (self.designs)
        fname.readline()
        self.targets = []
        while True:
            target = fname.readline().strip()
            if not target:
                break
            self.targets.append(target)
        print (f'Designs = {len(self.designs)=}')
        #print (f'Designs = {tarself.targetsgets}')

        self.redundants = {}
        if False:
        #if True:
            special = 'xxx'
            for i,d in enumerate(self.designs):
                tmp = d
                self.designs[i] = special+str(i)
                m = self.build_target(d)
                if m:
                    self.redundants[tmp] = m
                else:
                    self.designs[i] = tmp
            self.designs = [d for d in self.designs if not cmp(d, special)]
            self.maxred = max([len(r) for r in self.redundants])
        print (f'{len(self.redundants)=} {self.maxred=} {self.redundants=}')
        print (f'Reduced = {len(self.designs)=}')

    def solve_target(self, target) -> int:
        self.current_target = target
        self.current_comps = set()
        matchlen = self.build_target(target)
        if False:
            for c in self.current_comps:
                self.current_comps = self.current_comps | self.check_redundants(c)
        if False:
            assert matchlen == len(self.current_comps)
            for comp in self.current_comps:
                assert len(self.current_target) == len(''.join(comp))
        print (f'solve_target({target}) ==> {len(self.current_comps)}:')
        return len(self.current_comps)

    @functools.cache
    def enum_designs(self, target) -> set:
        print (f'>> enum_designs({target=})')
        x = set([tuple([target])])
        x = set([tuple([])])
        print (f'  base {x=}')
        if target:
            for d in self.designs:
                if cmp(target, d):
                    print (f'  match{target=}, {d=}')
                    for sd in self.enum_designs(target[len(d):]):
                        t = tuple([d, *sd])
                        print (f'  add {t=}, match {d=}')
                        x.add(t)
            #x = set([(tuple([d]) + sd) for d in self.designs for sd in self.enum_designs(target[len(d):]) if cmp(target, d)])
        print (f'   enum_designs({target=}) == {x=}')
        return x

    def solve_target2(self, target) -> int:
        pos = 0
        prod = 1
        dq = deque([target[pos:pos+8]])
        print (f'solve_target2({dq=})')
        while dq:
            t = dq.popleft()
            designs = self.enum_designs(t)
            print (f'solve_target2: enum_designs({t=}) ==> {len(designs)}:{designs=}')
            return prod
            prod = prod * len(designs)
            for design in designs:
                l = len(design)
                dq.append(target[pos+l:pos+l+8])

        return prod

    def build_target(self, target, comp=[], depth=0) -> int:
        print (f'{depth:03d}{' '*depth}build_target({target=})')
        if not target:
            self.current_comps.add(tuple(comp))
            return 1
        return sum([self.build_target(target[len(d):], comp + [d], depth+1) for d in self.designs if cmp(target,d)])
        
    def check_redundants(self, comp, depth=0, prefix="A") -> set:
        if len(comp) < 2:
            #print (f'{' '*depth}{prefix}:check_redundants {comp=} SHORT')
            return set([comp])
        comps = set([comp])
        for i in range(2,self.maxred+1):  
            for j in range(len(comp)-i+1):
                redcat = ''.join(comp[j:j+i])
                #print (f'{' '*depth}{prefix}:check_redundants {comp=} {i=} {j=} {redcat=}')
                if redcat in self.redundants:
                    #print (f'{' '*depth}{prefix}:found redundant hit: {i=} {j=} {redcat=}')
                    compsl = self.check_redundants(comp[0:j], depth+1, "L")
                    compsr = self.check_redundants(comp[j+i:], depth+1, "R")
                    comps = comps | set([l + tuple([redcat]) + r for l in compsl for r in compsr])
                    #print (f'{' '*depth}{prefix}:compounded comps: {comps=}')
        return comps

def main(fname):
    ll = LinenLayout()
    ll.read(fname)

    possible = []
    for i,t in enumerate(ll.targets):
        match = ll.solve_target2(t)
        print (f'{i}/{len(ll.targets)} --> {match}')
        
        #possible.append(match)
        #print (f'{i}/{len(ll.targets)} --> {possible[-1]} {sum(possible)}')
    print (f'Part 1: {sum([p>0 for p in possible])}')
    print (f'Part 2: {sum(possible)}')


if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
