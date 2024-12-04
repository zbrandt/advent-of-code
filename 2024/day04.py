import sys

letters = []
for line in sys.stdin:
    row = []
    for c in range(len(line) - 1):
        row.append(line[c])
    letters.append(row)

sequence = ["M", "A", "S"]
def check(i, position, direction):
    if (i == 3):
        return 1
    x = position[0] + direction[0]
    y = position[1] + direction[1]
    if (x >= 0 and x < len(letters[0])) and (y >= 0 and y < len(letters)):
        letter = letters[y][x]
        if (letter == sequence[i]):
            return check(i + 1, [x, y], direction)
    return 0

count = 0
shiftsx = [-1, 0, 1, -1, 1, -1, 0, 1]
shiftsy = [-1, -1, -1, 0, 0, 1, 1, 1]
for y in range(len(letters)):
    for x in range(len(letters[y])):
        if (letters[y][x] == "X"):
            for s in range(len(shiftsx)):
                count += check(0, [x, y], [shiftsx[s], shiftsy[s]]) 
print(count)

count = 0
dx = [-1, 1, -1, 1]
dy = [-1, -1, 1, 1]
for i in range(len(letters)):
    for j in range(len(letters[y])):
        if (letters[i][j] == "A"):
            adj = []
            for s in range(len(dx)):
                x = j + dx[s]
                y = i + dy[s]
                if (x >= 0 and x < len(letters[0])) and (y >= 0 and y < len(letters)):
                    letter = letters[y][x]
                    if (letter in ["S", "M"]):
                        adj.append(letters[y][x])
            if (len(adj) == 4) and (adj.count("M") == 2) and (adj != ["S", "M", "M", "S"]) and (adj != ["M", "S", "S", "M"]):
                print(adj, i, j)
                count += 1
print(count)