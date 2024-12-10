data = [*map(int, open('in.txt').read().split())]
A, B = sorted(data[0::2]), sorted(data[1::2])
print(sum(map(lambda a, b: abs(a-b), A, B)),
      sum(map(lambda a: a * B.count(a), A)))
