""" Module for Advent of Code Day 6.
    https://adventofcode.com/2024/day/6
"""
import sys

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
        dir = 0
        while self.valid_pos([r,c]):
            self.grid[r][c] = 'X'
            self.xes.append((r,c))
            while True:
                rx,cx = r + self.dirs[dir][0], c + self.dirs[dir][1]
                if self.valid_pos([rx,cx]) and self.grid[rx][cx] == '#':
                    dir = (dir + 1) % 4
                    continue
                break
            r,c = rx,cx
    
    def has_loop(self) -> bool:
        gp = self.start
        dir = 0
        steps = {}
        while self.valid_pos(gp):
            while True:
                r,c = gp[0] + self.dirs[dir][0], gp[1] + self.dirs[dir][1]
                if (r,c) in steps:
                    if steps[(r,c)] == dir:
                        return True
                steps[(r,c)] = dir
                if self.valid_pos([r,c]) and (self.grid[r][c] == '#' or self.grid[r][c] == 'O'):
                    dir = (dir + 1) % 4
                    continue
                break
            gp = [r,c]
        return False

    def find_loops(self) -> None:
        for r in range(self.dims[0]):
            for c in range(self.dims[1]):
                ch = self.grid[r][c]
                if ch == 'X':
                    self.grid[r][c] = 'O'
                    if self.has_loop():
                        self.obstacles.append((r,c))
                    self.grid[r][c] = '.'

        for obstacle in self.obstacles:
            self.grid[obstacle[0]][obstacle[1]] = 'O'

def main(fname):

    gg = GuardGallivant(fname)

    gg.walk_grid()
    print (f'Part 1: {len(gg.xes)}')
    #gg.pp()

    gg.find_loops()
    print (f'Part 2: {len(gg.obstacles)}')
    #gg.pp()

    return

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
