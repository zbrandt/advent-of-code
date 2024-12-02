# count = 0

# def check(numbers):
#     for i in range(len(numbers) - 1):
#         change = numbers[i + 1] - numbers[i]
#         if (abs(change) > 3) or (abs(change) < 1) or ((change > 0) != ((numbers[1] - numbers[0]) > 0)):
#             return 2
#     return 1

# for line in open("/home/zachary/Desktop/GitHub/advent-of-code/2024/day02/input").readlines():
#     numbers = [int(x) for x in line.split()]
    
#     i, edits = 0, 0
#     while i < len(numbers) - 1:
#         change = numbers[i + 1] - numbers[i]
#         if (abs(change) > 3) or (abs(change) < 1) or ((change > 0) != ((numbers[1] - numbers[0]) > 0)):
#             nums1 = numbers[:]
#             nums2 = numbers[:]
#             nums1.pop(i)
#             nums2.pop(i + 1)
#             edits = min(check(nums1), check(nums2))
#             break;
#         i += 1
#     if edits < 2:
#         count += 1

#above is off by a count of 3 for some reason....

import sys

def safe(numbers):
    changes = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
    signs = [x > 0 for x in changes]
    outs = [abs(x) > 3 or abs(x) < 1 for x in changes]
    if all(signs) != any(signs):
        return False
    if any(outs):
        return False
    return True
    

count = 0
for line in sys.stdin:
    numbers = [int(x) for x in line.split()]
    if safe(numbers):
        count += 1
    else:
        removals = [safe(numbers[:i] + numbers[i + 1:]) for i in range(len(numbers))]
        print(numbers)
        print(any(removals))
        if any(removals):
            count += 1

print(count)
