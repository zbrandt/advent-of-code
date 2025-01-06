""" Module for Advent of Code Day 7.
    https://adventofcode.com/2016/day/7
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re
"""
([a-z]?=[a-z]{3})(?!\1)\2\1
"""
def main(fname):
    lines_raw = fname.read().strip().split('\n')
    lines = [re.sub(r'\[\w+\]','X',line) for line in lines_raw]

    #print (lines)
    for i,line in enumerate(lines):
        m = re.search(r'(([a-z])(?!\2)([a-z])\3\2)', line)
        if m:
            m = m.group(0)
        #print (f'{lines_raw[i]} ==> {m}')

    codes = [re.search(r'(([a-z])(?!\2)([a-z])\3\2)', line) is not None for line in lines]
    print (codes)
    print (f'Part 1: {sum(codes)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)