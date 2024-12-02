""" Module for Advent of Code Day 2.
    https://adventofcode.com/2024/day/2
"""
import sys
from rich import print

def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def safe(level) -> bool:
    prev = level[0]
    slope = level[1] - level[0] > 0
    for i, x in enumerate(level[1:]):
        if slope != ((x - prev) > 0):
            return False
        diff = abs(x - prev)
        if diff < 1 or diff > 3:
            return False
        prev = x
    return True

def tolerant(level):
    level_str = ' '.join(map(str, level))
    if safe(level):
        print (f'{level_str}: [bold bright_green]Safe[/] without removing any level')
        return True
    else:   
        any_safe = False
        for i,_ in enumerate(level):
            level1 = level[:i] + level[i+1:]
            is_safe = safe(level1)
            any_safe |= is_safe
            if is_safe:
                level_str = ' '.join([(f'{int(x)}', f'[bold bright_red]{x}[/]')[i==j] for j,x in enumerate(level)])
                print (f'{level_str}: [bold bright_green]Safe[/] by removing the {ordinal(i+1)} level, [bold bright_red]{level[i]}[/].')
                break
        if not any_safe:
            print (f'{level_str}: [bold bright_red]Unsafe[/] regardless of which level is removed.')
        return any_safe

def main(fname):

    levels = [list(map(int, x.split())) for x in fname.read().strip().split('\n')]
        
    safety0 = list(map(safe, levels))
    safety1 = list(map(tolerant, levels))
    print (f'Part 1: {sum(safety0)}')
    print (f'Part 2: {sum(safety1)}')

if __name__ == "__main__":
    arg = sys.stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as arg:
            main(arg)
    else:
        main(arg)
