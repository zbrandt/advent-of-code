""" Module for Advent of Code Day 22.
    https://adventofcode.com/2016/day/22
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re

def viable(a,b) -> bool:
    return a['used'] != 0 and a != b and a['used'] <= b['avail']

def main(fname):
    #disks = re.findall(r'(?m)^/dev/grid/node-x(\d+)-y(\d+)\s+(\s+)\s+(\s+)\s+(\s+)\s+(\S+)$', fname.read())
    disks = [list(map(int,nums)) for nums in re.findall(r'(?m)^/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\S+)T\s+(?P<used>\S+)T\s+(?P<avail>\S+)T\s+(?P<use>\S+)%$', fname.read())]
    ddisks = { x+y*1j : {'key':x+y*1j, 'size':size, 'used':used, 'avail':avail, 'use':use} for x,y,size,used,avail,use in disks }
    disks = list(ddisks.values())

    ndisks = len(disks)

    viables = [viable(a,b) for _,a in enumerate(disks) for _,b in enumerate(disks)]
    print (f'Part 1: {sum(viables)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
