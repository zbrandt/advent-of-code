from operator import add, mul

cat = lambda x,y: int(str(x) + str(y))

ans = 0
for line in open('in.txt'):
    tgt, x, *Y = map(int, line.replace(':', '').split())

    X = [x]
    for y in Y:
        X = [op(x,y) for x in X for op in (add,mul,cat)]

    if tgt in X: ans += tgt

print(ans)
