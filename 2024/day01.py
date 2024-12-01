import sys
from collections import Counter

all_nums = list(map(int,sys.stdin.read().split()))
left_nums  = all_nums[0::2]
right_nums = all_nums[1::2]
right_counts = Counter(right_nums)

distances = [abs(x-y) for x,y in zip(sorted(left_nums), sorted(right_nums))]
similarity = [x * right_counts[x] for x in left_nums]

print (f'Part 1: {sum(distances)  = } ')
print (f'Part 2: {sum(similarity) = } ')