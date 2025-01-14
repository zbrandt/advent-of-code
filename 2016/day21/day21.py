""" Module for Advent of Code Day 21.
    https://adventofcode.com/2016/day/21
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring, redefined-builtin
import sys
import re

def inv_rotate_by(wdssapx, x) -> str:
    pwds = [wdssapx[b:] + wdssapx[:b] for b in range(len(wdssapx))]
    matches = []
    for passwd in pwds:
        a = passwd.index(x)
        b = (a+1 + bool(a >= 4)) % len(passwd)
        xpasswd = passwd[-b:] + passwd[:-b]
        if xpasswd == wdssapx:
            matches.append(passwd)
    if len(matches) != 1:
        print (f'inv_rotate_by: ALERT!!! {len(matches)} solutions: {matches}')
    #assert matches[0] == matches[-1]
    return matches[0]

def do_step (i, inst, passwd, inv, verbose=False) -> str:
    l = inst
    m1 = re.match(r'swap position (\d) with position (\d)', l)
    m2 = re.match(r'swap letter (\w) with letter (\w)', l)
    m3 = re.match(r'rotate (left|right) (\d) steps?', l)
    m4 = re.match(r'rotate based on position of letter (\w)', l)
    m5 = re.match(r'reverse positions (\d) through (\d)', l)
    m6 = re.match(r'move position (\d) to position (\d)', l)
    ms = [m1, m2, m3, m4, m5, m6]
    assert any(list(map(bool,ms)))

    if verbose:
        print (f'{i+1:3d}. {('    ','INV ')[inv]}', end='')
    if m1:
        a,b = sorted(list(map(int, m1.group(1,2))))
        xpasswd = passwd[:a] + passwd[b] + passwd[a+1:b] + passwd[a] + passwd[b+1:]
        if verbose:
            print (f'swap position: {a} <--> {b}. {passwd} -> {xpasswd}')
    elif m2:
        a,b = sorted(list(map(passwd.index, m2.group(1,2))))
        xpasswd = passwd[:a] + passwd[b] + passwd[a+1:b] + passwd[a] + passwd[b+1:]
        if verbose:
            print (f'swap chars: {m2.group(1,2)} ==> {a} <--> {b}. {passwd} -> {xpasswd}')
    elif m3:
        b = int(m3.group(2)) * (1,-1)[(m3.group(1) == 'right') != inv]
        xpasswd = passwd[b:] + passwd[:b]
        if verbose:
            print (f'rotate {m3.group(1)}: {b} step: {passwd} -> {xpasswd}')
    elif m4:
        if not inv:
            a = passwd.index(m4.group(1))
            b = (a+1 + bool(a >= 4)) % len(passwd)
            xpasswd = passwd[-b:] + passwd[:-b]
        else:
            xpasswd = inv_rotate_by(passwd, m4.group(1))
            a = xpasswd.index(m4.group(1))
            b = (a+1 + bool(a >= 4)) % len(xpasswd)
        if verbose:
            print (f'rotate by {m4.group(1)}, index:{a} -> steps:{b}. {passwd} -> {xpasswd}')
    elif m5:
        a,b = list(map(int, m5.group(1,2)))
        xpasswd = passwd[:a] + passwd[a:b+1][::-1] + passwd[b+1:]
        if verbose:
            print (f'reverse positions: {a} - {b}. {passwd} -> {xpasswd}')
    elif m6:
        x,y = list(map(int, m6.group(1,2)))
        if inv:
            x,y = y,x
        ch,xpasswd = passwd[x], passwd[:x]+passwd[x+1:]
        xpasswd = xpasswd[:y] + ch + xpasswd[y:]
        if verbose:
            print (f'move position: {x} -> {y}. {ch=}. {passwd} -> {xpasswd}')
    else:
        print (f'{l=}', list(map(bool,ms)))
        assert False

    if verbose:
        print ('-' * 50)
    passwd = xpasswd
    return passwd

def main(fname):
    verbose = False
    lines = [l.strip() for l in fname.readlines()]

    if len(lines) < 10:
        for i,inst in enumerate(lines):
            passwd = do_step(i, inst, 'abcde', False, True)
        print (f'Sample: {passwd}')
        return

    for part, passwd, step in ((1, 'abcdefgh', 1), (2, 'fbgdceah', -1)):
        for i,inst in enumerate(lines[::step]):
            passwd = do_step(i, inst, passwd, step == -1, verbose)
        print (f'Part {part}: {passwd}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
