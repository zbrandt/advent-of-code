""" Module for Advent of Code Day 23.
    https://adventofcode.com/2024/day/23
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
from functools import cache

class Graph:
    def __init__(self):
        self.nodes:dict[str,Node] = {}
        self.roots:dict[str,set[Node]] = {}
        self.triplets:set= set()

    def add_pair(self, na, nb):
        #print (f'G:add_pair({na}, {nb})')
        a = self.nodes.get(na, None)
        b = self.nodes.get(nb, None)
        newa = not a
        newb = not b
        #assert newa or newb

        if newa:
            a = Node(na)
            self.nodes[a.name] = a

        if newb:
            b = Node(nb)
            self.nodes[b.name] = b

        if a.parent is None:
            a.parent = na
            self.roots[a.name] = set([a.name])

        if b.parent is None:
            b.parent = nb
            self.roots[b.name] = set([b.name])

        a.peers.add(b.name)
        b.peers.add(a.name)

        triplets = (a.peers & b.peers) - set([a.name, b.name])
        if triplets:
            for t in triplets:
                tab = tuple(sorted([t, na, nb]))
                self.triplets.add(tab)
                #print (f'TRIPLET: {(na,nb)} {tab=} {self.triplets=}')

        self.merge_sets(a.name, b.name)

    @cache # pylint: disable=method-cache-max-size-none
    def grow_doily(self, doily_tuple) -> set:
        doily_set = set(doily_tuple)
        max_doily = doily_set
        candidates = set.intersection(*[self.nodes[n].peers for n in doily_set]) - doily_set
        if len(candidates):
            #print (f'grow_doilies: size={len(doily_set)} ==> {len(candidates)}:{candidates}')
            pass
        for c in candidates:
            md = self.grow_doily(tuple(doily_set | set([c])))
            if len(md) > len(max_doily):
                max_doily = md
        return max_doily

    def merge_sets(self, na, nb):
        a = self.nodes.get(na, None)
        b = self.nodes.get(nb, None)
        pa = self.parent(na)
        pb = self.parent(nb)
        if pa == pb:
            return
        assert pa in self.roots and pb in self.roots
        #print (f'merge_sets: {self=} {na}->{pa}, {nb}->{pb}')
        if len(self.roots[pa]) < len(self.roots[pb]):
            a,b = b,a
            pa,pb = pb,pa
            print (f'swap: {pa=}:{a=} {pb=}{b=}')
        for bnode in self.roots[pb]:
            self.nodes[bnode].parent = pa
        self.roots[pa] = self.roots[pa] | self.roots[pb]
        self.roots.pop(pb)


    def parent(self, name) -> str:
        node = self.nodes[name]
        #print (f'G:parent({name}={node.name}->{node.parent})')
        if not node.parent or node.parent == node.name:
            return node.parent
        return self.parent(node.parent)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Graph(nodes:{len(self.nodes)}, roots:{len(self.roots)}={self.roots})'

class Node:
    def __init__(self, name):
        self.name:str = name
        self.peers:set[str] = set()
        self.parent:str = None
        #print (f'Node({name})')

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Node({self.name})' if self else 'None'

def triple_t(t) -> bool:
    return t[0][0] == 't' or t[1][0] == 't' or t[2][0] == 't'

def main(fname):
    g = Graph()
    max_doily = set()
    data = fname.read()
    edges = re.findall(r'(\w\w)-(\w\w)', data)

    for i,(a,b) in enumerate(edges):
        print (f'add_pair {i+1:4d}/{len(edges)}: ({a},{b}), {max_doily=}', end='\r')
        g.add_pair(a,b)
        doily = g.grow_doily((a,b))
        if len(doily) > len(max_doily):
            max_doily = doily
        print()

    t_triples = [t for t in g.triplets if triple_t(t)]
    print (f'Part 1: {len(t_triples)}')
    print (f'Part 2: {','.join(sorted(list(max_doily)))}')

    print (f'{g=}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
