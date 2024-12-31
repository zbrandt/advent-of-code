""" Module for Advent of Code Day 11.
    https://adventofcode.com/2015/day/11
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import re
import string

def base26_encode(n):
    result = ""
    while n > 0:
        n, r = divmod(n, 26)
        result = chr(r + ord('a')) + result
    return result

def base26_decode(s):
    result = 0
    for c in s:
        result = result * 26 + (ord(c) - ord('a'))
    return result

def has_line(s):
    return re.search('|'.join([string.ascii_lowercase[i:i+3] for i in range(26-2)]),s) is not None

def has_noil(s):
    return re.search('o|i|l',s) is None

def has_two_pair(s):
    m = re.search(r'((\w)\2).*((\w)\4)',s)
    return m is not None and m.group(1) != m.group(3)

def inc_passwrd(s):
    return base26_encode(base26_decode(s)+1)

def next_password(x):
    x = inc_passwrd(x)
    while not (has_line(x) and has_noil(x) and has_two_pair(x)):
        x = inc_passwrd(x)
    return x

def main():
    x = "hxbxwxba"
    for i in range(2):
        x = next_password(x)
        print (f'Part {i+1}: {x}')

if __name__ == "__main__":
    main()
