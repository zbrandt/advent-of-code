import sys
import re
from math import sqrt, floor, ceil

def solve_race(T, R) -> int:
    s1 = floor((T / 2) - sqrt(T*T - 4*R) / 2) + 1
    s2 = ceil ((T / 2) + sqrt(T*T - 4*R) / 2) - 1
    ans = s2 - s1 + 1
    print (f'solve_race({T=}, {R=}) --> {s1} -- {s2} --> {ans}')
    return ans

for line in sys.stdin:
    category, _, data = line.partition(':')
    if category == 'Time':
        times = list(map(int,data.split()))
        times2 = [int(''.join(data.split()))]
    if category == 'Distance':
        distances = list(map(int,data.split()))
        distances2 = [int(''.join(data.split()))]

ans = 1
for T,R in zip(times, distances):
    ans *= solve_race(T, R)
print (f'{ans=}')

ans = 1
for T,R in zip(times2, distances2):
    ans *= solve_race(T, R)
print (f'{ans=}')