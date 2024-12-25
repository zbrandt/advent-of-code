from itertools import combinations


computers, connections = set(), set()
for line in open('in.txt'):
    a, b = line.strip().split('-')
    computers.update([a, b])
    connections.update([(a,b), (b,a)])


print(sum({(a,b), (b,c), (c,a)} < connections
          and 't' in (a + b + c)[::2]
          for a, b, c in combinations(computers, 3)))


networks = [{c} for c in computers]
for n in networks:
    for c in computers:
        if all((c,d) in connections for d in n): n.add(c)

print(*sorted(max(networks, key=len)), sep=',')
