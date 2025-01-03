import sys
from collections import Counter

lines = sys.stdin.read().split('\n')
garden = [list(line.strip()) for line in lines]

visited = []
dr = [0, -1, 1, 0]
dc = [-1, 0, 0, 1]

def in_bounds(r, c):
    return r >= 0 and r < len(garden) and c >= 0 and c < len(garden[r])

def region(r, c):
    region = set()
    queue = [(r, c)]    
    while queue:
        p = queue[0]
        if p in visited:
            queue = queue[1:]
            continue
        for i in range(4):
            nr, nc = p[0] + dr[i], p[1] + dc[i]
            if in_bounds(nr, nc) and garden[nr][nc] == garden[r][c]:
                queue.append((nr, nc))
        region.add(p)
        visited.append(p)
    return list(region)

def perimeter(region):
    perimeter = 0
    for p in region:
        for i in range(4):
            nr, nc = p[0] + dr[i], p[1] + dc[i]
            if in_bounds(nr, nc) and garden[nr][nc] != garden[p[0]][p[1]]:
                perimeter += 1
            if not in_bounds(nr, nc):
                perimeter += 1
    return perimeter

cost = 0
for r in range(len(garden)):
    for c in range(len(garden[r])):
        reg = region(r, c)
        cost += perimeter(reg) * len(reg)
print(cost)
