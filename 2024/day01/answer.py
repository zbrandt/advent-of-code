import sys

first = []
second = []
totalDistance = 0
for x in sys.stdin:
    numbers = x.split()
    first.append(int(numbers[0]))
    second.append(int(numbers[1]))

first = sorted(first)
second = sorted(second)

for i in range(len(first)):
    totalDistance += abs(first[i] - second[i])

print(totalDistance)

from collections import Counter

totalDistance = 0
pairs = Counter(second)
for i in first:
    totalDistance += i * pairs[i]

print(totalDistance) 