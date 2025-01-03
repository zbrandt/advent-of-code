""" Module for Advent of Code Day 21.
    https://adventofcode.com/2015/day/21
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring

from itertools import combinations, chain, product

weapons = {
    'Dagger'    : ( 8, 4, 0),
    'Shortsword': (10, 5, 0),
    'Warhammer' : (25, 6, 0),
    'Longsword' : (40, 7, 0),
    'Greataxe'  : (74, 8, 0),
}

armor = {
    'Leather'   : ( 13, 0, 1),
    'Chainmail' : ( 31, 0, 2),
    'Splintmail': ( 53, 0, 3),
    'Bandedmail': ( 75, 0, 4),
    'Platemail' : (102, 0, 5),
}

rings = {
    'Damage +1' : ( 25, 1, 0),
    'Damage +2' : ( 50, 2, 0),
    'Damage +3' : (100, 3, 0),
    'Defense +1': ( 25, 0, 1),
    'Defense +2': ( 40, 0, 2),
    'Defense +3': ( 80, 0, 3),
}

class Player:
    def __init__(self, name, hp=0, dam=0, arm=0):
        self.name = name
        self.hp = hp
        self.dam = dam
        self.arm = arm

def attack(attacker:Player, defender:Player, verbose):
    damage = max(attacker.dam - defender.arm, 1)
    defender.hp = max(defender.hp - damage, 0)
    if verbose:
        print (f'  - The {attacker.name} deals {attacker.dam}-{defender.arm} = {damage} damage; the {defender.name} goes down to {defender.hp} hit points.')

def play_game(p1, p2, verbose):
    while p1.hp and p2.hp:
        attack(p1, p2, verbose)
        p1,p2 = p2,p1
    if p1.hp < p2.hp:
        p1,p2 = p2,p1
    if verbose:
        print (f'In this scenario, the {p1.name} wins!')
    return p1

def powerset(iterable, pwr = None):
    s = list(iterable)
    pwr = (min(pwr, len(s)), len(s))[pwr is None]
    return chain.from_iterable(combinations(s, r) for r in range(pwr+1))

def main():

    wc = list(combinations(weapons,1))
    ac = list(powerset(armor,1))
    rc = list(powerset(rings,2))

    scenarios = []
    shopping_lists = list(product(wc, ac, rc))
    for sl in shopping_lists:
        cost = sum(weapons[x][0] for x in sl[0]) + sum(armor[x][0] for x in sl[1]) + sum(rings[x][0] for x in sl[2])
        dam  = sum(weapons[x][1] for x in sl[0]) + sum(armor[x][1] for x in sl[1]) + sum(rings[x][1] for x in sl[2])
        arm  = sum(weapons[x][2] for x in sl[0]) + sum(armor[x][2] for x in sl[1]) + sum(rings[x][2] for x in sl[2])

        player = Player('player', 100, dam, arm)
        boss = Player('boss', 109, 8, 2)
        win = play_game(player, boss, False)
        scenarios.append([cost, dam, arm, sl, win.name])

    for x in sorted(scenarios):
        #print (f'win={x[4]} cost={x[0]} dam={x[1]} arm={x[2]} sl={x[3]}')
        pass

    print (f'Part 1: {min(x[0] for x in scenarios if x[4] == "player")}')
    print (f'Part 2: {max(x[0] for x in scenarios if x[4] == "boss")}')

if __name__ == "__main__":
    main()
