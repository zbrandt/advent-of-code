""" Module for Advent of Code Day 11.
    https://adventofcode.com/2024/day/11
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import Counter
from math import log10

class PlutonianPebbles:
    def __init__(self, s:str):
        self.stones = Counter(list(map(int, s.split())))

    def blink(self) -> None:
        stones = Counter()
        for n, cnt in self.stones.items():
            if n == 0:
                stones[1] += cnt
            else:
                d = int(log10(n)+1)
                if d & 1 == 0:
                    a, b = divmod(n,10**(d//2))
                    stones[a] += cnt
                    stones[b] += cnt
                else:
                    stones[n * 2024] += cnt
        self.stones = stones

    def total(self) -> int:
        return self.stones.total()

def main(fname) -> None:
    pp = PlutonianPebbles(fname.read())
    for i, count in enumerate([25,50]):
        for _ in range(count):
            pp.blink()
        print (f'Part {i+1}: {pp.total()}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
