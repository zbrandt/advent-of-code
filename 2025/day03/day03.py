""" Module for Advent of Code Day 1.
    https://adventofcode.com/2025/day/3
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys

def maxify(nums, mxs, pos):
    mxs.append(0)
    nmx = []
    mx = 0
    for i,n in reversed(list(enumerate(nums))):
        mx = max(mx, n * (10 ** pos) + mxs[i+1])
        nmx = [mx] + nmx
    return nums[:-1], nmx

def main(fname):
    lights = list(map(lambda x : list(map(int, list(x))), fname.read().split()))
    
    j1 = j2 = 0
    for l in lights:
        nmx = [0] * len(l)
        for i in range(12):
            j1 += max(nmx) * int(i == 2)
            l, nmx = maxify(l, nmx, i)

        j2 += max(nmx)

    print (f'Part 1: {j1}')
    print (f'Part 2: {j2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)