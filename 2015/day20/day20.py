""" Module for Advent of Code Day 20.
    https://adventofcode.com/2015/day/20
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring

def brute(target, gifts, max_visits=None):
    tgt = target // 10
    max_visits = (max_visits,target)[max_visits is None]
    houses = [0] * tgt
    for i in range(1, tgt):
        for j in range(i, min(tgt, i*max_visits+1), i):
            houses[j] += i * gifts
    return min(h for h,p in enumerate(houses) if p >= target)

def main():
    target = 33_100_000

    for i, params in enumerate([(10, None), (11, 50)]):
        print (f'Part {i+1}: {brute(target, *params)}')

if __name__ == "__main__":
    main()
