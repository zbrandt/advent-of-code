def merge(ranges):
    ranges = sorted(ranges, key=lambda x: x[0])
    merged = []
    start, end = ranges[0]
    for s, e in ranges[1:]:
        if s <= end:
            end = max(e, end)
        else:
            merged.append(range(start, end))
            start, end = s, e
    merged.append(range(start, end))

    return merged

def main(fname):
    one = two = 0
    ranges, ids = [], []
    for x in fname.read().split('\n'):
        if "-" in x:
            start, end = map(int, x.split('-'))
            ranges.append((start, end + 1))
        elif x != "":
            ids.append(int(x))
    
    ranges = merge(ranges)
    for i in ids:
        for r in ranges:
            if i in r:
                one += 1
                break
        
    for r in ranges:
        two += len(r)

    print(f"Part One: {one}")
    print(f"Part Two: {two}")

if __name__ == "__main__":
    import sys
    main(open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin)
