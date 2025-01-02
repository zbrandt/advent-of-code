import sys
map = []
heads = []

for line in sys.stdin:
    row = []
    for i in range(len(line)):
        if line[i] == "0":
            heads.append((len(map), i))
        if line[i] != "\n":
            row.append(line[i])
    map.append(row)

def in_bounds(r, c):
    return r >= 0 and r < len(map) and c >= 0 and c < len(map[0])

ax = [-1, 0, 0, 1]
ay = [0, 1, -1, 0]
def check(x, r, c):
    if x == 9:
        return [(r, c)]
    dest = []
    for i in range(4):
        dr = r + ay[i]
        dc = c + ax[i]    
        if in_bounds(dr, dc) and (int(map[dr][dc]) == x + 1):
            dest.extend(check(x + 1, dr, dc))
    return dest

sum = 0
ratings = 0
for head in heads:
    dest = check(0, head[0], head[1])
    ratings += len(dest)
    sum += len(set(dest))
print(sum)
print(ratings)