""" Module for Advent of Code Day 1.
    https://adventofcode.com/2025/day/1
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys

def main(fname):
    turns = [(int(turn[0] == 'R')*2-1) * int(turn[1:]) for turn in fname.read().split()]
    p1 = p2 = 0
    pos = 50
    for turn in turns:
        newpos = pos + turn
        p1 += int(newpos % 100 == 0)
        p2 += (pos < 0 and newpos > 0) + (pos > 0 and newpos < 0) + (abs(abs(newpos)-1) // 100)
        pos = newpos % 100
    p2 += p1
    print (f'Part 1: {p1}')
    print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)