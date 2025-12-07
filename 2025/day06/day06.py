""" Module for Advent of Code Day 6.
    https://adventofcode.com/2025/day/6
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
from io import StringIO
import sys
import numpy as np

def main(fname):
    p1 = p2 = 0
    data = fname.read()
    lines = [x for x in data.split('\n') if x]
    nums = np.array([list(map(int,x.split())) for x in lines if x.strip()[0].isdigit()]).T
    ops = [x.split() for x in lines if not x.strip()[0].isdigit()][0]
    probs = np.array([prob.sum() if op == '+' else prob.prod() for prob, op in zip(list(nums), ops)])

    (rows, cols) = nums.T.shape
    colw = [len(str(nums[i].max(0)))+1 for i in range(cols)]
    cgrid = np.genfromtxt(StringIO(data), dtype='U1', delimiter=1)
    p2 = 0
    col = 0
    for i, op in enumerate(ops):
        prob = cgrid[0:rows, col:col+colw[i]].T
        prob = np.array([int(x) for x in [''.join(row).strip() for row in prob] if x])
        ans = prob.sum() if op == '+' else prob.prod()
        p2 += ans
        col += colw[i]
        #print (f'{i=} {op=} {prob=} {int(ans)=}')

    p1 = probs.sum()
    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
