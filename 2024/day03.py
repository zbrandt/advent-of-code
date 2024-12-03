import sys, re
from operator import mul

def mulstr(s) -> int:
    return mul(*map(int,re.match(r'mul\((\d+)\,(\d+)\)', s).groups()))

def main(arg):
    x = arg.read().strip()

    sum_mul = sum(mulstr(m) for m in re.findall(r'mul\(\d+\,\d+\)', x))
    print (f'Part 1: {sum_mul}')

    enabled = True
    sum_mul = 0
    dd_matches=re.findall(r"mul\(\d+\,\d+\)|do\(\)|don't\(\)", x)
    for m in dd_matches:
        if m == "do()":
            enabled = True
        elif m == "don't()":
            enabled = False
        elif enabled:
            sum_mul += mulstr(m)
    print (f'Part 2: {sum_mul}')

if __name__ == "__main__":
    arg = sys.stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as arg:
            main(arg)
    else:
        main(arg)
