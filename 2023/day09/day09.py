import sys

def get_next(seq:[int]) -> int:
    if not any(seq):
        return 0
    diffs = [seq[x] - seq[x-1] for x in range(1,len(seq))]
    return seq[-1] + get_next(diffs)

def get_prev(seq:[int]) -> int:
    if not any(seq):
        return 0
    diffs = [seq[x] - seq[x-1] for x in range(1,len(seq))]
    return seq[0] - get_prev(diffs)


next_sums = 0
prev_sums = 0
for line in sys.stdin:
    seq = list(map(int,line.split()))
    next = get_next(seq)
    prev = get_prev(seq)
    print (f'{prev} --> {seq=} --> {next}')
    next_sums += next
    prev_sums += prev

print (f'{next_sums=} {prev_sums=}')
