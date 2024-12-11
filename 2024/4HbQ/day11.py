from math import floor,log10
import functools

@functools.cache
def count(x, d=75):
    if d == 0: return 1
    if x == 0: return count(1, d-1)

    l = floor(log10(x))+1
    if l%2==0: return (count(x//10**(l//2), d-1)+
                       count(x% 10**(l//2), d-1))

    return count(x*2024, d-1)

print(sum(map(count, map(int, input().split()))))
