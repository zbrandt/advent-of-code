""" Module for Advent of Code Day 13.
    https://adventofcode.com/2024/day/13
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

def play_machine(ba, bb, pr, offset=0, verbose=False) -> int:
    pr[0] += offset
    pr[1] += offset

    noma = bb[1] * pr[0] - bb[0] * pr[1]
    nomb = ba[0] * pr[1] - ba[1] * pr[0]
    denom = ba[0] * bb[1] - ba[1] * bb[0]

    aq,ar = divmod(noma, denom)
    bq,br = divmod(nomb, denom)

    cost = (0, 3*aq + bq)[ar == 0 and br == 0]

    if verbose:
        print (f'Button A: X{ba[0]}, Y{ba[1]}')
        print (f'Button B: X{bb[0]}, Y{bb[1]}')
        print (f'Prize: X={pr[0]}, Y={pr[1]}')
        print (f'A={aq},{ar} B={bq},{br}  {('PRIZE','FAIL')[not cost]}  {cost=}\n')
    return cost

def main(fname) -> None:
    spend1 = 0
    spend2 = 0
    while True:
        try:
            ba, bb, prize = [fname.readline() for _ in range(3)]
            ba = list(map(int, re.match(r'Button \w: X([^,]+), Y(.+)', ba).groups()))
            bb = list(map(int, re.match(r'Button \w: X([^,]+), Y(.+)', bb).groups()))
            prize = list(map(int, re.match(r'Prize: X=([^,]+), Y=(.+)', prize).groups()))
            spend1 += play_machine(ba, bb, prize)
            spend2 += play_machine(ba, bb, prize, offset=10000000000000)
            fname.readline()
        except AttributeError:
            break
    print (f'Part 1: {spend1}')
    print (f'Part 2: {spend2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
