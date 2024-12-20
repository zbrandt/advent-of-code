""" Module for Advent of Code Day 17.
    https://adventofcode.com/2024/day/17
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from itertools import batched
from time import sleep

from rich import print as rprint # pylint: disable=redefined-builtin

def fmtbits(val, width, bknown, bempty):
    bempty = max(bempty,bknown)
    bknown = width - bknown
    bempty = width - bempty
    x = f'{val:0{width}b}'
    rx = '[bold]' + x[:bempty] + '[/][green]' + x[bempty:bknown] + '[/][blue]' + x[bknown:]
    return rx

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
    print ('-' * 20)
    cc.pp()
    print ('-' * 20)
    print (f'Part 1: {",".join(list(map(str,cc.output)))}')
    print ('=' * 20)


    shift_amt = 3
    base=1024
    guesses = {k:False for k in list(range(0,base))}
    for idx in range(len(cc.prog)+1):
        for j,reg in enumerate(guesses.keys()):
            cc.execute(reg)
            if cc.prog == cc.output:
                print (f'\nPart 2: {reg:x} --> {reg}')
                exit()
            #print (f'cc.execute({reg}): {cc.prog} == {cc.output}')
            
            rprint (f'Guess: {fmtbits(reg, 48, 10, 3 * idx + 10)}  {j:5}/({len(guesses)//base}*base)', end='\r')
            if len(cc.output) > idx:
                guesses[reg] = all([cc.prog[-i] == cc.output[-i] for i in range(1,idx+2)])
            #print (f'execute {reg} --> {guesses[reg]} --> {cc.output=} {cc.prog=}')
            if (guesses[reg]):
                #print (f'execute {reg} --> guesses[reg] --> {cc.output=} {cc.prog=}')
                pass
            #sleep(0.01)

        nextg = {}
        mink,maxk = None, None
        for k,v in guesses.items():
            if v:
                mink = [mink,k][mink is None or mink > k]
                maxk = [maxk,k][maxk is None or maxk < k]

        for k,v in guesses.items():
            if v:
                for j in range(0,1024):
                    nextg[(k << shift_amt) ^ j] = False
        rprint (f' ' * 80, end='\r')
        print (f'Round {idx} : True Guesses: {sum(guesses.values())} {mink=:x} {maxk=:x} --> Next round: {len(nextg)} ')
        guesses = nextg



if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
