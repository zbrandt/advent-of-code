""" Module for Advent of Code Day 24.
    https://adventofcode.com/2024/day/24
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from operator import __xor__, __or__, __and__
from collections import OrderedDict

all_wires:dict = dict()


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
        dfunc = {'AND': __and__, 'OR': __or__, 'XOR': __xor__}

        self.inputs = OrderedDict([(a,None),(b,None)])
        self.output = {x:None}
        self.name = name
        all_wires[a].add_gate(self)
        all_wires[b].add_gate(self)
        all_wires[x].driver = self
        self.fn = dfunc[self.name]

        self.exec()
    
    def set_input(self, name, value):
        assert name in self.inputs
        self.inputs[name] = value
        self.exec()

    def exec(self):
        (k,v), *_ = self.output.items()
        if v is None:
            vals = self.inputs.values()
            if all(x is not None for x in vals):
                v = self.fn(*vals)
                self.output[k] = v
                #print (f'Gate:exec: {self.inputs.items()=} {self.fn.__name__} ==> {v}')
                all_wires[k].set_value(v)

    def __repr__(self):
        (a, av), (b, bv), *_ = self.inputs.items()
        (x,xv), *_ = self.output.items()
        return (f'Gate("{a}", "{self.fn.__name__}", {b}", "{x}")')

def add_wires(wires):
    for w in wires:
        if w not in all_wires:
            all_wires[w] = Wire(w)

def check_adder(a, b, z, cin=True, cout=True) -> bool:
    wa = all_wires[a]
    wb = all_wires[b]

    wa.gates = sorted(wa.gates, key=lambda x: x.name)
    wb.gates = sorted(wb.gates, key=lambda x: x.name)

    if len(wa.gates) != 2:
        print (f'check_adder({a}, {b}): A wire {a} does not see two gates {[g.name for g in wa.gates]}')
        return False

    if len(wb.gates) != 2:
        print (f'check_adder({a}, {b}): B wire {b} does not see two gates  {[g.name for g in wb.gates]}')
        return False

    if wa.gates[0] != wb.gates[0] or wa.gates[1] != wb.gates[1]:
        print (f'check_adder({a}, {b}): Wires A & B do not see the same two gates')
        return False

    gand1:Gate = wa.gates[0]
    gxor1:Gate = wa.gates[1]
    if gand1.name != 'AND' or gxor1.name != 'XOR':
        print (f'check_adder({a}, {b}):  Wires A,B do not see AND and XOR gates')
        return False
    
    wxor1 = all_wires[list(gxor1.output)[0]]
    wxor1.gates = sorted(wxor1.gates, key=lambda x: x.name)

    wand1 = all_wires[list(gand1.output)[0]]
    wand1.gates = sorted(wand1.gates, key=lambda x: x.name)

    gor1 = None
    gand2 = None
    gxor2 = None
    if cin:
        if len(wxor1.gates) != 2:
            print (f'check_adder({a}, {b}): XOR1 wire "{wxor1.name}" does not see 2 gates {[g.name for g in wxor1.gates]}')
            #return False
        else:
            gand2 = wxor1.gates[0]
            gxor2 = wxor1.gates[1]
            assert gand2.name == 'AND' and gxor2.name == 'XOR'

        gor1 = None
        if len(wand1.gates) != 1:
            print (f'check_adder({a}, {b}): AND1 wire "{wand1.name}" does not see one gate {[g.name for g in wand1.gates]}')
            #return False
        else:
            gor1 = wand1.gates[0]
            assert gor1.name == 'OR'

    else:
        if wxor1.name != z:
            print (f'check_adder({a}, {b}): XOR1 wire "{wxor1.name}" does not match Z wire "{z}"')
            #return False


    if gxor2:
        wxor2 = all_wires[list(gxor2.output)[0]]
        if wxor2.name != z:
            print (f'check_adder({a}, {b}): XOR2 wire "{wxor2.name}" does not match Z wire "{z}"')

        if len(wand1.gates) != 1:
            print (f'check_adder({a}, {b}): AND1 wire "{wand1.name}" does not see one gate {[g.name for g in wand1.gates]}')
            #return False

    #if gand2 and cout:

    if gor1 and cout:
        wor1 = all_wires[list(gor1.output)[0]]
        if len(wor1.gates) != 2:
            print (f'check_adder({a}, {b}): OR1 wire "{wor1.name}" does not see 2 gates {[g.name for g in wor1.gates]}')

    return True

def swap_outputs(a, b):
    wa = all_wires[a]
    wb = all_wires[b]

    assert wa.driver and wb.driver
    wa.driver.output = {wb.name:wb.value}
    wb.driver.output = {wa.name:wa.value}

def main(fname):
    data = fname.read()
    for name, value in re.findall(r'(\w+):\s*([01])', data):
        w = Wire(name, int(value))
        all_wires[w.name] = w

    #print(all_wires)

    for a,fn,b,x in re.findall(r'(\w+) (\w+) (\w+) -> (\w+)', data):
        add_wires([a,b,x])
        g = Gate(a, fn, b, x)
    
    #print (sorted([(k,v) for k,v in all_wires.items() if k[0] == 'z']))
    zwires = [p[1].value for p in sorted([(k,v) for k,v in all_wires.items() if k[0] == 'z'])]
    zwires_int = sum([b*(1<<i) for i,b in enumerate(zwires)])
    print (f'Part 1: {zwires_int}')

    swaps = []
    #swaps = [('z07', 'gmt'), ('z18', 'dmn'), ('qjj', 'cbj'), ('cfk', 'z35')]
    sorted_swaps = []
    for s in swaps:
        swap_outputs(s[0], s[1])
        sorted_swaps.extend(list(s))
    sorted_swaps = sorted(sorted_swaps)
    print (f'Part 2: {','.join(sorted_swaps)}')

    bit_width = 45
    for i in range(bit_width):
        name = f'{i:02d}'
        chk = check_adder('x'+name, 'y'+name, 'z'+name, i != 0, i != bit_width-1)

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
