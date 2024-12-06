""" Module for Advent of Code Day 6.
    https://adventofcode.com/2024/day/6
"""
import sys
import copy

class GuardGallivant:
    dirs = ((-1,0), (0,1), (1,0),(0,-1))
    gc = ('^', '>', 'v', '<')

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
        self.save = copy.deepcopy(self.grid)

    def walk_grid(self):
        gp = self.start
        dir = 0
        while self.valid_pos(gp):
            self.grid[gp[0]][gp[1]] = self.gc[dir]
            #self.pp()
            self.grid[gp[0]][gp[1]] = 'X'
            while True:
                r,c = gp[0] + self.dirs[dir][0], gp[1] + self.dirs[dir][1]
                if self.valid_pos([r,c]) and self.grid[r][c] == '#':
                    dir = (dir + 1) % 4
                    continue
                break
            gp = [r,c]
    
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
        
    def x_count(self) -> int:
        return sum(row.count('X') for row in self.grid)

    def reset(self) -> None:
        self.grid = copy.deepcopy(self.save)

    def find_loops(self) -> int:
        self.reset()
        cnt = 0
        for r in range(self.dims[0]):
            for c in range(self.dims[1]):
                if self.grid[r][c] == '.':
                    self.grid[r][c] = 'O'
                    cnt += int(self.has_loop())
                    self.grid[r][c] = '.'
        return cnt

def main(fname):

    gg = GuardGallivant(fname)

    gg.walk_grid()

    print (f'Part 1: {gg.x_count()}')
    print (f'Part 2: {gg.find_loops()}')
    return

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
