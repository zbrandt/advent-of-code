grid = {i+j*1j: int(c) for i,r in enumerate(open('in.txt'))
                       for j,c in enumerate(r.strip())}

def search(pos, seen, height=0):
    if pos in grid and grid[pos] == height:
        if height < 9 or part==1 and pos in seen:
            return sum(search(pos+n, seen, height+1) for n in [1,-1,1j,-1j])
        seen.add(pos)
        return 1
    return 0

for part in 1, 2:
    print(sum(search(pos, set()) for pos in grid if grid[pos]==0))
