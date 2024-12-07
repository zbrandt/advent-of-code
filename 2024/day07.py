""" Module for Advent of Code Day 7.
    https://adventofcode.com/2024/day/7
"""
import sys
from operator import add, mul

def cat(x,y):
    return int(str(x) + str(y))

def solve(target, numbers, ops, running = 0, op = add) -> int:
    running = op(running, numbers[0])
    if running > target:
        return []
    if len(numbers) == 1:
        return [running]
    return sum([solve(target, numbers[1:], ops, running, op) for op in ops],[])

def main(fname):
    lines = fname.read().strip().split('\n')
    targets = {}
    for l in lines:
        s1, _, s2 = l.partition(':')
        target, numbers = int(s1), list(map(int,s2.split()))
        targets[target] = numbers

    sum1 = [k*int(k in solve(k, v, (add, mul))) for k,v in targets.items()]
    sum2 = [k*int(k in solve(k, v, (add, mul, cat))) for k,v in targets.items()]

    print (f'Part 1: {sum(sum1)}')
    print (f'Part 2: {sum(sum2)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
