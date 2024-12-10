D = [(None if i%2 else i//2, int(d)) for i,d in
        enumerate(open('data.txt').read())]

for i in range(len(D)-1,-1,-1):
    for j in range(i):
        i_data, i_size = D[i]
        j_data, j_size = D[j]

        if i_data != None and j_data == None and i_size <= j_size:
            D[i] = (None, i_size)
            D[j] = (None, j_size - i_size)
            D.insert(j, (i_data, i_size))


flatten = lambda x: [x for x in x for x in x]
D = [[data if data else 0]*size for data, size in D]

print(sum(i*c for i,c in enumerate(flatten(D)) if c))
