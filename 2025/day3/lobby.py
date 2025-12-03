import numpy as np

def largest_joltage(bank, n):
    bank = np.array(bank)
    joltage = ""
    
    while n > 0:
        i = np.argmax(bank[:(len(bank) - n + 1)])
        joltage += str(bank[i])
        bank = np.split(bank, [i + 1])[1]
        n -= 1

    return int(joltage)

def main(fname):
    one = two = 0
    banks = [list(map(int,x.strip())) for x in fname.read().split('\n')]
    for bank in banks:
        one += largest_joltage(bank, 2)
        two += largest_joltage(bank, 12)
    
    print(f'Part One: {one}')
    print(f'Part One: {two}')

if __name__ == "__main__":
    import sys
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
