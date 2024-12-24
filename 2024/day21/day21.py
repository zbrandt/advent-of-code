""" Module for Advent of Code Day 21.
    https://adventofcode.com/2024/day/21
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
import numpy as np
from collections import Counter
from math import comb
from itertools import permutations as P
from functools import cache
from itertools import product

kpd = """
789
456
123
#0A
"""

arr = """
#^A
<v>
"""

darrows = { (-1,0): '<', (0,-1): '^', (1,0): '>', (0,1): 'v', (0,0): '.'}

xunit = (1,0)
yunit = (0,1)

def tmult(a,b):
    return (a[0]*b[0], a[1]*b[1])

def tunit(v):
    return (int(np.sign(v[0])), int(np.sign(v[1])))

def tabs(a):
    return (abs(a[0]), abs(a[1]))

def tadd(a,b):
    return (a[0] + b[0], a[1] + b[1])

def tsub(a,b):
    return (a[0] - b[0], a[1] - b[1])

def tcomb(v):
    return comb(abs(v[0])+abs(v[1]), abs(v[1]))

class Keypad:

    def __init__(self, keys:str, name):
        self.grid = { (x,y):ch for y,row in enumerate(keys.strip().splitlines()) for x,ch in enumerate(row.strip()) }
        self.rgrid = { v:k for k,v in self.grid.items() }
        self.w = max(p[0] for p in self.grid.keys())+1
        self.h = max(p[1] for p in self.grid.keys())+1
        self.apos = self.rgrid['A']
        self.gap = self.rgrid['#']
        self.name = name
        self.pos = self.apos

    def pp(self):
        print (f'Keypad "{self.name}" {self.w}x{self.h} A={self.apos}')
        print ('\n'.join(''.join(self.grid[(x,y)] for x in range(self.w)) for y in range(self.h)))
        print ('-' * self.w)

    @cache
    def katob(self, posa, posb, witha=True) -> list:

        dxy = tsub(posb, posa)
        mxy = tabs(dxy)
        uxy = tunit(dxy)
        gap = self.gap
        bad_path = None
        
        just_two = True

        moves = set()
        if just_two:
            # moves x,y and then y,x
            moves = list([darrows[tmult(uxy, xunit)] * mxy[0] + darrows[tmult(uxy, yunit)] * mxy[1], \
                         darrows[tmult(uxy, yunit)] * mxy[1] + darrows[tmult(uxy, xunit)] * mxy[0]])
        else:
            moves = darrows[tmult(uxy, xunit)] * mxy[0] + darrows[tmult(uxy, yunit)] * mxy[1]
            moves = list(set([''.join(x) for x in list(P(moves))]))
        
        if gap == (posa[0], posb[1]):
            bad_path = darrows[tmult(uxy, yunit)] * mxy[1] + darrows[tmult(uxy, xunit)] * mxy[0]
        elif gap == (posb[0], posa[1]):
            bad_path = darrows[tmult(uxy, xunit)] * mxy[0] + darrows[tmult(uxy, yunit)] * mxy[1]
        if bad_path:
            moves.remove(bad_path)

        # this line is just magic ...
        if just_two and len(moves) > 1:
            match uxy:
                case (1,1):
                    moves = [moves[1]]   # y,x
                case (1,-1):
                    moves = [moves[1]]   # x,y
                case (-1,-1):
                    moves = [moves[0]]   # x,y
                case (-1,1):
                    moves = [moves[0]]   # x,y
                case _:
                    pass
        
        moves = [x+'A' for x in moves]
        #print (fkatob({posa}={self.grid[posa]}, {posb}={self.grid[posb]}) => {len(moves)}:{moves}')
        return moves

    def moveto(self, ch) -> tuple[int, str]:
        epos = self.rgrid[ch]
        moves = self.katob(self.pos, epos)
        self.pos = epos
        return moves
    
    def enter_code(self, code) -> str:
        return ''.join(path for path in [self.moveto(ch)[0] for ch in code])

    def decode(self, code:str) -> str:
        rarrows = {v:k for k,v in darrows.items()}

        ans = ''
        while code:
            ch, *code = code
            if ch == 'A':
                ans += self.grid[self.pos]
            else:
                self.pos = tadd(self.pos,rarrows[ch])
                assert self.grid[self.pos] != '#'
        return ans

def code_paths(kp:Keypad, code:str):
    paths = [list(kp.moveto(ch)) for ch in code]
    #print (f'{paths=}')
    totals = [''.join(x) for x in list(product(*paths))]
    print (f'{code}: {[(len(x),x) for x in totals]}')
    return totals

def best_keypad_move(posa, posb):
    nkey = NumericKeypad("Keypad 1")
    a1key = ArrowKeypad("Arrowpad 1")
    a2key = ArrowKeypad("Arrowpad 2")

    moves1 = nkey.katob(posa, posb)
    moves2 = []

    print (f'{moves1=}')
    for m in moves1:
        moves2.append(a1key.katob(a1key.pos, a1key.rgrid[m]))
    print (f'{moves2=}')
    exit()


class NumericKeypad(Keypad):
    def __init__(self, name="keypad"):
        Keypad.__init__(self, kpd, name)

class ArrowKeypad(Keypad):
    def __init__(self, name="arrowpad"):
        Keypad.__init__(self, arr, name)
        self.grammar = self.build_grammar()
    
    def build_grammar(self) -> dict:
        vals = list(self.grid.values())
        vals.remove('#')
        key_pairs = list(product(vals, repeat=2))

        grammar = {}
        for _,p in enumerate(key_pairs):
            path = self.katob(self.rgrid[p[0]], self.rgrid[p[1]])[0]
            #print (f'{i:2d}: {p[0]} -> {p[1]} ==> {path}')

            prev = 'A'
            encode = []
            for ch in path:
                encode.append(self.katob(self.rgrid[prev], self.rgrid[ch])[0])
                prev = ch
            grammar[path] = encode
        return grammar

def decode_n_robots(s:str, robots:int):
    nkey = NumericKeypad("Keypad")
    akey = ArrowKeypad("Arrowpad")

    for _ in range(robots):
        s = akey.decode(s)
    s = nkey.decode(s)
    return s

def encode_n_robots(code:str, robots:int, verbose):
    nkey = NumericKeypad("Keypad")
    akey = ArrowKeypad("Arrowpad")

    if verbose:
        print (f'code: len={len(code)} "{code}"')
    code = nkey.enter_code(code)
    if verbose:
        print (f'code: len={len(code)} "{code}"')
    for _ in range(robots):
        code = akey.enter_code(code)
        if verbose:
            print (f'code: len={len(code)} "{code}"')

    return code

def encode_n_robots2(code:str, robots:int, verbose):
    nkey = NumericKeypad("Keypad")
    akey = ArrowKeypad("Arrowpad")

    if verbose:
        print (f'code: len={len(code)} "{code}"')
    code = nkey.enter_code(code)

    if verbose:
        print (f'code: len={len(code)} "{code}"')
    code = akey.enter_code(code)
    if verbose:
        print (f'code: len={len(code)} "{code}"')
    
    robots -=1
    code_counts = Counter(re.findall(f'([^A]*A)', code))
    code_length = sum([len(k) * v for k,v in code_counts.items()])
    #print (f'{code_length=}, {code_counts=}')
    for _ in range(robots):
        cc_next = Counter()
        for k,v in code_counts.items():
            for w in akey.grammar[k]:
                #print (f'{w=} * {v}: {k} --> {akey.grammar[k]}')
                cc_next[w] += v
        code_counts = cc_next
        code_length = sum([len(k) * v for k,v in code_counts.items()])
        #print (f'{_}: {code_length=}, {code_counts=}')
    
    code_length = sum([len(k) * v for k,v in code_counts.items()])
    return code_length

def main(fname):

    #library()
    #exit()

    verbose = False
    doors = fname.read().strip().split('\n')
    answer = 0
    robots = 25
    for d in doors:
        dcode = None
        if robots <= 8:
            code = encode_n_robots(d, robots, False)
            complexity = int(d[:3]) * len(code)
            dcode = decode_n_robots(code, robots)
            ec2 = encode_n_robots2(d, robots, False)
            if verbose:
                print (f'{d}: {int(d[:3]):3} * {len(code)} = {complexity} {code} {ec2=}')
            else:
                print (f'{d}: {int(d[:3]):3} * {len(code)} = {complexity} {ec2=}')
            #print (f'{d}: {code} --> {dcode}')
            assert d == dcode
        else:
            ec2 = encode_n_robots2(d, robots, False)
            complexity = int(d[:3]) * ec2
        answer += complexity
    print (f'Part 1: {answer}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
