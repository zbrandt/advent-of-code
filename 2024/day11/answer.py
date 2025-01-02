import sys
stones = sys.stdin.read().strip().split(" ")

def check(s):
    while len(s) > 1 and s[0] == "0":
        s = s[1:]
    return s

b = 0
while b < 25:
    i = 0
    while i < len(stones):
        s = stones[i]
        if int(s) == 0:
            stones[i] = '1'
        elif len(s) % 2 == 0:
            stones[i] = check(s[0:len(s) // 2])
            stones.insert(i + 1, check(s[len(s) // 2:len(s)]))
            i += 1
        else:
            stones[i] = str(int(stones[i]) * 2024)
        i += 1
    b += 1

print(len(stones))