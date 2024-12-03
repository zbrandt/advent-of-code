import sys

def check(section):
    if (")" in section) and ("," in section):
        end = section.find(")")
        print(section)
        nums = [int(x) for x in section[:end].split(",")]
        return nums[0] * nums[1]
    return 0

result = 0
for line in sys.stdin:
    for i in range(len(line) - 4):
        if line[i:i+4] == "mul(":
            result += check(line[i+4:i+12])
print(result)
