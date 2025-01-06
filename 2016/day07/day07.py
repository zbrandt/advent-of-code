""" Module for Advent of Code Day 7.
    https://adventofcode.com/2016/day/7
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re

def main(fname):
    lines = fname.read().strip().split('\n')
    lines_supernet = [re.sub(r'\[\w+\]','#',line) for line in lines]
    lines_hypernet = ['#'.join(re.findall(r'\[(\w+)\]',line)) for line in lines]

    def match_count(x):
        return len(re.findall(r'(([a-z])(?!\2)([a-z])\3\2)', x))

    def find_xyx(z, swap):
        return {(m[0],re.sub(r'(([a-z])(?!\2)([a-z])\2)',r'\3\2\3', m[0]))[swap] for m in re.findall(r'(?=(([a-z])(?!\2)([a-z])\2))', z)}

    matches = [ tuple(match_count(line[i]) for i in range(2)) for line in zip(lines, lines_supernet) ]
    codes = [ m[1] > 0 and m[1] == m[0] for m in matches]

    ssls = [bool(find_xyx(x[0], 0) & find_xyx(x[1], 1)) for x in zip(lines_supernet, lines_hypernet)]

    print (f'Part 1: {sum(codes)}')
    print (f'Part 2: {sum(ssls)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
