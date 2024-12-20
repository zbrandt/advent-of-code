""" Module for Advent of Code Day 4.
    https://adventofcode.com/2015/day/4
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from hashlib import md5

def md5_search(code, match) -> int:
    number = 0
    md5_digest = ""
    while md5_digest[:len(match)] != match:
        number += 1
        md5_digest = md5((code+str(number)).encode("ascii")).hexdigest()
    return number

def main(fname):
    code = fname.read().strip()
    for part in [1,2]:
        print (f'Part {part}: {md5_search(code, '0'*(4+part))}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
