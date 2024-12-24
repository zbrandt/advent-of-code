""" Module for Advent of Code Day 19.
    https://adventofcode.com/2024/day/19
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, method-cache-max-size-none
import sys
from functools import cache

def cmp(full, pre) -> bool:
    #print (f'cmp({full}, {pre:4}) = {full[:len(pre)] == pre}')
    return full[:len(pre)] == pre

class LinenLayout:
    def __init__(self):
        self.targets = []
        self.designs = []
        self.maxd = 0

    def read(self, fname):
        self.designs = [x.strip() for x in fname.readline().strip().split(',')]
        self.designs = set(sorted(self.designs, key=lambda x: f'{len(x):03d}' + x, reverse=True))
        fname.readline()
        self.targets = [t for t in fname.read().strip().split('\n')]
        self.maxd = max([len(t) for t in self.designs])
        print (f'{len(self.designs)} designs. Max length {self.maxd}')

    @cache
    def solve_v(self, target, depth=0, pre='') -> int:
        if not target:
            print (f'{' '*depth}solve_v({pre}+{target}, {depth}) ==> 1 Design')
            return 1
        print (f'{' '*depth}solve_v({pre}+{target}, {depth})')
        x = [self.solve_v(target[dlen+1:],depth+1,pre+target[:dlen+1]) for dlen in range(min(len(target), self.maxd)) if target[:dlen+1] in self.designs]
        y = [target[dlen+1:]                                           for dlen in range(min(len(target), self.maxd)) if target[:dlen+1] in self.designs]
        print (f'{' '*depth}solve_v({pre}+{target}, {depth}) ==> {sum(x)=} ==> {list(zip(y,x))}')
        return sum(x)

    @cache
    def solve_q(self, target) -> int:
        if not target:
            return 1
        return sum([self.solve_q(target[dlen+1:]) for dlen in range(min(len(target), self.maxd)) if target[:dlen+1] in self.designs])

    def solve_target(self, target, verbose=False) -> int:
        if verbose:
            return self.solve_v(target)
        else:
            return self.solve_q(target)

def main(fname):
    ll = LinenLayout()
    ll.read(fname)

    possible = []
    for i,t in enumerate(ll.targets):
        possible.append(ll.solve_target(t, False))
        #print (f'{i}/{len(ll.targets)} --> {possible[-1]:14d}  {t}')

    print (f'Part 1: {sum([p>0 for p in possible])}')
    print (f'Part 2: {sum(possible)}')


if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
