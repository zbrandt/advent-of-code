import sys

count = 0
dial = 50
for line in sys.stdin:
    instruction = line.strip()
    spin = int(instruction[1:])
    print(dial, count)
    if instruction[:1] == "R":
        for i in range(dial + 1, dial + spin + 1):
            if i % 100 == 0:
                count += 1
        dial = (dial + spin) % 100
    else:
        for i in range(dial - spin, dial):
            if i % 100 == 0:
                count += 1
        dial = (dial - spin) % 100
    
print(count)