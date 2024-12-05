import sys

correctCount = 0
incorrectCount = 0
rules = {}
for line in sys.stdin:
    if "|" in line:
        a, b = [int(x) for x in line.split("|")]
        if a not in rules.keys():
            rules[a] = [b]
        else:
            rules[a].append(b)
    if "," in line:
        correct = True
        update = [int(x) for x in line.split(",")]
        corrected = []
        for i in range(len(update)):
            num = update[i]
            if num in rules.keys():
                for j in range(0, i):
                    if update[j] in rules[num]:
                        correct = False
                        k = corrected.index(update[j])
                        if num in corrected:
                            if k < corrected.index(num):
                                corrected.remove(num)
                        if num not in corrected:
                            corrected.insert(k, num)
                for j in range(i + 1, len(update)):
                    if update[j] in rules.keys():
                        if num in rules[update[j]]:
                            correct = False
            if num not in corrected:
                corrected.append(num)
        if correct:
            correctCount += update[len(update) // 2]
        if not correct:
            incorrectCount += corrected[len(corrected) // 2]
print(correctCount)
print(incorrectCount)
