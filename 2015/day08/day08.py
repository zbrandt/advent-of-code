""" Module for Advent of Code Day 8.
    https://adventofcode.com/2015/day/8
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import ast

def escaped(s:str) -> str:
    return '"' + s.translate(str.maketrans({ "\"":  r"\"", "\\": r"\\" })) + '"'

def main(fname):
    lines = fname.read().strip().split('\n')

    print (f'Part 1: {sum(len(line) - len(ast.literal_eval(line)) for line in lines)}')
    print (f'Part 2: {sum(len(escaped(line)) - len(line) for line in lines)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
