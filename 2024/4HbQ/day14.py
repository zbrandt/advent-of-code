import re

bots = [[*map(int, re.findall(r'-?\d+',l))]
                   for l in open('in.txt')]

ffwd = lambda p,q,r,s: ((p+r*t) % w - w//2,
                        (q+s*t) % h - h//2)

w, h, t = 101, 103, 100
a, b, c, d = 0, 0, 0, 0

for bot in bots:
    p, q = ffwd(*bot)

    a += p > 0 and q > 0
    b += p > 0 and q < 0
    c += p < 0 and q > 0
    d += p < 0 and q < 0

print(a * b * c * d)

for t in range(10000):
    new = set(ffwd(*b) for b in bots)
    if len(new)==len(bots): print(t); break
