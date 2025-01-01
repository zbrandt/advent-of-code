""" Module for Advent of Code Day 16.
    https://adventofcode.com/2015/day/16
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from operator import __eq__, __gt__, __lt__

raw_wrapping = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""
wrapping = {a:int(c) for a,b,c in [feature.partition(':') for feature in raw_wrapping.strip().split('\n')]}

op1 = {k :__eq__ for k in wrapping}
op2 = op1.copy()
op2['cats'] = __lt__
op2['trees'] = __lt__
op2['pomeranians'] = __gt__
op2['trgoldfishees'] = __gt__

def main(fname):

    data = fname.read().strip()
    aunts = {int(n): {k:int(v) for k,v in re.findall(r'(\w+):\s(\d+)', attrs)} for n, attrs in re.findall(r'(?m)^Sue (\d+):\s+(.*)\s*$',data)}
    for i, op in enumerate([op1, op2]):
        matches = [k for k, attrs in aunts.items() if all([op[k](wrapping[k], v) for k,v in attrs.items()])]
        print (f'Part {i+1}: {matches[0]}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
