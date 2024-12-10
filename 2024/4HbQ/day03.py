from parse import findall
d = "do()" + open("data.txt").read() + "don't()"
for _ in 1, 2:
    print(sum(x*y for x,y in findall("mul({:d},{:d})", d)))
    d = ''.join(r[0] for r in findall("do(){}don't()", d))
