import sys

line = sys.stdin.read()
blocks = ""
files = []
count = 0

index = 48
for i in range(len(line)):
    if i % 2 == 0:
        file = int(line[i]) * str(chr(index))
        blocks += file
        files.insert(0, file)
        index += 1
    else:
        blocks += int(line[i]) * '.'

f, s = 0, lambda x: '.' * len(x)
while f < len(files):
    file = files[f]
    space = s(file)
    if space in blocks:
        i, j = blocks.index(space), blocks.index(file)
        if i < j:
            blocks = blocks[0:i] + file + blocks[i + len(file):j] + space + blocks[j + len(space):len(blocks)]
    f += 1
    
chars = list(blocks)
for i in range(len(blocks)):
    if chars[i] != '.':
        count += i * int(ord(chars[i]) - 48)
print(count)
