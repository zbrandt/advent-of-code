""" Module for Advent of Code Day 6.
    https://adventofcode.com/2024/day/6
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import defaultdict
from rich.progress import track
class GuardGallivant:
    dirs = ((-1,0), (0,1), (1,0),(0,-1))
    draw = defaultdict(lambda : '\u2588',
                        [(0b0101, '\u2503'), (0b1010, '\u2501'),
                         (0b0011, '\u2517'), (0b0110, '\u250f'), (0b1100, '\u2513'),(0b1001, '\u251b'),
                         (0b0111, '\u2523'), (0b1101, '\u252b'),
                         (0b1111, '\u254b'),
                        ])

    def pp(self) -> None:
        print ('\n'.join([''.join(row) for row in self.grid]))
        print ('=' * len(self.grid[0]))

    def find_start(self):
        for i, row in enumerate(self.grid):
            if '^' in row:
                return [i,row.index('^')]
        return None

    def valid_pos(self, pos) -> bool:
        return pos[0] >= 0 and pos[0] < self.dims[0] and pos[1] >= 0 and pos[1] < self.dims[1]

    def __init__(self, fname) -> None:
        self.grid = [list(row) for row in fname.read().strip().split()]
        self.start = self.find_start()
        self.dims = [len(self.grid), len(self.grid[0])]
        self.obstacles = []
        self.path = defaultdict(int)

    def walk_grid(self):
        r,c = self.start
        direction = 0
        while self.valid_pos((r,c)):
            self.grid[r][c] = 'X'
            self.path[(r,c)] |= 1 << ((direction + 2) % 4)
            while True:
                rx,cx = r + self.dirs[direction][0], c + self.dirs[direction][1]
                if self.valid_pos([rx,cx]) and self.grid[rx][cx] == '#':
                    direction = (direction + 1) % 4
                    continue
                break
            self.path[(r,c)] |= 1 << direction
            r,c = rx,cx

    def has_loop(self) -> bool:
        r,c = self.start
        direction = 0
        steps = {}
        while self.valid_pos((r,c)):
            while True:
                rx,cx = r + self.dirs[direction][0], c + self.dirs[direction][1]

                # check for loop
                if (rx,cx) in steps:
                    if steps[(rx,cx)] == direction:
                        return True
                steps[(rx,cx)] = direction

                if self.valid_pos([rx,cx]) and (self.grid[rx][cx] == '#' or self.grid[rx][cx] == 'O'):
                    direction = (direction + 1) % 4
                    continue
                break
            r,c = rx,cx
        return False

    def find_loops(self):
        for r,c in track(self.path.keys(), description="Find loops..."):
            self.grid[r][c] = 'O'
            if self.has_loop():
                self.obstacles.append((r,c))
            self.grid[r][c] = '.'

    def show_tracks(self):
        for k,v in self.path.items():
            self.grid[k[0]][k[1]] = self.draw[v]
        for obstacle in self.obstacles:
            self.grid[obstacle[0]][obstacle[1]] = 'O'
        self.grid[self.start[0]][self.start[1]] = '^'

def main(fname):


    gg = GuardGallivant(fname)

    gg.walk_grid()
    gg.find_loops()
    gg.show_tracks()
    gg.pp()
    print (f'Part 1: {len(gg.path)}')
    print (f'Part 2: {len(gg.obstacles)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
