import random
from demux_cherche import *
random.seed(1)
for _ in range(3000):
    G1, G2, G3, F = (random.choice(cat) for _ in range(4))
    i1, w1, i2, i3, j = (random.randrange(2) for _ in range(5))
    cs = candidates(G1, i1, w1, G2, i2, G3, i3, F, j, range(6,70))
    if cs:
        k2, n, k3, FA = cs[0]
        W1 = G1.outs[i1] if w1 == 0 else G1.outs[1 - i1]
        C2 = G2.align(i2, W, k2); C3 = G3.align(i3, W1, k3)
        print('x', norm(FA.outs[j]), norm(C2.ins[1-i2]))
        print('y', norm(FA.outs[1-j]), norm(C3.ins[1-i3]), k2, n, k3)
        break
