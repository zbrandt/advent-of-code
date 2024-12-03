import sys, re

def main(farg):
    enabled = True
    total1 = total2 = 0
    for a, b, do, dont in re.findall(r"mul\((\d+)\,(\d+)\)|(do\(\))|(don't\(\))", farg.read()):
        if do or dont:
            enabled = not sdont
        else:
            x = int(a) * int(b)
            total1 += x
            total2 += x * enabled
    print (f'Part 1: {total1}')
    print (f'Part 2: {total2}')

if __name__ == "__main__":
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
    