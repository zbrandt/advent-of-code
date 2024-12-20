""" Module for Advent of Code Day 18.
    https://adventofcode.com/2024/day/18
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from collections import deque
from collections import Counter
from collections import defaultdict
from copy import copy
from rich import print # pylint: disable=redefined-builtin

def tadd (a,b):
    return (a[0]+b[0], a[1]+b[1])

dirs = ((-1,0), (0,-1), (0,1), (1,0))
cuts = ((-2,0), (0,-2), (0,2), (2,0))

def cheat_diamond(minsize, maxsize) -> set:
    cd = { (x,y) for x in range (-maxsize, maxsize+ 1) for y in range (-maxsize, maxsize +1) if minsize <= abs(x)+abs(y) <= maxsize }
    return cd

def grid_distance(a,b) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

class RaceCondition:
    def __init__(self, data):
        self.track = {(x,y):ch for y,row in enumerate(data.split('\n')) for x,ch in enumerate(row)}
        self.w = max(xy[0] for xy in self.track.keys())+1
        self.h = max(xy[1] for xy in self.track.keys())+1
        self.spos = [xy for xy in self.track.keys() if self.track[xy] == 'S'][0]
        self.epos = [xy for xy in self.track.keys() if self.track[xy] == 'E'][0]
        print (f'Track {self.w}x{self.h} Start={self.spos} End={self.epos}')

        self.min_path_list = self.min_path()
        self.min_path_dict = {p:i for i,p in enumerate(self.min_path_list)}
        self.short_cuts = defaultdict(set)
    
    def path_distance(self, p, q):
        assert p in self.min_path_dict and q in self.min_path_dict
        return abs(self.min_path_dict[p] - self.min_path_dict[q])
    
    def find_short_cuts2(self, path, p, size=2):
        assert p in path
        cd = cheat_diamond(2,size)
        short_cuts = set()
        for i,dxy in enumerate(cd):
            xy2 = tadd(p, dxy)
            if xy2 in path:
                pair = sorted([p, xy2])
                short_cuts = short_cuts | {tuple(pair)}
        return short_cuts

    def find_short_cuts(self, dist):
        progress = 0
        found = 0
        self.short_cuts = defaultdict(set)
        total = (len(self.min_path_list) ** 2) // 2
        for i,p in enumerate(self.min_path_list):
            for j,q in enumerate(self.min_path_list[i+1:]):
                progress += 1
                if progress % 9967 == 0:
                    print (f'{progress:6d}/{total}  find_short_cuts:{found}', end='\r')
                    pass
                if grid_distance(p,q) > 1 and grid_distance(p,q) <= dist:
                    #print (f'{i=} {j=} ..... {p=} {q=} {grid_distance(p,q)=}')
                    pair = sorted([p, q])
                    pdist = self.path_distance(p, q)-grid_distance(p, q)
                    if pdist > 0:
                        found += 1
                        self.short_cuts[pdist].add(tuple(pair))
        print()

    def min_path(self):
        dq = deque([[self.spos]])
        seen = set()
        while dq:
            path = dq.popleft()
            p = path[-1]
            if p not in seen:
                seen.add(p)
                if p == self.epos:
                    break
                for d in dirs:
                    if self.track[tadd(p,d)] != '#':
                        dq.append(path + [tadd(p,d)])
        
        return path


def main(fname):
    rc = RaceCondition(fname.read())
    print (f'Shortest time is {len(rc.min_path_list)-1} ps')

    rc.find_short_cuts(2)
    report = sorted([(k,len(v)) for k,v in rc.short_cuts.items()])
    for tim,cnt in report:
        if tim >= 100:
            #print (f'There are {cnt} cheats that save {tim} picoseconds.')
            pass
    part1 = sum([len(v) for k,v in rc.short_cuts.items() if k >= 100])
    print (f'Part 1: {part1}')
    print ('-' * 20)

    rc.find_short_cuts(20)
    report = sorted([(k,len(v)) for k,v in rc.short_cuts.items()])
    for tim,cnt in report:
        if tim >= 50:
            print (f'There are {cnt} cheats that save {tim} picoseconds.')
            pass
    part2 = sum([len(v) for k,v in rc.short_cuts.items() if k >= 100])
    print (f'Part 2: {part2}')




    if False:
        short_cuts = set()
        for i,p in enumerate(mp):
            print (f'{i+1:6d}/{len(mp)}  short_cuts:{len(short_cuts)}', end='\r')
            short_cuts = short_cuts | rc.find_short_cuts(mp, p, 20)
        print()
        print (f'{len(short_cuts)=}')
        sc_lens = [abs(mp.index(sc[0]) - mp.index(sc[1]))-2 for sc in short_cuts]
        print (f'{len(sc_lens)=}')
        if False:
            over50 = sorted([(x,y) for x,y in Counter(sc_lens).most_common() if x >= 50])
            for v,c in over50:
                print (f'There are {c} cheats that save {v} picoseconds.')
                pass

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
