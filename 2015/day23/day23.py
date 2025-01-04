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

    def execute(self):
        self.ip = 0
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
    data = fname.read().strip()
    program = [(inst, op1, op2) for inst, op1, op2 in re.findall(r'(?m)^(\S+)\s(\S+)(?:, (\S+))?$', data)]

    tl = TuringLock(program)
    for i in range(2):
        tl.reg = {'a':i, 'b':0}
        tl.execute()
        print (f'Part {i+1}: {tl.reg['b']} -- {tl}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
