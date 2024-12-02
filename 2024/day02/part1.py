import sys

count = 0
for line in sys.stdin:
    numbers = [int(x) for x in line.split()]
    changes = []
    for i in range(len(numbers) - 1):
        diff = numbers[i + 1] - numbers[i]
        if abs(diff) > 3 or abs(diff) < 1:
            changes = []
        changes.append(numbers[i + 1] - numbers[i])
    if len(changes) > 0:
        valid = True
        for x in changes:
            if (x > 0) != (changes[0] > 0):
                valid = False
                break
        if valid:
            count += 1
print(count)