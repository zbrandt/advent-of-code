import sys
products = []
factors = []
count = 0

for line in sys.stdin:
    a, b = line.split(":")
    products.append(int(a))
    factors.append([int(x) for x in b.split(" ")[1:]])

def helper(nums, total):
    add = nums[0] + nums[1]
    mul = nums[0] * nums[1]
    if len(nums) == 2:
        return [add, mul]
    nums = nums[2:]
    return [x for x in helper(nums.insert(0, add), add)] + [x for x in helper(nums[2:].insert(0, mul), mul)]

def check(goal, nums):
    return goal in helper(nums, 0)

for i in range(len(products)):
    if check(products[i], factors[i]):
        count += products[i]

print(count)
