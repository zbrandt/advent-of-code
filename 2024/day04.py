import sys, re

directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]

def xmas(grid, row, col, dir=None) -> int:
    if dir == None:
        return sum(xmas(grid, row, col, dir) for dir in directions)
    match = 'XMAS'
    while match:
        ch = grid[row][col]
        if ch != match[0]:
            return 0
        #print (f'xmas(grid, {row=}, {col=}, {dir=}, {ch=})')
        match = match[1:]
        row,col = row+dir[0], col+dir[1]
    return 1

def x_mas(grid, row, col) -> int:
    if (grid[row][col] == 'A' and
        grid[row+1][col+1] in 'MS' and
        grid[row+1][col-1] in 'MS' and
        grid[row-1][col-1] in 'MS' and
        grid[row-1][col+1] in 'MS' and
        grid[row-1][col-1] != grid[row+1][col+1] and
        grid[row-1][col+1] != grid[row+1][col-1]):
        #print (f'grid[{row}][{col}]')
        return 1
    return 0

def main(fname):
    grid = [list(x) for x in fname.read().strip().split()]

    xgrid = []
    xgrid.append(['.'] * (len(grid[0]) + 2))
    for row in grid:
        xgrid.append(['.'] + row + ['.'])
    xgrid.append(['.'] * (len(grid[0]) + 2))

    for row in xgrid:
        print (''.join(row))

    xmas_count = 0
    x_mas_count = 0
    for row,_ in enumerate(xgrid):
        for col,_ in enumerate(_):
            xmas_count += xmas(xgrid, row, col)
            x_mas_count += x_mas(xgrid, row, col)
    print (f'Part 1: {xmas_count=}')
    print (f'Part 2: {x_mas_count=}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
