""" Module for Advent of Code Day 21.
    https://adventofcode.com/2016/day/21
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re

def main(fname):

    lines = [l.strip() for l in fname.readlines()]
    passwd = ('abcde','abcdefgh')[len(lines) > 40]

    for l in lines:
        m1 = re.match(r'swap position (\d) with position (\d)', l)
        m2 = re.match(r'swap letter (\w) with letter (\w)', l)
        m3 = re.match(r'rotate (left|right) (\d) steps?', l)
        m4 = re.match(r'rotate based on position of letter (\w)', l)
        m5 = re.match(r'reverse positions (\d) through (\d)', l)
        m6 = re.match(r'move position (\d) to position (\d)', l)
        ms = [m1, m2, m3, m4, m5, m6]
        assert any(list(map(bool,ms)))

        if m1:
            a,b = sorted(list(map(int, m1.group(1,2))))
            xpasswd = passwd[:a] + passwd[b] + passwd[a+1:b] + passwd[a] + passwd[b+1:]
            print (f'swap position: {a} <--> {b}. {passwd} -> {xpasswd}')
        elif m2:
            a,b = sorted(list(map(passwd.index, m2.group(1,2))))
            xpasswd = passwd[:a] + passwd[b] + passwd[a+1:b] + passwd[a] + passwd[b+1:]
            print (f'swap chars: {m2.group(1,2)} ==> {a} <--> {b}. {passwd} -> {xpasswd}')
        elif m3:
            b = int(m3.group(2)) * (1,-1)[m3.group(1) == 'right']
            xpasswd = passwd[b:] + passwd[:b]
            print (f'rotate {m3.group(1)}: {b} step: {passwd} -> {xpasswd}')
        elif m4:
            a = passwd.index(m4.group(1))
            b = (a+1 + bool(a >= 4)) % len(passwd)
            xpasswd = passwd[-b:] + passwd[:-b]
            print (f'rotate by {m4.group(1)}, index:{a} -> steps:{b}. {passwd} -> {xpasswd}')
        elif m5:
            a,b = list(map(int, m5.group(1,2)))
            xpasswd = passwd[:a] + passwd[a:b+1][::-1] + passwd[b+1:]
            print (f'reverse positions: {a} - {b}. {passwd} -> {xpasswd}')
        elif m6:
            x,y = list(map(int, m6.group(1,2)))
            ch,xpasswd = passwd[x], passwd[:x]+passwd[x+1:]
            xpasswd = xpasswd[:y] + ch + xpasswd[y:]
            print (f'move position: {x} -> {y}. {ch=}. {passwd} -> {xpasswd}')
        else:
            print (l, list(map(bool,ms)))
            exit()
        #print ('-' * 50)
        passwd = xpasswd

    #print (passwd)

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
