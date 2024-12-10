from functools import cmp_to_key

rules, pages = open('in.txt').read().split('\n\n')
cmp = cmp_to_key(lambda x, y: -(x+'|'+y in rules))

a = [0, 0]
for p in pages.split():
    p = p.split(',')
    s = sorted(p, key=cmp)
    a[p!=s] += int(s[len(s)//2])

print(*a)
