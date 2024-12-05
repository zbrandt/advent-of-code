""" Module for Advent of Code Day 5.
    https://adventofcode.com/2024/day/5
"""
import sys
from collections import defaultdict

def is_ordered(rules, update, fix=False, depth=0) -> int:
    print (f'{' '*(depth+1)*int(fix)}is_ordered({update}, {fix=})')
    in_order = True
    dupdate = {v: i for i,v in enumerate(update)}
    for i,v in enumerate(update):
        if v in rules:
            r = rules[v]
            for rv in r:
                if rv in dupdate:
                    j = dupdate[rv]
                    if j < i:
                        if fix:
                            fixed_update = update.copy()
                            fixed_update[i] = update[j]
                            fixed_update[j] = update[i]
                            return is_ordered(rules, fixed_update, True, depth+1)
                        in_order = False
                        break
    return (update[len(update)//2] * int(in_order))

def main(fname):
    lines = fname.read().strip().split()
    rules = []
    updates = []
    for l in lines:
        if '|' in l:
            rules.append(list(map(int,l.split('|'))))
        else:
            updates.append(list(map(int,l.split(','))))

    drules = defaultdict(list)
    for r in rules:
        drules[r[0]].append(r[1])

    ordered = [is_ordered(drules, u) for u in updates]        
    print (f'Part 1: {sum(ordered)}')

    unordered = [is_ordered(drules, u, True) for i,u in enumerate(updates) if not ordered[i]]
    print (f'Part 2: {sum(unordered)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
