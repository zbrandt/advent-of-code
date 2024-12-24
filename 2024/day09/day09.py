""" Module for Advent of Code Day 9.
    https://adventofcode.com/2024/day/9
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

BASE_BIG:int=0x4E01
BASE_SMALL:int=ord('0')

def main(fname) -> None:

    def pp(disk):
        if base_ch != BASE_SMALL:
            x = (''.join(disk).replace('.', chr(base_ch-1)))
        else:
            x = (''.join(disk))
        print (f'{x:.80s}')

    def compact1(disk: str) -> str:
        ldisk:list[str] = list(disk)
        i, j = 0, len(ldisk)-1
        while True:
            while ldisk[j] =='.':
                j -= 1
            while ldisk[i] != '.':
                i += 1
            if i >= j:
                break
            ldisk[i], ldisk[j] = ldisk[j], ldisk[i]
        return ''.join(ldisk)

    def compact2(disk: str):
        pos, blocks, spaces = 0, [], []
        for block, _, space in re.findall(r'(([^\.])\2*)(\.*)', disk):
            blocks.append((pos, len(block), block[0]))
            pos += len(block)
            spaces.append((pos, len(space), '.'))
            pos += len(space)

        ldisk = list(disk)
        for b, block in enumerate(reversed(blocks)):
            for s,space in enumerate(spaces):
                if block[0] <= space[0]:
                    break
                if block[1] <= space[1]:
                    for i in range(block[1]):
                        ldisk[space[0] + i], ldisk[block[0] +i ] = block[2], '.'
                    spaces[s] = (space[0] + block[1], space[1]-block[1], '.')
                    #print (f'move block {b}:{block} to space {s}:{space}. New space: {spaces[s]}')
                    break
        return ''.join(ldisk)

    def compute_checksum(disk: str) -> int:
        return sum(i*(ord(ch)-base_ch) for i,ch in enumerate(disk) if ch != '.')

    nums = list(map(int,list(fname.read().strip())))
    base_ch = (BASE_SMALL, BASE_BIG)[len(nums) > 26]
    disk = ''.join([(chr(base_ch+i//2),'.')[i&1] * nums[i] for i in range(len(nums))])

    disk1 = compact1(disk)
    checksum1 = compute_checksum(disk1)
    print (f'Part 1: {checksum1}')

    disk2 = compact2(disk)
    checksum2 = compute_checksum(disk2)
    print (f'Part 2: {checksum2}')


if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
