""" Module for Advent of Code Day 13.
    https://adventofcode.com/2015/day/13
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from itertools import permutations
from collections import defaultdict

def main(fname):

    data = fname.read().strip()
    happiness = defaultdict(int, {(name, neigh): (-1,1)[gl == 'gain'] * int(amt) for name, gl, amt, neigh in re.findall(r'(?m)^(\w+) would (gain|lose) (\d+) .* (\w+)\.', data)})
    names = set(k[0] for k in happiness)

    for i in range(2):
        scores = {sum(happiness[name,seating[(i+1) % len(seating)]] + happiness[seating[(i+1) % len(seating)], name] for i,name in enumerate(seating)):seating for seating in permutations(names)}
        print (f'Part {i+1}: {max(scores)}, {scores[max(scores)]}')
        names.add('me')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
