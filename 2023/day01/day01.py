import sys
import re

ten_digits = {
    'one'   : '1',
    'two'   : '2',
    'three' : '3',
    'four'  : '4',
    'five'  : '5',
    'six'   : '6',
    'seven' : '7',
    'eight' : '8',
    'nine'  : '9',
}

p1 = "|".join([x[:-1] + '(?=' + x[-1:] + ')' for x in ten_digits.keys()])
pattern = re.compile(p1)

if False:
    line = 'fiveight'
    m = pattern.findall(line)
    res = pattern.sub(lambda m: ten_digits[m.group(0) + line[m.span()[1]]], line)
    print (m, res)

sum = 0
abc_sum = 0
for line in sys.stdin:
    line = line.strip()
    digits = list(map(int, filter(str.isdigit, list(line))))
    cal = digits[0] * 10 + digits[-1]
    sum += cal

    abc_line = pattern.sub(lambda m: ten_digits[m.group(0) + line[m.span()[1]]], line)
    abc_digits = list(map(int, filter(str.isdigit, list(abc_line))))
    abc_cal = abc_digits[0] * 10 + abc_digits[-1]
    abc_sum += abc_cal

print (sum, abc_sum)