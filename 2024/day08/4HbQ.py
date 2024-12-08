G = {i+j*1j: c for i,r in enumerate(open(0))
               for j,c in enumerate(r.strip())}

for N in [1], range(50): print(len({a + n*(a-b)
    for a in G for b in G if '.' < G[a] == G[b]
    and a != b for n in N} & {*G}))
