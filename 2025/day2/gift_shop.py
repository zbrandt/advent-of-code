import sys

# def invalid(id):
#     if len(id) % 2 != 0:
#         return False
#     return id[:(len(id) // 2)] == id[(len(id) // 2):]

def invalid(id):
    i = len(id) // 2
    while i > 0:
        if "".join(id.split(id[:i])) == "":
            return True
        i -= 1
    return False    

invalid_sum = 0
ranges = sys.stdin.readline().split(',')
for ids in ranges:
    start, end = ids.split('-')
    for id in range(int(start), int(end) + 1):
        if invalid(str(id)):
            invalid_sum += id
print(invalid_sum)