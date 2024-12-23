import sys

line = sys.stdin.read()
blocks = ""
count = 0

index = 48
for i in range(len(line)):
    if i % 2 == 0:
        blocks += int(line[i]) * str(chr(index))
        index += 1
    else:
        blocks += int(line[i]) * '.'

def check(chars):
    for i in reversed(range(len(chars))):
        if chars[i] != '.':
            return i

chars = list(blocks)
i, j = blocks.index('.'), len(blocks) - 1
while i <= j:
    chars[i], chars[j] = chars[j], chars[i]
    i = chars.index('.')
    j = check(chars)

print(blocks)
# print(''.join(chars))
for i in range(chars.index('.')):
    if chars[i] != '.':
        count += i * int(ord(chars[i]) - 48)
print(count)
