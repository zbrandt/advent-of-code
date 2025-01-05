""" Module for Advent of Code Day 3.
    https://adventofcode.com/2016/day/3
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import numpy as np

def main(fname):
    triplets = np.loadtxt(fname, dtype=int)
    triplets_t = np.concatenate([triplets[3*i:3*i+3].T for i in range(triplets.shape[0]//3)])

    for i, sides in enumerate([triplets, triplets_t]):
        triangles = [(a,b,c) for a,b,c in sides if all([a<b+c, b<a+c, c<a+b])]
        print (f'Part {i+1}: {len(triangles)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
