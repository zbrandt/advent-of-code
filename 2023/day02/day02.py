import sys
import functools
import operator

from collections import Counter

limits = Counter({'red' : 12, 'green' : 13, 'blue' : 14})

fitting = []
powers = []
for line in sys.stdin:
    game, reveals = line.split(':')
    game_num = game.split()[1]
    reveals = reveals.split(';')
    ctr_union = Counter()
    for r in reveals:
        ctr = Counter({ vk[1]:int(vk[0]) for vk in [c.split() for c in r.split(',')] })
        ctr_union = ctr_union | ctr
    if ctr_union <= limits:
        fitting.append(int(game_num))
    powers.append(functools.reduce(operator.mul, ctr_union.values(), 1))

print (f'sum of fitting games: {sum(fitting)}')
print (f'sum of powers: {sum(powers)}')
