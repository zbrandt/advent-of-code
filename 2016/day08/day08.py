""" Module for Advent of Code Day 8.
    https://adventofcode.com/2016/day/8
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re
import numpy as np

ocr_4x6 =  {0x19297a52:'A', 0x392e4a5c:'B', 0x1928424c:'C', 0x39294a5c:'D', 0x3d0e421e:'E', 0x3d0e4210:'F', 0x19285a4e:'G', 0x252f4a52:'H', 0x1c42108e:'I', 0x0c210a4c:'J', 0x254c5292:'K', 0x2108421e:'L', 0x19294a4c:'O', 0x39297210:'P', 0x39297292:'R', 0x1d08305c:'S', 0x1c421084:'T', 0x25294a4c:'U', 0x23151084:'Y', 0x3c22221e:'Z'}

def main(fname):

    def pp(disp):
        return '\n'.join(''.join((' ','\u2588')[val] for val in row) for row in disp)

    def ocr(disp:np.array):
        return ''.join(ocr_4x6[int(''.join(disp[:,col:col+5].flatten().astype(str)),2)] for col in range(0,disp.shape[1],4+1))

    lines = fname.read().strip().split('\n')
    cmds = [(re.match(r'rect (\d+)x(\d+)', line), re.match(r'rot.* (x|y)=(\d+) by (\d+)', line)) for line in lines]
    cmds = [((np.s_[:int(rect.group(2)), :int(rect.group(1))] if rect else None), ((np.s_[int(rot.group(2)),:], np.s_[:,int(rot.group(2))])[rot.group(1) == 'x'], int(rot.group(3))) if rot else None) for rect, rot in cmds]
    disp = np.zeros([6, 50], dtype=int) if len(cmds) > 10 else np.zeros([3, 7], dtype=int)

    for rect, rot in cmds:
        if rect:
            disp[rect] = 1
        elif rot:
            disp[rot[0]] = np.roll(disp[rot[0]], rot[1])

    print (f'Part 1: {np.sum(disp)}')
    print (f'Part 2: {ocr(disp)}')
    print (pp(disp))

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
