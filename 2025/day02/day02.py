""" Module for Advent of Code Day 2.
    https://adventofcode.com/2025/day/2
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys

def factors(n):
    return set(
        x for tup in ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0) for x in tup
    ) - {1}

def is_invalid_n(id, n) -> bool:
    (chunk, rem) = divmod(len(id), n)
    return rem == 0 and id[:chunk] * n == id

def is_invalid_any(id) -> bool:
    return (any([is_invalid_n(id, n) for n in factors(len(id))]))    

def main(fname):
    p1 = p2 = 0
    gift_ids = [list(map(int,x.strip().split('-'))) for x in fname.read().split(',')]
    for gid in gift_ids:
        for i in range(gid[0], gid[1] + 1):
            if is_invalid_n(str(i), 2):
                p1 += i
            if is_invalid_any(str(i)):
                p2 += i

    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
