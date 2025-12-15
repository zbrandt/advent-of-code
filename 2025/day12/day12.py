""" Module for Advent of Code Day 10.
    https://adventofcode.com/2025/day/10
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
from ast import literal_eval
import sys
from collections import deque, Counter
from itertools import combinations
from functools import reduce
import operator

class Device:
    name : str
    inputs : list[str]
    outputs : list[str]
    ripe : bool
    counts : dict[str, int]

    def __init__(self, line):
        n,o = line.split(':')
        self.name = n.strip()
        self.outputs = o.strip().split()
        self.reset()

    def reset(self):
        self.inputs = []
        self.counts = {}
        self.ripe = False

    def __repr__(self):
        return f'{self.name}: {' '.join(self.outputs)}' 

    def __str__(self):
        return f'Node {self.name}: Inputs:{' '.join(self.inputs)}, Outputs:{' '.join(self.outputs)}' 

class Reactor:
    devs : dict[str, Device]
    out : Device
    root : Device
    specials : set[str]

    def __init__(self, fname):
        self.devs = { d.name: d for d in [Device(line) for line in fname.readlines()]} 
        self.out = Device('out:')
        self.root : Device = None
        self.add_device(self.out)
        self.specials = set(['any', 'dac', 'fft', 'both'])

    def you(self):
        if 'you' in self.devs:
            return self.devs['you']
        return None

    def svr(self):
        if 'svr' in self.devs:
            return self.devs['svr']
        return None

    def reset(self):
        for d in self.devs.values():
            d.reset()

    def add_device(self, d : Device) -> None:
        self.devs[d.name] = d

    def update_count(self, d : Device) -> None:
        if d == self.root:
            d.ripe = True
            d.counts = { k:(0,1)[k == 'any'] for k in self.specials }
        elif all (self.devs[i].ripe for i in d.inputs):
            d.ripe = True
            d.counts = { k:sum(self.devs[i].counts[k] for i in d.inputs) for k in self.specials}
            if d.name == 'fft':
                d.counts['fft'] = d.counts['any']
                d.counts['both'] += d.counts['dac']
            elif d.name == 'dac':
                d.counts['dac'] = d.counts['dac']
                d.counts['both'] += d.counts['fft']

    def make_connects(self) -> None:
        deq = deque(([self.root.name]))
        visited : set[Device] = set()
        while deq:
            dev : Device = self.devs[deq.popleft()]
            if dev in visited:
                continue
            visited.add(dev)
            for out in dev.outputs:
                self.devs[out].inputs.append(dev.name)
                deq.append(out)

    def count_paths(self) -> int:
        self.root.count = 1
        deq = deque(([self.root.name]))
        while deq:
            dev : Device = self.devs[deq.popleft()]
            self.update_count(dev)
            if dev.ripe:
                noutputs = len(dev.outputs)
                if noutputs >= 1:
                    for out in dev.outputs:
                        if out not in deq:
                            deq.append(out)
            else:
                deq.append(dev.name)
        return self.out.counts

    def __repr__(self):
        return f'{'\n'.join('"'+str(k)+'":'+str(v) for k,v in self.devs.items())}'


def main(fname):
    p1 = p2 = 0
    r = Reactor(fname)

    if True:
        r.root = r.devs.get('you', None)
        if r.root:
            r.make_connects()
            #print (f'Part 1 Connected Graph:\n{str(r)}')
            p1 = r.count_paths()['any']
            print (f'Part 1: {p1}')

    r.reset()
    r.root = r.devs.get('svr', None)
    if r.root:
        r.make_connects()
        #print (f'Part 2 Connected Graph:\n{str(r)}')
        p2 = r.count_paths()['both']
        print (f'Part 2: {p2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
