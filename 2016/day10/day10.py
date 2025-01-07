""" Module for Advent of Code Day 10.
    https://adventofcode.com/2016/day/10
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re

def run_robots(bots, outs, target):
    two = [k for k,v in bots.items() if len(v[0]) == 2]
    if not two:
        return None

    match = -1
    two = two[0]
    high,low = bots[two][0]
    high,low = ((high,low),(low,high))[high < low]
    for op in zip([low,high],bots[two][1]):
        if op[1][0] == 'output':
            outs[op[1][1]] = op[0]
        elif op[1][0] == 'bot':
            bots[op[1][1]] = (bots[op[1][1]][0] + [op[0]], bots[op[1][1]][1])
        if set(target) == set(bots[two][0]):
            match = two
        bots[two] = ([], bots[two][1])
    return match

def main(fname):
    lines = sorted(fname.read().strip().split('\n'))
    bots = {int(id):[[],((lt,int(low)),(ht,int(high)))] for line in lines for id, lt, low, ht, high in re.findall(r'bot (\d+).*(output|bot)\D+(\d+).*(output|bot)\D+(\d+)', line)}
    outs = {}

    for id,val in [(int(bot), int(val)) for line in lines for val, bot in re.findall(r'value (\d+)\D+(\d+)', line)]:
        bots[id] = (bots[id][0] + [val], bots[id][1])
    
    while (match := run_robots(bots, outs, (17, 61))) is not None:
        if match > 0:
            print (f'Part 1: {match}')
    
    print (f'Part 2: {outs[0] * outs[1] * outs[2]}')


if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
