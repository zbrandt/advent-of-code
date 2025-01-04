""" Module for Advent of Code Day 23.
    https://adventofcode.com/2015/day/23
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

class TuringLock:
    def __init__(self, prog):
        self.reg = {'a':0, 'b':0}
        self.ip:int = 0
        self.prog:list[tuple[str]] = prog

    def execute(self, a=0, b=0):
        self.ip = 0
        self.reg =  {'a':a, 'b':b}
        while self.ip < len(self.prog):
            inst,op1,op2 = self.prog[self.ip]
            match inst:
                case 'hlf':
                    self.reg[op1] //= 2
                case 'tpl':
                    self.reg[op1] *= 3
                case 'inc':
                    self.reg[op1] += 1
                case 'jmp':
                    self.ip += (int(op1) - 1) * 1
                case 'jie':
                    self.ip += (int(op2) - 1) * (self.reg[op1] & 1 ^ 1)
                case 'jio':
                    self.ip += (int(op2) - 1) * int(self.reg[op1] == 1)
                case _:
                    assert False
            self.ip += 1

    def __str__(self):
        return f'TuringLock(reg={self.reg}, ip={self.ip}, len(prog)={len(self.prog)})'

def main(fname):
    program = re.findall(r'(?m)^(\S+)\s(\S+)(?:, (\S+))?$', fname.read())

    tl = TuringLock(program)
    for i in range(2):
        tl.execute(a=i, b=0)
        print (f'Part {i+1}: {tl.reg['b']}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
