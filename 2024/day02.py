""" Module for Advent of Code Day 2.
    https://adventofcode.com/2024/day/2
"""
import sys
from rich import print
from rich.console import Console

def pp(levels, red = -1) -> str:
    return ' '.join([(f'{int(x)}', f'[bold bright_red]{x}[/]')[j == red] for j,x in enumerate(levels)])

def ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def safe(level) -> bool:
    increasing = all(1 <= level[i + 1] - level[i] <= 3 for i in range(len(level) - 1))
    decreasing = all(1 <= level[i] - level[i + 1] <= 3 for i in range(len(level) - 1))
    return increasing or decreasing

def dampener(level):
    if safe(level):
        print (f'{pp(level)}: [bold bright_green]Safe[/] without removing any level')
        return True
    for i,_ in enumerate(level):
        if safe(level[:i] + level[i+1:]):
            print (f'{pp(level, i)}: [bold bright_green]Safe[/] by removing the {ordinal(i+1)} level, [bold bright_red]{level[i]}[/].')
            return True
    print (f'{pp(level)}: [bold bright_red]Unsafe[/] regardless of which level is removed.')
    return False

def main(fname):

    console = Console(width=60)
    console.rule("[bold red]Logging")
    levels = [list(map(int, x.split())) for x in fname.read().strip().split('\n')]

    safety0 = list(map(safe, levels))
    safety1 = list(map(dampener, levels))
    console.rule("[bold red]Results")
    print (f'Part One: {sum(safety0)} safe reports')
    print (f'Part Two: {sum(safety1)} safe reports with dampener')

if __name__ == "__main__":
    arg = sys.stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as arg:
            main(arg)
    else:
        main(arg)
