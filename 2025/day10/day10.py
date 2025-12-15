""" Module for Advent of Code Day 10.
    https://adventofcode.com/2025/day/10
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
from ast import literal_eval
import sys
from collections import deque, Counter
from itertools import combinations
from functools import reduce
import operator

def read_pattern(s) -> int:
    #print ([1 << i * int(c == '#') for i,c in enumerate(s)])
    return sum((1 << i) * (c == '#') for i,c in enumerate(s))

def read_toggle(s) -> int:
    return [sum(1 << n for n in t) for t in [literal_eval('{'+t[1:-1]+'}') for t in s]]

def main(fname):
    lines = fname.readlines()
    data = [(read_pattern(a[1:-1]), read_toggle(list(b)), c) for a, *b, c in [line.split() for line in lines]]

    p1 = p2 = 0
    for line in data:
        print (f'line: {line}')
        for n in range(len(line[1])):
            combs = list(combinations(line[1],n+1))
            match = [int(reduce(operator.xor,c) == line[0]) for c in combs]
            if any(match):
                print (f'presses={n+1}, match={[x[0] for x in zip(combs, match) if x[1]]}')
                break
        p1 += n + 1
    
    print ('-' * 30)
    machines = [([Counter(literal_eval('{'+x[1:-1]+'}')) for x in b],Counter({k:v for k,v in enumerate(literal_eval('['+c[1:-1]+']'))})) for a, *b, c in [line.split() for line in lines]]

    for m in machines:
        dist_cache = {0:0}
        target = m[1]
        while 
        for p in m[0]
        

        presses = find_dist(m[0], px) for px in m[1])
    
    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
