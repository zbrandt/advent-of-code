""" Module for Advent of Code Day 9.
    https://adventofcode.com/2015/day/9
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from itertools import permutations

def main(fname):

    def travel (cities):
        return sum(edges[city,cities[i+1]] for i,city in enumerate(cities[:-1]))

    data = fname.read().strip()
    edges = {k:int(v) for a,b,d in re.findall(r'(\w+) to (\w+) = (\d+)', data) for k,v in {(a,b):d, (b,a):d}.items()}
    cities = set(k[0] for k in edges)

    routes = { travel(cl):cl for cl in list(permutations(cities)) }

    print (f'Part 1: {min(routes)} {routes[min(routes)]}')
    print (f'Part 1: {max(routes)} {routes[max(routes)]}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
