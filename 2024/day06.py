""" Module for Advent of Code Day 6.
    https://adventofcode.com/2024/day/6
"""
import sys
from rich.progress import track
class GuardGallivant:
    dirs = ((-1,0), (0,1), (1,0),(0,-1))

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
        self.xes = []

    def walk_grid(self):
        r,c = self.start
        direction = 0
        while self.valid_pos((r,c)):
            self.grid[r][c] = 'X'
            self.xes.append((r,c))
            while True:
                rx,cx = r + self.dirs[direction][0], c + self.dirs[direction][1]
                if self.valid_pos([rx,cx]) and self.grid[rx][cx] == '#':
                    direction = (direction + 1) % 4
                    continue
                break
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
        for r,c in track(self.xes, description="Find loops..."):
            self.grid[r][c] = 'O'
            if self.has_loop():
                self.obstacles.append((r,c))
            self.grid[r][c] = '.'

    def add_start_and_obstacles(self):
        for obstacle in self.obstacles:
            self.grid[obstacle[0]][obstacle[1]] = 'O'
        self.grid[self.start[0]][self.start[1]] = '^'

def main(fname):
    gg = GuardGallivant(fname)

    gg.walk_grid()
    gg.find_loops()
    gg.add_start_and_obstacles()
    gg.pp()
    print (f'Part 1: {len(gg.xes)}')
    print (f'Part 2: {len(gg.obstacles)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
