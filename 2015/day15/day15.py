""" Module for Advent of Code Day 15.
    https://adventofcode.com/2015/day/15
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from itertools import combinations_with_replacement as Cwr
from collections import Counter
import numpy as np

def main(fname):

    data = fname.read().strip()
    ingredients = {name: np.array(list(map(int,quals))) for name, *quals in re.findall(r'(?m)(\S+):'+','.join([r'\s\S+\s(\S+)']*5), data)}
    ingr_mx = np.matrix(list(ingredients.values()))
    mixes = {tuple(x[ing] for ing in list(ingredients)) for x in [Counter(c) for c in Cwr(ingredients, 100)]}
    all_scores = [np.matrix(ingr_mx.T @ np.array(m)).A1 for m in list(mixes)]

    for i in range(2):
        scores = [score[0:4].prod() for score in all_scores if (i == 0 or score[4] == 500) and all(list(map(lambda x: x > 0, score)))]
        print (f'Part {i+1}: {max(scores)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
