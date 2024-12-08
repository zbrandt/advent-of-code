import sys

input_lines:list[str] = sys.stdin.read().strip().split('\n')
ncards = len(input_lines)
card_counts = [1] * ncards

points:int = 0           
for idx, line in enumerate(input_lines):
    card, _, values = line.partition(':')
    winners, _, youhave = values.partition('|')
    winners = set(map(int,winners.split()))
    youhave = set(map(int,youhave.split()))
    matches = winners & youhave
    if matches:
        points += 1 << (len(matches)-1)
        for i in range (idx+1, idx+len(matches)+1):
            card_counts[i] += card_counts[idx]
print (f'{card=} {winners=} {youhave=} {matches=} {points=} cards={sum(card_counts)}')
print (f'{card_counts=} sum={sum(card_counts)}')
