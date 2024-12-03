import sys, re
from operator import mul

def main(farg):    
    enabled = True
    total1 = total2 = 0
    for smul, sdo, sdont in re.findall(r"(mul\(\d+\,\d+\))|(do\(\))|(don't\(\))", farg.read()):
        if sdo or sdont:
            enabled = bool(sdo)
        else:
            x = eval(smul)
            total1 += x
            total2 += x * enabled
    print (f'Part 1: {total1}')
    print (f'Part 2: {total2}')

if __name__ == "__main__":
    arg = sys.stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as arg:
            main(arg)
    else:
        main(arg)
