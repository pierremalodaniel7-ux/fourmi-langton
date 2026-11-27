from traj import *
import random
cat = catalogue(False); print(len(cat), 'chocs ;', len(catalogue()), 'déviations')
random.seed(5); bad = 0; lines = []; exp = []
for _ in range(200):
    c = random.choice(cat); k = random.randrange(6)
    X = norm((random.randrange(6), random.randint(-50, 50), random.randint(-50, 50), random.randrange(8)))
    i = random.randrange(2); C = c.align(i, X, random.randint(-5, 5))
    t0 = C.te - 200
    ins = C.ins if C.first == 0 else C.ins[::-1]
    lines.append(sit_of(ins, t0)); exp.append((t0, sorted(norm(T) for T in C.outs)))
R = lotdump(lines, 680)
for (t0, e), (a, cc) in zip(exp, R):
    d = decode(a, cc); got = sorted(of_label(lab_of(x, t0 + 680)) for x in d) if d else None
    bad += got != e
print('erreurs :', bad, '/ 200')
