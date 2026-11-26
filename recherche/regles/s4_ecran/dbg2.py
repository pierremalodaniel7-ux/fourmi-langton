import random
from demux_cherche import *
random.seed(3); n=0
while n < 3:
    G1, G2, G3, F = (random.choice(cat) for _ in range(4))
    i1, w1, i2, i3, j = (random.randrange(2) for _ in range(5))
    cs = candidates(G1, i1, w1, G2, i2, G3, i3, F, j, range(6,70))
    if not cs: continue
    k2, nn, k3, FA = cs[0]
    B = build(G1, i1, w1, G2, i2, G3, i3, F, j, k2, k3, FA, 0) or build(G1, i1, w1, G2, i2, G3, i3, F, j, k2, k3, FA, 1)
    if not B: continue
    B = shift_all(B, 400 - min(B['times'].values())); Tend = max(B['times'].values()) + 640
    for c in [(1,0)]:
        a, cc = lotdump([case_sit(B, *c)], Tend)[0]; d = decode(a, cc)
        print(c, 'got', sorted(of_label(lab_of(z, Tend)) for z in d) if d else None)
        print('   exp', B['exp'][c], B['times'], B['order'])
        # G1 alone
        a, cc = lotdump([sit_of([B['T'][x] for x in B['order'] if x in ('W','a1')])], Tend)[0]; d = decode(a, cc)
        print('   G1 seul', sorted(of_label(lab_of(z, Tend)) for z in d))
    n += 1
