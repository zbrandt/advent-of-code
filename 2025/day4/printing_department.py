import numpy as np
from scipy.signal import convolve2d

def get_neighbors(grid):
    maps = { '.': 0, '@': 1 }
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    grid = np.array([list(map(lambda x: maps[x], row)) for row in grid])
    return convolve2d(grid, kernel, mode='same', boundary='fill', fillvalue=0)

def main(fname):
    one = two = 0
    grid = [list(x) for x in fname.read().split('\n')]
    neighbors = get_neighbors(grid)
    wave = 0
    print(grid)
    while not np.all(neighbors == get_neighbors(grid)) or wave == 0:
        neighbors = get_neighbors(grid)
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '@' and neighbors[i][j] < 4:
                    if wave == 0:
                        one += 1
                    two += 1
                    grid[i][j] = '.'
        wave += 1
    
    print(f"Part One: {one}")
    print(f"Part Two: {two}")

if __name__ == "__main__":
    import sys
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
