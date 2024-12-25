""" Module for Advent of Code Day 5.
    https://adventofcode.com/2015/day/5
"""
import re

# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring

def three_vowels(s:str) -> bool:
    return sum(s.count(vowel) for vowel in list('aeiou')) >= 3

def twice_in_a_row(s:str) -> bool:
    return re.search(r'(.)\1', s) is not None

def no_bad_strings(s:str) -> bool:
    return all(bad not in s for bad in ['ab', 'cd', 'pq', 'xy'])

def pair_of_pairs(s:str) -> bool:
    return re.search(r'(..).*\1', s) is not None

def palindrome3(s:str) -> bool:
    return re.search(r'(.).\1', s) is not None

def main(fname):
    strings = fname.read().strip().split('\n')
    
    print ('\n'.join([f'Part {i+1}: {sum([all(r(s) for r in rules) for s in strings])}' \
                      for i,rules in enumerate([[three_vowels, twice_in_a_row, no_bad_strings], \
                                                [pair_of_pairs, palindrome3]])]))

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)