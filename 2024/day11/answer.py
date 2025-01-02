import sys
from collections import Counter
stones = Counter(list(map(int, sys.stdin.read().split(" "))))

i = 0
while i < 75:
    temp = Counter()
    for s, c in stones.items():
        if s == 0:
            temp[1] += c
        elif len(str(s)) % 2 == 0:
            st = str(s)
            half = len(st) // 2
            f, l = int(st[:half]), int(st[half:])
            temp[f] += c
            temp[l] += c
        else:
            temp[s * 2024] += c
    stones = temp
    i += 1

print(sum(stones.values()))

