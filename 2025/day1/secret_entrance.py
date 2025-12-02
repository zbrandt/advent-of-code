import sys

count = 0
dial = 50
for line in sys.stdin:
    instruction = line.strip()
    
    if instruction[:1] == "R":
        dial = (dial + int(instruction[1:])) % 100
    else:
        dial = (dial - int(instruction[1:])) % 100
    
    if dial == 0:
        count += 1

print(count)