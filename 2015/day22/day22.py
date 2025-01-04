""" Module for Advent of Code Day 21.
    https://adventofcode.com/2015/day/21
"""
# pylint: disable=line-too-long, missing-function-docstring, missing-class-docstring
import sys
import re
import builtins
from itertools import chain
from copy import deepcopy
from typing import Dict

verbose = True # pylint: disable=invalid-name

def vprint(*args, **kwargs):
    if verbose:
        builtins.print(*args, **kwargs)

class Player:
    def __init__(self, name:str, hp:int):
        self.name = name
        self.hp = hp

    def __repr__(self):
        return f'Player (name="{self.name}", hp={self.hp})'

class Boss(Player):
    def __init__(self, name:str = 'Boss', hp:int = 55, damage:int = 8):
        super().__init__(name, hp)
        self.damage = damage

    def __repr__(self):
        return f'Boss (name="{self.name}", hp={self.hp}, damage={self.damage})'

class Wizard(Player):
    def __init__(self, name:str = 'Player', hp:int = 50, mana:int = 500):
        super().__init__(name, hp)
        self.mana = mana

    def __repr__(self):
        return f'Wizard (name="{self.name}", hp={self.hp}, mana={self.mana})'

class Spell:
    def __init__(self, **kwargs):
        self.name:str = None
        self.mana:int = 0
        self.boss_hp:int = 0
        self.wiz_hp:int = 0
        self.duration:int = 0
        self.recharge:int = 0
        self.armor:int = 0
        self.__dict__.update( kwargs )

class WizardSimulator:

    min_wiz_win:int = 999999

    spell_book = {s.name:s for s in [
        Spell(name='Missile',   mana=53,  boss_hp=-4 ),
        Spell(name='Drain',     mana=73,  boss_hp=-2,   wiz_hp=2 ),
        Spell(name='Shield',    mana=113, armor=7,      duration=6 ),
        Spell(name='Poison',    mana=173, boss_hp=-3,   duration=6 ),
        Spell(name='Recharge',  mana=229, recharge=101, duration=5 ),
    ]}

    def __init__(self, wiz = Wizard(), boss = Boss(), hard=False):
        #config
        self.wiz = wiz
        self.boss = boss
        self.hard = hard

        # state
        self.spells:Dict[str, Spell] = {}
        self.history:list[str] = []
        self.turns:int = 0
        self.who:Player = self.wiz
        self.opp:Player = self.boss
        self.mana_spent:int = 0

    def __repr__(self):
        last_spell = self.history[-1] if self.history else ''
        return f'WizardSimulator (wiz={self.wiz.__repr__()}, boss={self.boss.__repr__()}, hard={self.hard}, spell={last_spell})'

    def player_turn(self):

        player = self.who

        if self.mana_spent > WizardSimulator.min_wiz_win:
            vprint (f'{player.name} turn: pruning {self.mana_spent} > {WizardSimulator.min_wiz_win}.')
            return []

        if self.hard and isinstance(player, Wizard):
            self.wiz.hp -= 1

        if self.boss.hp <= 0:
            if self.mana_spent <= WizardSimulator.min_wiz_win:
                print (f'{self.boss.name} died. Mana: {self.mana_spent}, {len(self.history)} Spells: {', '.join(self.history)}')
                if self.mana_spent < WizardSimulator.min_wiz_win:
                    print (f'New best: Mana spent: {self.mana_spent}')
                    WizardSimulator.min_wiz_win = self.mana_spent
            return []

        if self.wiz.hp <= 0:
            vprint (f'{self.wiz.name} died\n{self}')
            return []

        armor = self.spell_book['Shield'].armor * int('Shield' in self.spells)
        desc = ''
        desc += f'-- {player.name} Turn -- {('','(Hard)')[self.hard]}\n'
        desc += f'- {self.wiz.name} has {self.wiz.hp} hit points, {armor} armor, {self.wiz.mana} mana\n'
        desc += f'- {self.boss.name} has {self.boss.hp} hit points\n'

        for s in list(self.spells.values()):
            s.duration -= 1
            self.boss.hp += s.boss_hp
            self.wiz.mana += s.recharge
            desc += f'{s.name}\'s timer is now {s.duration}.\n'
            if s.duration == 0:
                desc += f'{s.name} wears off.\n'
                del self.spells[s.name]

        self.turns += 1
        self.who, self.opp = self.opp, self.who

        if isinstance(player, Wizard):
            games = self.wiz_turn(desc)
        else:
            games = self.boss_turn(desc)

        return games

    def boss_turn(self, desc):

        armor = self.spell_book['Shield'].armor * int('Shield' in self.spells)
        damage = self.boss.damage - armor
        if armor:
            desc +=  f'{self.boss.name} attacks for {self.boss.damage} - {armor} = {damage} damage!\n'
        else:
            desc += f'{self.boss.name} attacks for {damage} damage!\n'
        self.wiz.hp -= damage

        vprint(desc)

        return [self]

    def wiz_turn(self, desc):

        moves = []

        for s in self.spell_book.values():
            sdesc = str(desc)
            if self.wiz.mana >= s.mana and s.name not in self.spells:
                g = deepcopy(self)
                g.wiz.mana -= s.mana
                g.mana_spent += s.mana
                if not s.duration:
                    sdesc += f'{self.wiz.name} casts {s.name}, {-s.boss_hp} damage, {s.wiz_hp} heal\n'
                    g.boss.hp += s.boss_hp
                    g.wiz.hp += s.wiz_hp
                else:
                    sdesc += f'{self.wiz.name} casts {s.name}\n'
                    g.spells[s.name] = deepcopy(s)
                g.history.append(s.name)
                moves.append(g)
                vprint (sdesc)

        if not moves:
            desc += f'{self.wiz.name} can\'t afford any spells!\n'
            vprint (desc)

        return moves

def main(fname):
    global verbose # pylint: disable=global-statement

    verbose = False
    config = {k:int(v) for k,v in re.findall(r'(?m)^(\S.+): (\w+)', fname.read())}
    boss = Boss('Boss', config['Hit Points'], config['Damage'])

    parts = []
    for hard in [False, True]:
        games = [WizardSimulator(boss=boss, hard=hard)]
        WizardSimulator.min_wiz_win = 99999
        print (games)
        while games:
            games = list(chain.from_iterable([g.player_turn() for g in games]))
            for i,g in enumerate(games):
                vprint (f'{i:3d}/{len(games)}: {g}')

        parts.append(WizardSimulator.min_wiz_win)

    for i,p in enumerate(parts):
        print (f'Part {i+1}: {p}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
