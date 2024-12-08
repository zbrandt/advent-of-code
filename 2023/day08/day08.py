import sys
import re
import math

class Node:
    def __init__(self, mapline) -> None:
        m = re.match(r'(\w+)\s*\=\s*\((\w+),\s*(\w+)\)', mapline)
        #m = re.match(r'(\w+) = \((\w+), (\w+)\)', mapline)
        self.node = None
        self.left = None
        self.right = None
        if m:
            self.node = m.groups()[0]
            self.left = m.groups()[1]
            self.right = m.groups()[2]

def loop_length(nodes, node, instructions) -> int:
    steps = 0
    while node.node[-1] != 'Z':
        new_node = node
        lr = instructions[steps % len(instructions)]
        if lr == 'L':
            new_node = nodes[node.left]
        elif lr == 'R':
            new_node = nodes[node.right]
        else:
            assert False
        steps += 1
        #print (f'{steps=}: {node.node} --> {lr} --> {new_node.node}')
        node = new_node
    #print (f'{steps=}')
    return (steps)

instructions = input()
nodes = {}
first = None
threads = []
for line in sys.stdin:
    n:Node = Node(line)
    if n.node:
        nodes[n.node] = n
        if first is None:
            first = n
        if n.node[-1] == 'A':
            threads.append(n)

if False:
    node = nodes.get('AAA', first)
    steps = 0
    while node.node[-1] != 'Z':
        new_node = node
        lr = instructions[steps % len(instructions)]
        if lr == 'L':
            new_node = nodes[node.left]
        elif lr == 'R':
            new_node = nodes[node.right]
        else:
            assert False
        steps += 1
        print (f'{steps=}: {node.node} --> {lr} --> {new_node.node}')
        node = new_node
    print (f'{steps=}')

    print ('2' * 80)

thread_lengths = []
for t in threads:
    thread_lengths.append(loop_length(nodes, t, instructions))
    print (f'{len(thread_lengths)} {t.node} {thread_lengths[-1]}')
print (f'{thread_lengths=}')
print (f'{math.lcm(*thread_lengths)=}')
exit()

steps = 0
allz = False
zcount = 0
thread_count = len(threads)
while zcount != thread_count:
    allz = True
    lr = instructions[steps % len(instructions)]
    print (f'{len(threads)} {steps=} {lr=} {[x.node for x in threads]} {zcount=}')
    if lr == 'L':
        for i in range(thread_count):
            threads[i] = nodes[threads[i].left]
            allz &= threads[i].node[-1] == 'Z'
    elif lr == 'R':
        for i in range(thread_count):
            threads[i] = nodes[threads[i].right]
            allz &= threads[i].node[-1] == 'Z'
    else:
        assert False
    zcount = sum([x.node[-1] == 'Z' for x in threads])
    steps += 1

print (f'{len(threads)} {steps=} {lr=} {[x.node for x in threads]} {zcount=}')
print (f'{steps=}')

