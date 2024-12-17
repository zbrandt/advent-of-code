""" Module for Advent of Code Day 16.
    https://adventofcode.com/2024/day/16
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import deque
from collections import defaultdict
from copy import copy, deepcopy


def main(fname) -> None:

    dirs = [(-1,0), (0,1), (1,0), (0,-1)]
    east = dirs.index((-1,0))

    def circ(a,b):
        #print (f'circ({a},{b}) ->', end='')
        m = len(dirs)
        a,b=a%m,b%m
        if a<b:
            a,b=b,a
        res = min(a-b , b+m-a)
        #print (f'{res}')
        return res


    def tadd(a:tuple, b:tuple) -> tuple:
        return (a[0]+b[0], a[1]+b[1])
    
    def tneg(a:tuple) -> tuple:
        return (-a[0], -a[1])

    class Triplet:
        def __init__(self, p, d, s):
            self.pos = p
            self.dir = d
            self.score = s

        def tuple(self):
            return (self.pos, self,dir, self.score)

        def __str__(self):
            return f'Triplet(p={self.pos}, d={self.dir}, s={self.score})'

        def __repr__(self):
            return f'Triplet(p={self.pos}, d={self.dir}, s={self.score})'

    def get_neighbors(m, s, t:Triplet):
        empties = [Triplet(tadd(t.pos,dirs[d]),(d+2)%4,0) for d in range(4) if m[tadd(t.pos,dirs[d])] != '#' and (d != t.dir or d != (t.dir+2)%4)]
        neighbors = {Triplet(e.pos, e.dir, t.score + (1001,1)[t.dir == e.dir or t.dir==-1]) for e in empties if e.score < s[e.pos][e.dir]}
        return neighbors

    def ppmaze(w, h, m):
        x = f'{'\n'.join(''.join(m[(x,y)] for x in range(w)) for y in range(h))}'
        print (x)

    def solve(m, spos, epos):
        scores = defaultdict(lambda : copy([100_000_000, 100_000_000, 100_000_000, 100_000_000]))
        scores[epos] = [0]*4
        neighbors = get_neighbors(m, scores, Triplet(epos, -1, 0))
        for n in neighbors:
            scores[n.pos][n.dir] = n.score

        m2 = deepcopy(m)
        seats = set()
        d = deque([[t, set([t.pos, epos])] for t in neighbors])
        while d:
            #print (f'{d=}')
            t, path = d.popleft()
            neighs = get_neighbors(m, scores, t)
            neighbors = [n for n in neighs if n.pos not in path]
            for n in neighbors:
                if n.score <= scores[n.pos][n.dir]:
                    #print (f'{n=} {n.score} {scores[n.pos]}')
                    scores[n.pos][n.dir] = n.score
                    if n.dir != t.dir:
                        scores[t.pos][n.dir] = n.score - 1
                    #print (f'  new low score at {(n.pos, n.dir)} = {n.score}')
                    if n.pos == spos:
                        en = Triplet(n.pos, east, n.score + ((east - n.dir) % 4) * 1000)
                        if en.score <= scores[en.pos][en.dir]:
                            print (f'min path {en.score }')
                            if en.score < scores[en.pos][en.dir]:
                                seats = set()
                            scores[en.pos][en.dir] = en.score
                            seats = seats | path | set([n.pos])
                    else:
                        npath = path | set([n.pos])
                        print (f'append {n=} {len(npath)=} {len(seats)=}')
                        if len(npath) > 3000:
                            m2[n.pos] = 'X'
                            ppmaze(w,h,m2)
                            input()
                        d.append([n, npath])
                        
        score1 = scores[spos][east]
        for xy in seats:
            maze[xy] = 'O'
        ppmaze(w,h,m)
        print (f'Part 1: {score1}')
        print (f'Part 2: {len(seats)}')
        exit()

        errors = set()
        seats = set([spos])
        txy = Triplet(spos, east, score1)
        print (f'seats: append {txy=} START')
        d = deque([txy])
        while d:
            t = d.popleft()
            match = 0
            for i,dxy in enumerate(dirs):
                pxy = tadd(t.pos, dxy)
                target = t.score - (circ(t.dir,i+2) * 1000 + 1)
                print (f'  {t=}: check {i},{pxy}: {target=} {scores[pxy]}')
                if target in scores[pxy]:
                    match += 1
                    txy = Triplet(pxy,(i+2)%4,target)
                    if txy not in d:
                        d.append(txy)
                    if pxy not in seats:
                        print (f'seats: append {txy=}')
                        seats.add(pxy)
            if match == 0 and t.pos != epos:
                print (f'{t=} no matches')
                errors.add(t.pos)
                input()

        print (f'{scores[epos]=}')
        for xy in seats:
            maze[xy] = 'O'
        for xy in errors:
            maze[xy] = 'X'
        ppmaze(w,h,m)
        print (f'Part 2: {len(seats)}')


    
    data = fname.read()
    maze = {(x,y):ch for y,row in enumerate(data.split('\n')) for x,ch in enumerate(row)}
    w,h = max(k[0] for k in maze.keys())+1, max(k[1] for k in maze.keys())+1
    epos = [k for k,v in maze.items() if v == 'E'][0]
    spos = [k for k,v in maze.items() if v == 'S'][0]

    #print (maze)
    print (f'{spos=} {epos=} {w=} {h=}')
    ppmaze (w, h, maze)
    solve(maze, spos, epos)

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
