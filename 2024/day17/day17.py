""" Module for Advent of Code Day 17.
    https://adventofcode.com/2024/day/17
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from itertools import batched

#from rich import print # pylint: disable=redefined-builtin

opcodes = { 0: 'adv',
                1: 'bxl',
                2: 'bst',
                3: 'jnz',
                4: 'bxc',
                5: 'out',
                6: 'bdv',
                7: 'cdv'
                }

class ChronospatialComputer:

    def __init__(self, regs, prog):
        self.regs = regs
        self.prog = prog
        self.ip = 0
        self.output = []

    def combo(self, v):
        if 0 <= v <= 3:
            return v
        if v == 4:
            return self.regs['A']
        if v == 5:
            return self.regs['B']
        if v == 6:
            return self.regs['C']
        assert False

    def pp(self):
        print (f'CC: ip={self.ip:2} A:{self.regs['A']:026b} B:{self.regs['B']:026b} C:{self.regs['C']:026b}')

    def execute(self, regA=None, verbose=False, verbose2=False):
        self.ip = 0 
        self.output = []
        if regA is not None:
            self.regs['A'] = regA
        if verbose2:
            self.pp()
        while self.ip < len(self.prog):
            inst,op = self.prog[self.ip],self.prog[self.ip+1]
            if inst == 0:
                if verbose:
                    print (f'ADV({op}): A= {self.regs['A']} // {2 ** self.combo(op)} = {self.regs['A'] // (2 ** self.combo(op))}')
                self.regs['A'] = self.regs['A'] // (2 ** self.combo(op))
            elif inst == 1:
                if verbose:
                    print (f'BXL({op}) B= {self.regs['B']} ^ {op} = {self.regs['B'] ^ op}')
                self.regs['B'] = self.regs['B'] ^ op
            elif inst == 2:
                if verbose:
                    print (f'BST({op}) B= {self.combo(op)} % 8 = {self.combo(op) % 8}')
                self.regs['B'] = self.combo(op) % 8
            elif inst == 3:
                if verbose:
                    print (f'JNZ({op})')
                if self.regs['A'] != 0:
                    self.ip = op
                    if verbose2:
                        print ('-' * 20)
                        self.pp()
                    continue
            elif inst == 4:
                if verbose:
                    print (f'BXC({op}) B= {self.regs['B']} ^ {self.regs['C']} = {self.regs['B'] ^ self.regs['C']}')
                self.regs['B'] = self.regs['B'] ^ self.regs['C']
            elif inst == 5:
                if verbose:
                    print (f'OUT({op}) = {self.combo(op) % 8}')
                self.output.append(self.combo(op) % 8)
            elif inst == 6:
                if verbose:
                    print (f'BDV({op}) B= {self.regs['A']} // {2 ** self.combo(op)} = {self.regs['A'] // (2 ** self.combo(op))}')
                self.regs['B'] = self.regs['A'] // (2 ** self.combo(op))
            elif inst == 7:
                if verbose:
                    print (f'CDV({op}) C= {self.regs['A']} // {2 ** self.combo(op)} = {self.regs['A'] // (2 ** self.combo(op))}')
                self.regs['C'] = self.regs['A'] // (2 ** self.combo(op))
            self.ip += 2
            if verbose:
                print ('-' * 20)
                self.pp()
        
def main(fname) -> None:

    data = fname.read()
    regs = {k:int(v) for k,v in re.findall(r'Register ([ABC]):\s(\S+)',data)}
    prog = list(map(int,re.findall(r'Program:\s(\S+)',data)[0].split(',')))
    cc = ChronospatialComputer(regs, prog)
    cc.execute(verbose=False, verbose2=True)
    cc.pp()
    print (','.join(list(map(str,cc.output))))


    guesses = {k:False for k in list(range(0,1024))}
    plen = len(cc.prog)
    for idx in range(len(cc.prog)+1):
        for reg in guesses.keys():
            cc.execute(reg)
            if cc.prog == cc.output:
                print (f'{reg=} for the win')
                exit()
            #print (f'cc.execute({reg}): {cc.prog[0]} == {cc.output[0]}')
            if len(cc.output) > idx:
                guesses[reg] = all([cc.prog[-i] == cc.output[-i] for i in range(1,idx+2)])
            if (guesses[reg]):
                print (f'execute {reg} --> {cc.output=} {cc.prog=}')

        nextg = {}
        for k,v in guesses.items():
            if v:
                for j in range(0,1024):
                    nextg[(k << 3) ^ j] = False
        print (f'Round {idx} : True Guesses: {sum(guesses.values())} --> Next round: {len(nextg)} ')
        guesses = nextg



if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
