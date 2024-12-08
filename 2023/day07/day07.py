import sys
import re
from collections import Counter

rank_descriptors = (
    [r'1111', 'High card'],
    [r'1112', 'Two of a kind'],
    [r'122', 'Two pair'],
    [r'113', 'Three of a kind'],
    [r'23', 'Full house'],
    [r'4', 'Four of a kind'],
    [r'5', 'Five of a kind'],
)

def jokerify(cards:str) -> str:
    ctr = Counter(cards)
    jcards = cards
    if ctr['J']:
        most = ctr.most_common(1)[0]
        for i in ctr.most_common():
            if i[0] != 'J':
                most = i
                break
        jcards = cards.replace('J',most[0])
        print (f'{ctr['J']} jokers: {cards} -> {jcards}')
    return jcards

def rank(cards:str) -> int:
    counts = ''.join(sorted([str(item[1]) for item in Counter(cards).items()]))
    for i, desc in enumerate(rank_descriptors):
        if re.search(desc[0], counts):
            print (f'{cards=} {counts= :5} {desc[1]}')
            return i+1
    assert False

class Hand:
    def __init__(self, cards, bid) -> None:
        self.cards = cards
        self.bid = bid

        self.cardsx = self.cards.replace('A', 'E').replace('K', 'D').replace('Q', 'C').replace('J', 'B').replace('T', 'A')
        self.rank = rank(self.cards)
        self.rankx = str(self.rank) + self.cardsx

        self.jcards = jokerify(self.cards)
        self.jcardsx = self.cards.replace('A', 'E').replace('K', 'D').replace('Q', 'C').replace('J', '1').replace('T', 'A')
        self.jrank = rank(self.jcards)
        self.jrankx = str(self.jrank) + self.jcardsx

hands:[Hand] = []

for line in sys.stdin:
    cards, bid = line.split()
    hands.append(Hand(cards, int(bid)))

winnings = 0
for rank,h in enumerate(sorted(hands,key=lambda x:x.rankx, reverse=False)):
    print (f'{h.cards=} {h.bid=:6} {h.rank=} {h.rankx=} {rank_descriptors[h.rank-1][1]}')
    winnings += (rank+1) * h.bid

print (f'{winnings=}')

jwinnings = 0
for jrank,h in enumerate(sorted(hands,key=lambda x:x.jrankx, reverse=False)):
    print (f'{h.cards=} {h.jcards=} {h.bid=:6} {h.jrank=} {h.jrankx=} {rank_descriptors[h.jrank-1][1]}')
    jwinnings += (jrank+1) * h.bid

print (f'{jwinnings=}')
