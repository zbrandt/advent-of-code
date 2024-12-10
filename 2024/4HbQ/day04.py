from collections import defaultdict

G = defaultdict(str) | {(i,j):c for i,r in enumerate(open(0))
                                for j,c in enumerate(r)}
g = list(G.keys())
D = -1,0,1

T = list('XMAS'),
print(sum([G[i+di*n, j+dj*n] for n in range(4)] in T
                for di in D for dj in D for i,j in g))

T = list('MAS'), list('SAM')
print(sum([G[i+d, j+d] for d in D] in T
      and [G[i+d, j-d] for d in D] in T for i,j in g))
