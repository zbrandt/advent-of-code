data = [[*map(int, l.split())] for l in open('data.txt')]

def good(d, s=0):
    for i in range(len(d)-1):
        if not 1 <= d[i]-d[i+1] <= 3:
            return s and any(good(d[j-1:j] + d[j+1:]) for j in (i,i+1))
    return True

for s in 0, 1: print(sum(good(d, s) or good(d[::-1], s) for d in data))
