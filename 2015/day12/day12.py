""" Module for Advent of Code Day 12.
    https://adventofcode.com/2015/day/12
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import json


def get_nums(jdata, no_red = False) -> list[int]:
    if isinstance(jdata, list):
        out = []
        for elem in jdata:
            out.extend(get_nums(elem, no_red))
        return out
    if isinstance(jdata, dict):
        out = []
        for k,v in jdata.items():
            if isinstance(k, int):
                out.append(k)
            if no_red and v == 'red':
                return []
            out.extend(get_nums(v, no_red))
        return out
    if isinstance(jdata, int):
        return [jdata]
    return []

def main(fname):

    data = fname.read().strip()

    jdata = json.loads(data)
    for i in range(2):
        print (f'Part {i+1}: {sum(get_nums(jdata, i == 1))}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
