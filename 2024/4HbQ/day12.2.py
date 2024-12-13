from numpy import array as A, count_nonzero as nnz, unique
from scipy.ndimage import label
from scipy.signal import convolve2d

G = A([list(l.strip()) for l in open('in.txt')])

ans = A([0,0])
for L, n in [label(G == g) for g in unique(G)]:
    for i in range(n):
        H = (L == i+1)

        h = nnz(convolve2d(H, [[1,-1]]))
        v = nnz(convolve2d(H, [[1],[-1]]))
        x = abs(convolve2d(H, [[-1,1],[1,-1]]))

        ans += H.sum() * A([h+v, x.sum()])

print(*ans)
