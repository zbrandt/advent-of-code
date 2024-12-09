""" Module for Advent of Code Day 9.
    https://adventofcode.com/2024/day/9
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

def main(fname) -> None:

    base_ch:int=0x4E01
    #base_ch:int=ord('0')

    def pp(disk):
        if base_ch != ord('0'):
            print(''.join(disk).replace('.', chr(base_ch-1)))
        else:
            print(''.join(disk))

    def compact1(disk: str):
        disk = list(disk)
        i, j = 0, len(disk)-1
        while True:
            while disk[j] =='.':
                j -= 1
            while disk[i] != '.':
                i += 1
            if i >= j:
                break
            disk[i], disk[j] = disk[j], disk[i]
        return ''.join(disk)

    def compact2(disk: str):
        pos, blocks, spaces = 0, [], []
        for block, _, space in re.findall(r'(([^\.])\2*)(\.*)', disk):
            blocks.append((pos, len(block), block[0]))
            pos += len(block)
            spaces.append((pos, len(space), '.'))
            pos += len(space)

        disk = list(disk)
        for b, block in enumerate(reversed(blocks)):
            for s,space in enumerate(spaces):
                if block[0] <= space[0]:
                    break
                if block[1] <= space[1]:
                    for i in range(block[1]):
                        disk[space[0] + i], disk[block[0] +i ] = block[2], '.'
                    spaces[s] = (space[0] + block[1], space[1]-block[1], '.')
                    #print (f'move block {b}:{block} to space {s}:{space}. New space: {spaces[s]}')
                    break
        return ''.join(disk)

    def compute_checksum(disk: str) -> int:
        return sum(i*(ord(ch)-base_ch) for i,ch in enumerate(disk) if ch != '.')

    nums = list(map(int,list(fname.read().strip())))
    disk = ''.join([(chr(base_ch+i//2),'.')[i&1] * nums[i] for i in range(len(nums))])

    disk1 = compact1(disk)
    checksum1 = compute_checksum(disk1)
    print (f'Part 1: {checksum1}')

    disk2 = compact2(disk)
    checksum2 = compute_checksum(disk2)
    print (f'Part 2: {checksum2}')


if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
