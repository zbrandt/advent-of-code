import sys
products = []
factors = []
count = 0

for line in sys.stdin:
    a, b = line.split(":")
    products.append(int(a))
    factors.append([int(x) for x in b.split(" ")[1:]])

ops = [
    lambda x, y: [x + y],
    lambda x, y: [x * y],
    lambda x, y: [int(str(x) + str(y))]
]

def helper(nums):
    combos = []
    for op in ops:
        combos.extend(op(nums[0], nums[1]))
    if len(nums) == 2:
        return combos
    permutations = []
    for x in combos:
        permutations += helper([x] + nums[2:])
    return permutations

def check(goal, nums):
    return goal in helper(nums)

for i in range(len(products)):
    if check(products[i], factors[i]):
        count += products[i]

print(count)
