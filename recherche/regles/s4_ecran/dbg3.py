import random
from demux_cherche import *
random.seed(3)
bad=0
for _ in range(50):
    G1 = random.choice(cat); i1 = random.randrange(2)
    C = G1.align(i1, W, 0)
    for dt in (0, 200):
        C2 = C.mov((0,0), dt)
        ins = C2.ins if C2.first == 0 else C2.ins[::-1]
        T = C2.te + 640
        a, cc = lotdump([sit_of(ins, 0)], T)[0]; d = decode(a, cc)
        got = sorted(of_label(lab_of(z, T)) for z in d) if d else None
        if got != sorted(norm(t) for t in C2.outs): bad += 1; print('bad', i1, dt, C2.te, got, sorted(C2.outs))
print(bad)
