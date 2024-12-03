import sys, re

def main(farg):
    enabled = True
    total1 = total2 = 0
    for a, b, sdo, sdont in re.findall(r"mul\((\d+)\,(\d+)\)|(do\(\))|(don't\(\))", farg.read()):
        if sdo or sdont:
            enabled = not sdont
        else:
            x = int(a) * int(b)
            total1 += x
            total2 += x * enabled
    print (f'Part 1: {total1}')
    print (f'Part 2: {total2}')

if __name__ == "__main__":
    arg = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin