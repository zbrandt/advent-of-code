import sys, re
from itertools import product
from collections import defaultdict

dirs = list(product([-1, 0, 1], repeat=2))

grid = None
def main(fname):
    target = list('XMAS')
    data = fname.read().strip()
    ddgrid = defaultdict(str,{(i,j): cell for i,row in enumerate(data.split()) for j,cell in enumerate(list(row)) })
    width = max(x[1] for x in ddgrid.keys())
    xmas_count = sum([[ddgrid[(k[0] + i*d[0],k[1] + i*d[1])] for i in range(len(target))] == target for d in dirs for k in list(ddgrid.keys())])

    m = re.findall(f'(?s)(?=(M|S).(M|S).{{{width}}}A.{{{width}}}(M|S).(M|S))', data)
    x_mas_count = sum(x[0] != x[3] and x[1] != x[2] for x in m)

    print(f'Part 1: {xmas_count}')
    print(f'Part 2: {x_mas_count}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
