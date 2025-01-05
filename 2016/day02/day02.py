""" Module for Advent of Code Day 2.
    https://adventofcode.com/2016/day/2
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys

keypads = [
"""
123
456
789
""",
"""
  1  
 234 
56789
 ABC 
  D  
""" ]

dirs = dict(zip('LURD',[-1j**i for i in range(4)]))

def create_keypad(i, pads):
    rows = [ row for row in pads[i].split('\n') if row ]
    pad = {x+y*1j:ch for y,line in enumerate(rows) for x,ch in enumerate(line) if ch != ' '}
    dap = {v:k for k,v in pad.items()}
    return pad, dap

def walk(keypad, pos, moves):
    for m in moves:
        pos = (pos, pos + m)[pos + m in keypad]
        yield pos

def main(fname):
    moves = [[dirs[ch] for ch in line] for line in fname.read().strip().split('\n')]
    for i in range(2):
        keypad, dapyek = create_keypad(i, keypads)
        pos = dapyek['5']
        code = ''.join(keypad[pos := [x for x in walk(keypad, pos, row)][-1]] for row in moves)
        print (f'Part {i+1}: {code}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
