import numpy as np
from io import StringIO

def read(data, math="normal"): # 
    problems = np.array([line.split() for line in data.split('\n')]).T
    if math == "normal":
        return problems.tolist()
    
    raw = np.genfromtxt(StringIO(data), dtype='U1', delimiter=1).T
    widths = [max(map(len, p)) for p in problems]
    
    temp = []
    row = 0
    for i in range(len(problems)):
        p = raw[row:row + widths[i], 0:(len(raw[0]) - 1)]
        numbers = [int("".join(x).strip()) for x in p]
        numbers.append(str(problems[i][len(problems[i]) - 1]))
        temp.append(numbers)
        row += widths[i] + 1
    problems = temp
    return problems

def solve(problem):
    operation = problem[len(problem) - 1]
    numbers = np.array(problem[:len(problem) - 1]).astype(int)
    if operation == '+':
        return np.sum(numbers)
    else:
        return np.prod(numbers)

def main(fname):
    one = two = 0
    data = fname.read()
    one = sum(map(solve, read(data, "normal")))
    two = sum(map(solve, read(data, "cephalopod")))

    print(f"Part One: {one}")
    print(f"Part Two: {two}")

if __name__ == "__main__":
    import sys
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
