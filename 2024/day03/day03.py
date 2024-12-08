""" Module for Advent of Code Day 3.
    https://adventofcode.com/2024/day/3
"""
# pylint: disable=line-too-long, missing-function-docstring
import sys
import re

def main(fname):
    enabled = True
    total1 = total2 = 0
    for a, b, do, dont in re.findall(r"mul\((\d+)\,(\d+)\)|(do\(\))|(don't\(\))", fname.read()):
        if do or dont:
            enabled = not dont
        else:
            x = int(a) * int(b)
            total1 += x
            total2 += x * enabled
    print (f'Part 1: {total1}')
    print (f'Part 2: {total2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)