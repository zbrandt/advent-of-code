import sys
city = []
antinodes = []

for line in sys.stdin:
    city.append([c for c in line[:len(line)-1]])

chars = [city[r][c] for r in range(len(city)) for c in range(len(city[r])) if city[r][c] != '.']
freqs = {char: [(r, c) for r in range(len(city)) for c in range(len(city[r])) if city[r][c] == char] for char in chars} 

tadd = lambda t1, t2: (t1[0] + t2[0], t1[1] + t2[1])
tsub = lambda t1, t2: (t1[0] - t2[0], t1[1] - t2[1])
tinv = lambda t: (-1 * t[0], -1 * t[1])

def check(t):
    r = t[0] >= 0 and t[0] < len(city)
    c = t[1] >= 0 and t[1] < len(city[0])
    return r and c

for char in chars:
    for start in freqs[char]:
        for end in freqs[char]:
            if start != end:
                diff = tsub(end, start)
                print(diff)
                locs = [tadd(end, diff), tadd(start, tinv(diff))]
                print(locs)
                antinodes.extend([pos for pos in locs if pos not in antinodes and check(pos)])

antinodes = list(set(antinodes))
print(len(antinodes))

for r in range(len(city)):
    for c in range(len(city[r])):
        if (r, c) in antinodes and city[r][c] == '.':
            city[r][c] = "#"

for r in city:
    line = '.'.join(r)
    print(line)