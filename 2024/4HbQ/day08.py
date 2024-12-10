from itertools import permutations

G = {i+j*1j: c for i,r in enumerate(open(0))
               for j,c in enumerate(r.strip())}

for r in [1], range(50):
    anti = []
    for freq in {*G.values()} - {'.'}:
        ants = [p for p in G if G[p] == freq]
        pairs = permutations(ants, 2)
        anti += [a+n*(a-b) for a,b in pairs
                           for n in r]

    print(len(set(anti) & set(G)))
