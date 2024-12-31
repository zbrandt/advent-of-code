""" Module for Advent of Code Day 9.
    https://adventofcode.com/2015/day/9
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
import json


def get_nums(jdata, no_red = False) -> list[int]:
    #print (jdata)
    if isinstance(jdata, list):
        out = []
        for elem in jdata:
            out.extend(get_nums(elem, no_red))
        return out
    elif isinstance(jdata, dict):
        out = []
        for k,v in jdata.items():
            if isinstance(k, int):
                out.append(k)
            if no_red and v == 'red':
                return []
            out.extend(get_nums(v, no_red))
        return out
    elif isinstance(jdata, int):
        return [jdata]
    elif isinstance(jdata, str):
        return []
    else:
        print (f'{jdata=}')
        assert False

def main(fname):

    data = fname.read().strip()
    
    #nums = [int(x) for x in re.findall(r'([-|+]?\d+)',data)]
    #print (f'Part 1: {sum(nums)}')

    jdata = json.loads(data)
    for i in range(2):
        print (f'Part {i+1}: {sum(get_nums(jdata, i == 1))}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
