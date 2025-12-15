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
    counts : dict[str, int]

    def __init__(self, line):
        n,o = line.split(':')
        self.name = n.strip()
        self.outputs = o.strip().split()
        self.reset()

    def reset(self):
        self.inputs = []
        self.counts = {}

    def __repr__(self):
        return f'{self.name}: {" ".join(self.outputs)}'

    def __str__(self):
        return f'Node {self.name}: Inputs:{" ".join(self.inputs)}, Outputs:{" ".join(self.outputs)}'

class Reactor:
    devs : dict[str, Device]
    out : Device
    root : Device
    specials : frozenset[str]

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
            d.counts = { k:0 for k in self.specials }
            d.counts['none'] = 1
            return

        counts = {k:sum(self.devs[i].counts[k] for i in d.inputs) for k in self.specials}

        if d.name == 'dac':
            counts = {'none':0, 'dac':counts['none'] + counts['dac'], 'fft':0, 'both': counts['both'] + counts['fft'] }
        elif d.name == 'fft':
            counts = {'none':0, 'dac':0, 'fft':counts['none'] + counts['fft'], 'both': counts['both'] + counts['dac'] }

        d.counts = counts

    def make_connects(self) -> None:
        self.reset()
        deq = deque(([self.root.name]))
        visited : set[str] = set()
        while deq:
            dev : Device = self.devs[deq.popleft()]
            if dev.name in visited:
                continue
            visited.add(dev.name)
            for child in dev.outputs:
                if child not in self.devs:
                    raise ValueError(f"Unknown device referenced: {child} (from {dev.name})")
                self.devs[child].inputs.append(dev.name)
                deq.append(child)

    def reachable(self, root_name) -> set[str]:
        reachable = set()
        deq = deque(([root_name]))
        while deq:
            name = deq.popleft()
            if name in self.devs and name not in reachable:
                reachable.add(name)
                for child in self.devs[name].outputs:
                    if child in self.devs:
                        deq.append(child)
        
        return reachable
    
    def count_paths_kahn(self, root) -> dict[str, int]:
        reach = self.reachable(root)
        if 'out' not in reach:
            raise RuntimeError("Output 'out' is not reachable from the root")

        self.out.counts = { k:0 for k in self.specials }
 
        indeg = {name: len(self.devs[name].inputs) for name in reach}
        q = deque(([root]))

        processed = 0
        while q:
            u = q.popleft()
            processed += 1
            self.update_count(self.devs[u])
                              
            for v in self.devs[u].outputs:
                if v not in reach:
                    continue
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        
        if processed != len(reach):
            raise RuntimeError("Cycle or unresolved dependencies in reachable subgraph")
        
        return self.out.counts

    def __repr__(self):
        return "\n".join(f'"{k}":{v}' for k, v in self.devs.items())

def count_paths (r : Reactor, root : str, match : Callable[[str], bool]) -> int:
    count = 0
    r.root = r.devs.get(root)
    if r.root:
        r.make_connects()
        counts = r.count_paths_kahn(root)
        count = sum(v for k,v in counts.items() if match(k))
    return count

def main(fname):
    r = Reactor(fname)

    parts = [ ('you', lambda k: True), ('svr', lambda k: k == 'both')]

    for i, p in enumerate(parts):
        print (f'Part {i+1}: {count_paths(r, *p)}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
