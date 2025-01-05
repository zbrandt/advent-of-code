""" Module for Advent of Code Day 5.
    https://adventofcode.com/2016/day/5
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import hashlib

def interesting(door, idx, pwd = None):
    inpx = door + str(idx)
    result = hashlib.md5(inpx.encode("utf-8")).hexdigest()
    #print (f'interesting({idx, pwd} -> {result[0:5]} + {result[5]} + {result[6]})')
    if pwd:
        pos = ord(result[5]) - ord('0')
        return ((pwd[0], 0),(result[6], pos)) [result[:5] == '00000' and pos < len(pwd) and pwd[pos % len(pwd)] == ' ']
    return ('', result[5]) [result[:5] == '00000']

def main(fname):
    pwdlen = 8
    inp = fname.read().strip()

    idx = 0
    pwd = ''
    while len(pwd) < pwdlen:
        pwd += interesting(inp, idx)
        idx += 1
        print (f'{idx:8}: {pwd=}', end='\r')
    print (' ' * 40, end='\r')
    print (f'Part 1: {pwd}')

    idx = 0
    pwd = list(' ' * pwdlen)
    while ' ' in pwd:
        ch, pos = interesting(inp, idx, pwd)
        pwd[pos] = ch
        idx += 1
        print (f'{idx:8}: pwd="{''.join(pwd)}"', end='\r')
    print (' ' * 40, end='\r')
    print (f'Part 2: {''.join(pwd)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
