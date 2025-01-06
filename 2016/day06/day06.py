""" Module for Advent of Code Day 6.
    https://adventofcode.com/2016/day/6
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
from collections import Counter
import numpy as np

def main(fname):
    msgs = np.array([np.array(list(m.strip())) for m in fname])
    most = ''.join([str(Counter(col).most_common()[0][0]) for col in msgs.T])
    least = ''.join([str(Counter(col).most_common()[-1][0]) for col in msgs.T])
    print (f'Part 1: {most}')
    print (f'Part 2: {least}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)