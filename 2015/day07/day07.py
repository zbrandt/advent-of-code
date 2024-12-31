""" Module for Advent of Code Day 7.
    https://adventofcode.com/2015/day/7
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from operator import __xor__, __or__, __and__, __not__, __inv__
from collections import OrderedDict

all_wires:dict = dict()

def __nand__(a, b):
    return __inv__(__and__(a, b))

def __rshift__(a, b):
    return a >> b

def __lshift__(a, b):
    return a << b

class Wire:
    def __init__(self, name, value=None):
        self.name = name
        self.gates = []
        self.value = value
        self.driver = None
    
    def set_value(self, value):
        self.value = value
        for g in self.gates:
            g.set_input(self.name, self.value)
    
    def add_gate(self, gate):
        self.gates.append(gate)
        if self.name in gate.inputs:
            gate.inputs[self.name] = self.value

    def __repr__(self):
        return (f'Wire("{self.name}", {self.value})')
    
class Gate:
    def __init__(self, a, name, b, x):
        dfunc = {
            'AND'   : __and__,
            'NAND'  : __nand__,
            'RSHIFT'  : __rshift__,
            'LSHIFT'  : __lshift__,
            'OR'    : __or__,
            'XOR'  : __xor__
            }

        self.inputs = OrderedDict([(a,None),(b,None)])
        self.output = {x:None}
        self.dirty = False
        self.name = name
        self.unary = a == b
        all_wires[a].add_gate(self)
        all_wires[b].add_gate(self)
        all_wires[x].driver = self
        self.fn = dfunc[self.name]

        self.exec()
    
    def set_input(self, name, value):
        assert name in self.inputs
        if self.inputs[name] != value:
            self.inputs[name] = value
            self.dirty = True
        self.exec()

    def exec(self):
        (k,v), *_ = self.output.items()
        if v is None or self.dirty:
            vals = self.inputs.values()
            #print (f'Gate:exec: {self.fn.__name__} {vals=}')
            if all(x is not None for x in vals):
                if self.unary:
                    vals = [list(vals)[0], list(vals)[0]]
                #print (f'Gate:exec: {vals=} {self.fn.__name__}')
                v = self.fn(*vals) & 0xFFFF
                self.output[k] = v
                self.dirty = False
                #print (f'Gate:exec: {self.inputs.items()=} {self.fn.__name__} ==> {v}')
                all_wires[k].set_value(v)

    def __repr__(self):
        if self.unary:
            (a, av), *_ = self.inputs.items()
            b = a
            bv = av
        else:
            (a, av), (b, bv), *_ = self.inputs.items()
        (x,xv), *_ = self.output.items()
        return (f'Gate("{a}", "{self.fn.__name__}", {b}", "{x}")')

def add_wires(wires):
    for w in wires:
        if w not in all_wires:
            all_wires[w] = Wire(w)

def main(fname):
    data = fname.read()
    lines = data.strip().split('\n')
    for line in lines:
        m = re.match(r'^([a-z]+|[0-9]+) -> ([a-z]+)$', line)
        if m:
            arg1, output = m.group(1), m.group(2)
            #print (f'set: {arg1} --> {output}')            
            if arg1.isdigit():
                w = all_wires.get(output, None)
                if w is None:
                    w = Wire(output, int(arg1))
                    all_wires[w.name] = w
                else:
                    w.set_value(int(arg1))
                continue
            oper = 'OR'
            arg2 = arg1

        if m is None:
            m = re.match(r'^(NOT) ([a-z]+) -> ([a-z]+)$', line)
            if m:
                oper, arg1, output = m.group(1), m.group(2), m.group(3)
                arg2 = arg1
                oper = 'NAND'

        if m is None:
            m = re.match(r'^([a-z]+|[0-9]+) ([A-Z]+) ([a-z]+|[0-9]+) -> ([a-z]+)$', line)
            if m:
                arg1, oper, arg2, output = m.group(1), m.group(2), m.group(3), m.group(4)

        if m is None:
            print (line)
            assert False

        if m:
            if arg1.isdigit():
                name = 'wire'+arg1
                if name not in all_wires:
                    w = Wire(name, int(arg1))
                    all_wires[w.name] = w
                arg1 = name

            if arg2.isdigit():
                name = 'wire'+arg2
                if name not in all_wires:
                    w = Wire(name, int(arg2))
                    all_wires[w.name] = w
                arg2 = name

            #print (f'binary: {arg1} {oper} {arg2} --> {output}')
            add_wires([arg1, arg2, output])
            Gate(arg1, oper, arg2, output)

    print (f'Part 1: {all_wires['a'].value}')
    a_val = all_wires['a'].value
    for k,v in all_wires.items():
        if k[0:4] == 'wire':
            continue
        if k == 'b':
            v.set_value(a_val)
    print (f'Part 2: {all_wires['a'].value}')

    exit()

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)