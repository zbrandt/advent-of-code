""" Module for Advent of Code Day 6.
    https://adventofcode.com/2015/day/6
"""
import sys
import re
from rich import print # pylint: disable=redefined-builtin
from rich.progress import track

# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring

dfun = {'turn on'   : (1, 1),
        'turn off'  : (1, 0),
        'toggle'    : (0, 0)}

def do_rule (rule, x, y, val, part) -> bool:
    if x >= rule[1][0] and x <= rule[2][0] and y >= rule[1][1] and y <= rule[2][1]:
        if part == 1:
            if rule[0][0]:
                val = rule[0][1]
            else:
                val = val ^ 1
        else:
            if rule[0][0]:
                val = max(0, val + (2 * rule[0][1])-1)
            else:
                val += 2
    return val

def do_rules (rules, x, y, part) -> bool:
    val = 0
    for r in rules:
        val = do_rule(r, x, y, val, part)
    return val

def main(fname):
    rules = [(dfun[op], (int(xy[0]),int(xy[1])), (int(xy[2]),int(xy[3]))) for op, *xy in re.findall(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)',fname.read())]

    for part in [1,2]:
        lights = sum(do_rules(rules, x, y, part) for x in track(range(1000)) for y in range(1000))
        print (f'Part {part}: {lights}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
