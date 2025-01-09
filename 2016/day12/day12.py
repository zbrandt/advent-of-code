""" Module for Advent of Code Day 11.
    https://adventofcode.com/2016/day/11
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys

def typeify(s):
    return s if s.isalpha() else int(s)

def execute(program, regc = 0):
    ip = 0
    regs = [0] * 4
    regs[2] = regc

    def read_op(op) -> int:
        return op if isinstance(op, int) else regs[ord(op) - ord('a')]

    def write_op(op, val) -> None:
        regs[ord(op) - ord('a')] = val

    while ip < len(program):
        inst, *op = program[ip]
        src = read_op(op[0])
        match inst:
            case 'cpy':
                write_op(op[1], src)
            case 'inc':
                write_op(op[0], src + 1)
            case 'dec':
                write_op(op[0], src - 1)
            case 'jnz':
                ip = ip - 1 + read_op(op[1]) if src else ip
        ip += 1
    return regs[0]

def main(fname):
    program = [[typeify(w) for w in line.split()] for line in fname.readlines()]
    for i in [0,1]:
        print (f'Part {i+1}: {execute(program, i)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
