""" Module for Advent of Code Day 14.
    https://adventofcode.com/2015/day/14
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re

def main(fname):

    data = fname.read().strip()
    reindeer = {name: {'speed':int(speed), 'duration':int(duration), 'rest':int(rest)} for name, speed, duration, rest in \
                re.findall(r'(?m)^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$', data)}

    tzero = 2503

    for step in range(1, tzero+1):
        for v in reindeer.values():
            quot, rem = divmod(step, v['duration'] + v['rest'])
            v['distance'] = (quot * v['duration'] + min(rem, v['duration'])) * v['speed']

        leader = max(reindeer, key=lambda k:reindeer[k]['distance'])

        for v in reindeer.values():
            v['points'] = v.get('points', 0) + int(v['distance'] == reindeer[leader]['distance'])

    for i,key in enumerate(['distance', 'points']):
        winner = max(reindeer, key=lambda k:reindeer[k][key])
        print (f'Part {i+1}: {reindeer[winner][key]} \"{winner}\"')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
