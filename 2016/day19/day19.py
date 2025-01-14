""" Module for Advent of Code Day 18.
    https://adventofcode.com/2016/day/18
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
from math import log
from  itu.algs4.searching import red_black_bst # https://github.com/itu-algorithms/itu.algs4/blob/master/README.md
from rich import print
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

pb_format = [TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
]
class Table:
    def __init__(self, size, progress:bool = True):
        self.size = size
        self.seats:red_black_bst.RedBlackBST = red_black_bst.RedBlackBST()

        progress_bar = Progress(*pb_format, disable=not progress)
        with progress_bar as p:
            if progress:
                print (f'Setting up round table for {size} elves ...')
                setup = p.add_task(description='', total=size)
                p.update(setup, advance=1)

            for i in range(size):
                self.seats.put(i+1, 0)
                if progress:
                    p.update(setup, advance=1)
            p.update(setup, visible=False)

    def play(self, rule, progress:bool = True):
        progress_bar = Progress(*pb_format, disable=not progress)
        with progress_bar as p:
            if progress:
                print (f'Playing {rule.__name__} game ...')
                game_play = p.add_task(description='', total=self.seats.size())
                p.update(game_play, advance=1)

            pos = self.seats.min()

            while self.seats.size() > 1:
                target_elf = rule(self, pos)
                self.seats.delete(target_elf)
                pos = self.elf_left(pos)
                if progress:
                    p.update(game_play, advance=1)
            
            p.update(game_play, visible=False)
        return self.seats.min()

    def elf_left(self, elf):
        target = elf + 1 if elf < self.seats.max() else self.seats.min()
        elf = self.seats.ceiling(target)
        return elf

    def elf_across(self, elf):
        nseats = self.seats.size()
        target = (self.seats.rank(elf) + nseats // 2) % nseats
        across = self.seats.select(target)
        return across

#simple closed form solution :(
def part2(n):
    p = 3**int(log(n-1,3))
    return n-p+max(n-2*p,0)

def main(fname):

    progress = True
    data = int(fname.read().strip())
    rules = [Table.elf_left, Table.elf_across]

    for i, rule in enumerate(rules):
        table = Table(int(data), progress)
        winner = table.play(rule, progress)
        print (f'Part {i+1}: {winner}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
