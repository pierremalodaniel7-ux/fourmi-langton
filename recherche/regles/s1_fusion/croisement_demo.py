#!/usr/bin/env python3
"""S1 / R-404 Croisement réutilisable SANS constant : deux signaux (directions 0 et r) dont les fourmis passent à distance 2 l'une
de l'autre (le plus près possible sans s'influencer, d'après croisement.py) ; 4 cas, 2 usages (16 suites), 20 usages (3 graines + 20 × (1,1)),
2 moteurs, certificat « tout nombre d'usages ». Pour r = 1 (60°), 2 (120°), 4, 5 (et 3 = face à face sur voies voisines, pour voir).
Usage : python3 s1_fusion/croisement_demo.py"""
import sys, os, json, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from hx import ship, ship_dir, step
from chocs_exhaustif_lib import hd
from fa_lib import decode, lotdump, back, kship
from circuit import Circuit, check_cases, check_multi, certificat
def path(a, g, n):
    A = [list(a)]; G = dict(g); P = []
    for _ in range(n): step(A, G); P.append(tuple(A[0][:2]))
    return P
out = []
for r in (1, 2, 3, 4, 5):
    Bp = kship(0, (0, 0), 0); dA = ship_dir(r); best = None
    PB = path(Bp[0], {c: 1 for c in Bp[1]}, 1200)
    for x in range(-6, 7):
        for y in range(-6, 7):
            for tau in range(8):
                Ap = kship(r, (x - 60 * dA[0] + 60 * ship_dir(0)[0], y - 60 * dA[1] + 60 * ship_dir(0)[1]), tau)
                PA = path(Ap[0], {c: 1 for c in Ap[1]}, 1200)
                d = min(hd(p[0] - q[0], p[1] - q[1]) for p, q in zip(PA, PB))
                if d == 2 and (best is None or (abs(x) + abs(y)) < best[0]): best = (abs(x) + abs(y), Ap)
    if best is None: print('r =', r, ': pas de géométrie à distance 2'); continue
    Ap = best[1]
    Kd = kship(0, (40, 40), 0)          # témoin : vaisseau constant parallèle à B, 80 voies plus loin (le cas (0,0) n'est pas vide)
    C = Circuit([('Kd', Kd, None), ('B', back(Bp, 40), 'y'), ('A', back(Ap, 40), 'x')])
    R = lotdump([C.sit({'x': 0, 'y': 0}), C.sit({'x': 1, 'y': 0}), C.sit({'x': 0, 'y': 1})], 4000)
    d = [set(map(tuple, decode(*x))) for x in R]
    (oA,), (oB,) = d[1] - d[0], d[2] - d[0]
    C.outputs = {'X': (lambda e: e['x'], [oA]), 'Y': (lambda e: e['y'], [oB])}
    rc = check_cases(C, 4000)
    n2 = sum(1 for e1, e2 in itertools.product(C.cases(), repeat=2) if (lambda s: s[0] and s[1] == 2)(check_multi(C, [e1, e2], 200)))
    r20 = []
    for seed in range(3):
        random.seed(seed); seq = [random.choice(C.cases()) for _ in range(20)]
        sup, gd, same, s = check_multi(C, seq, 200, engine2=True); r20.append((sup, gd, same))
    sup, gd, same, s = check_multi(C, [{'x': 1, 'y': 1}] * 20, 200, engine2=True); r20.append((sup, gd, same))
    worst, per, fronts = certificat(C, 200, 4000, J=6, log=lambda *a: None)
    print(f'r = {r} : 4 cas {sum(z[1] for z in rc)}/4 (2 moteurs {all(z[3] for z in rc)}) ; 2 usages {n2}/16 ; 20 usages {r20} ; '
          f'certificat min {worst} {per} ; face {fronts}', flush=True)
    out.append(dict(r=r, A=Ap, B=Bp, quatre=sum(z[1] for z in rc), deux_usages=n2, vingt=r20, cert=dict(min=worst, per=per, fronts=fronts),
                    un_usage={str((e['x'], e['y'])): C.sit(e) for e in C.cases()}))
json.dump(out, open(os.path.join(HERE, 'croisement_demo.json'), 'w'), indent=1)
