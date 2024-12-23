import sys
products = []
factors = []
count = 0

for line in sys.stdin:
    a, b = line.split(":")
    products.append(int(a))
    factors.append([int(x) for x in b.split(" ")[1:]])

def helper(nums):
    add = nums[0] + nums[1]
    mul = nums[0] * nums[1]
    if len(nums) == 2:
        return [add, mul]
    nums = nums[2:]
    nums.insert(0, add)
    adds = [x for x in helper(nums)]
    nums[0] = mul
    muls = [x for x in helper(nums)]
    return adds + muls

def check(goal, nums):
    return goal in helper(nums)

for i in range(len(products)):
    if check(products[i], factors[i]):
        count += products[i]

print(count)
