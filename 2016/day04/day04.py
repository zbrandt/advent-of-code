""" Module for Advent of Code Day 3.
    https://adventofcode.com/2016/day/3
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re
from string import ascii_lowercase
from collections import Counter

def rotx(x):
    return lambda s: str.translate(s, str.maketrans(ascii_lowercase, ascii_lowercase[x%26:] + ascii_lowercase[:x%26]))

def main(fname):
    data = fname.read()
    rooms = [(''.join([p[0] for p in Counter(sorted(name.replace('-',''))).most_common(5)]), int(id), cs) for name, id, cs in re.findall (r'([a-z-]+)(\d+)\[(\w+)\]', data)]
    cyphs = [(rotx(int(id))(name.replace('-', ' ')), int(id)) for name, id, cs in re.findall (r'([a-z-]+)(\d+)\[(\w+)\]', data)]
    idsum = sum(r[1] for r in rooms if r[0] == r[2])
    objects = [c[1] for c in cyphs if 'obj' in c[0]][0]
    print (f'Part 1: {idsum}')
    print (f'Part 2: {objects}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
