""" Module for Advent of Code Day 22.
    https://adventofcode.com/2024/day/22
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
from functools import cache
from collections import defaultdict

@cache
def next_secret(secret):
    secret = (secret ^ (secret * 64)) % 16777216
    secret = (secret ^ (secret // 32)) % 16777216
    secret = (secret ^ (secret * 2048)) % 16777216
    return secret

@cache
def nth_secret(secret, n):
    while n:
        secret = next_secret(secret)
        n -= 1
    return secret

sumdbseq = defaultdict(int)
alldbseq = {}

def buyer_sig (idx, secret, count, window):
    dbseq = defaultdict(int)

    i = window+1
    sec_n = [nth_secret(secret, i) for i in range(window+1)]
    mod_n = [sec % 10 for sec in sec_n]
    dlt_n = [1<<11]+[mod_n[i] - mod_n[i-1] for i in range(1, window+1)]
    dtuple = tuple(dlt_n[1:5])

    while True:
        if dtuple not in dbseq:
            dbseq[dtuple] = mod_n[-1]
            sumdbseq[dtuple] += mod_n[-1]
        if i > count:
            break
        sec_n = sec_n[1:] + [next_secret(sec_n[-1])]
        mod_n = mod_n[1:] + [sec_n[-1] % 10]
        dlt_n = dlt_n[1:] + [mod_n[-1] - mod_n[-2]]
        dtuple = tuple(dlt_n[1:5])
        i += 1

    alldbseq[idx] = dbseq

def main(fname):
    buyers = list(map(int,fname.read().strip().split('\n')))

    part1 = 0
    for b in buyers:
        secret = b
        for _ in range(2000):
            secret = next_secret(secret)
        part1 += secret
    print (f'Part 1: {part1}')

    for i,b in enumerate(buyers):
        print (f'Buyer : {i+1:4d}/{len(buyers):4d}', end='\r')
        buyer_sig(i, b, 2000, 4)

    (k,_) = max(sumdbseq.items(), key=lambda x: x[1])
    bananas = 0
    for i,b in enumerate(buyers):
        bananas += alldbseq[i][k]
    print (f'Part 2: {bananas} {' '*20}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
