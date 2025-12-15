""" Module for Advent of Code Day 11.
    https://adventofcode.com/2025/day/11
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from collections import deque
from typing import Callable
class Device:
    name : str
    inputs : list[str]
    outputs : list[str]
    ripe : bool
    counts : dict[str, int]
    deferrals: int

    def __init__(self, line):
        n,o = line.split(':')
        self.name = n.strip()
        self.outputs = o.strip().split()
        self.reset()

    def reset(self):
        self.inputs = []
        self.counts = {}
        self.ripe = False
        self.deferrals = 0

    def __repr__(self):
        return f'{self.name}: {" ".join(self.outputs)}'

    def __str__(self):
        return f'Node {self.name}: Inputs:{" ".join(self.inputs)}, Outputs:{" ".join(self.outputs)}'

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
        self.specials = frozenset(['none', 'dac', 'fft', 'both'])

    def reset(self):
        for d in self.devs.values():
            d.reset()

    def add_device(self, d : Device) -> None:
        self.devs[d.name] = d

    def update_count(self, d : Device) -> None:
        if d == self.root:
            d.ripe = True
            d.counts = { k:0 for k in self.specials }
            d.counts['none'] = 1
        elif all (self.devs[i].ripe for i in d.inputs):
            d.ripe = True
            counts = {k:sum(self.devs[i].counts[k] for i in d.inputs) for k in self.specials}

            if d.name == 'dac':
                counts = {'none':0, 'dac':counts['none'] + counts['dac'], 'fft':0, 'both': counts['both'] + counts['fft'] }
            elif d.name == 'fft':
                counts = {'none':0, 'dac':0, 'fft':counts['none'] + counts['fft'], 'both': counts['both'] + counts['dac'] }

            d.counts = counts

    def make_connects(self) -> None:
        deq = deque(([self.root.name]))
        visited : set[str] = set()
        while deq:
            dev : Device = self.devs[deq.popleft()]
            if dev.name in visited:
                continue
            visited.add(dev.name)
            for out in dev.outputs:
                if out not in self.devs:
                    raise ValueError(f"Unknown device referenced: {out} (from {dev.name})")
                self.devs[out].inputs.append(dev.name)
                deq.append(out)

    def count_paths(self) -> dict[str, int]:
        self.out.counts = { k:0 for k in self.specials }
        self.out.deferrals = 0
        self.out.ripe = False
        deq = deque(([self.root.name]))
        deqset = set([deq[0]])
        while deq:
            dev : Device = self.devs[deq.popleft()]
            deqset.remove(dev.name)
            self.update_count(dev)
            if dev.ripe:
                noutputs = len(dev.outputs)
                if noutputs >= 1:
                    for out in dev.outputs:
                        if out not in deqset:
                            deq.append(out)
                            deqset.add(out)
            else:
                dev.deferrals += 1
                if dev.deferrals > len(self.devs):
                    raise RuntimeError(f"Stuck: {dev.name} never became ripe; inputs={dev.inputs}")
                deq.append(dev.name)
                deqset.add(dev.name)
        if not self.out.ripe:
            raise RuntimeError("Output 'out' was never reached from the root")
        return self.out.counts

    def __repr__(self):
        return "\n".join(f'"{k}":{v}' for k, v in self.devs.items())

def count_paths (r : Reactor, root : str, match : Callable[[str], bool]) -> int:
    count = 0
    r.reset()
    r.root = r.devs.get(root)
    if r.root:
        r.make_connects()
        counts = r.count_paths()
        count = sum(v for k,v in counts.items() if match(k))
    return count

def main(fname):
    r = Reactor(fname)

    parts = [ ('you', lambda k: True), ('svr', lambda k: k == 'both')]

    for i, p in enumerate(parts):
        print (f'Part {i+1}: {count_paths(r, *p)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
