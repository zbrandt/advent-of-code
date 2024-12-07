""" Module for Advent of Code Day 7.
    https://adventofcode.com/2024/day/7
"""
# pylint: disable=line-too-long, missing-function-docstring
import sys
import re
from operator import add, mul
from itertools import chain

def cat(x:int, y:int) -> int:
    return int(str(x) + str(y))

def compute(target, numbers, ops, running = 0, op = add) -> list[int]:
    running = op(running, numbers[0])
    if running > target:
        return []
    if len(numbers) == 1:
        return [running]
    return chain(*[compute(target, numbers[1:], ops, running, op) for op in ops])

def main(fname) -> None:
    targets = {int(k) : list(map(int, v.split())) for k,v in re.findall(r'(\d+)\s*:\s*(\d.*)', fname.read())}

    sum1 = [k*int(k in compute(k, v, (add, mul))) for k,v in targets.items()]
    sum2 = [k*int(k in compute(k, v, (add, mul, cat))) for k,v in targets.items()]

    print (f'Part 1: {sum(sum1)}')
    print (f'Part 2: {sum(sum2)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
