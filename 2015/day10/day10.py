""" Module for Advent of Code Day 10.
    https://adventofcode.com/2015/day/10
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import re

def main():

    def look_and_say(s):
        return ''.join([str(len(a))+b for a,b in re.findall(r'((\w)\2*)', s)])

    x = "1113122113"
    for i, cnt in enumerate([40,10]):
        for _ in range(cnt):
            x = look_and_say(x)
        print (f'Part {i+1}: {len(x)}')

if __name__ == "__main__":
    main()
