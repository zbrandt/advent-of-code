""" Module for Advent of Code Day 17.
    https://adventofcode.com/2015/day/16=7
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

def main(fname):

    def count (target, buckets, used=0, depth=0) -> int:
        if target == 0:
            return [used]
        total = []
        if buckets:
            bucket = list(buckets.items())[0]
            if bucket[1] <= target:
                total.extend(count(target - bucket[1], dict(list(buckets.items())[1:]), used+1, depth+1))
            total.extend(count(target, dict(list(buckets.items())[1:]), used, depth+1))
        return total

    buckets = {chr(ord('A')+i):int(vol) for i,vol in enumerate(re.findall(r'(\d+)',fname.read()))}
    target = (25,150)[max(buckets.values()) > 25]

    counts = count(target, buckets)
    minb = min(counts)
    print (f'Part 1: {len(counts)}')
    print (f'Part 2: {sum((bcnt == minb) for bcnt in counts)}')
    

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
