""" Module for Advent of Code Day 17.
    https://adventofcode.com/2015/day/16=7
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

def main(fname):

    def count (target, buckets, used=0) -> int:
        if target == 0:
            return [used]
        total = []
        if buckets:
            if buckets[0] <= target:
                total.extend(count(target - buckets[0], buckets[1:], used+1))
            total.extend(count(target, buckets[1:], used))
        return total

    buckets = [int(vol) for vol in re.findall(r'(\d+)',fname.read())]
    target = (25,150)[max(buckets) > 25]

    counts = count(target, buckets)
    minb = min(counts)
    print (f'Part 1: {len(counts)}')
    print (f'Part 2: {sum((bcnt == minb) for bcnt in counts)}')
    

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
