#!/usr/bin/env python3
"""R-328 Un demi-additionneur R2L2 (data/demi_add_reutilisables.json) utilisé N fois de suite, entrées (a,b) au hasard, k périodes d'écart.
Lecture de chaque usage : S = nombre de vaisseaux sur la voie S issus de cet usage, C = idem sur la voie C (fourmis repérées par usage)."""
import json, random, sys
from banc import sit
from outils_r import lot, parse
R = 'H:R2L2'; P = 8
import os
H = json.load(open(os.environ.get('DA_FILE', 'data/demi_add_reutilisables.json')))[int(sys.argv[1]) if len(sys.argv) > 1 else 0]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 20; k = int(sys.argv[3]) if len(sys.argv) > 3 else 200
def tracks(l):
    d = parse(l); return [((a[1], a[2]), a[1] * d['fin'][i][1] - a[2] * d['fin'][i][0]) if a else None for i, a in enumerate(d['ants'])]
a_, c_ = H['porte'].split('|')[1:]
an = [tuple(map(int, t.split(','))) for t in a_.split(';')]; cl = [tuple(map(int, t.split(',')[:2])) for t in c_.split(';') if t]
src = {'B': (an[0], [(1, 0)]), 'A': (an[1], [c for c in cl if c != (1, 0)]), 'K2': (tuple(H['K2'][0]), [tuple(c) for c in H['K2'][1]]), 'K3': (tuple(H['K3'][0]), [tuple(c) for c in H['K3'][1]])}
dd = {n: tracks(lot([sit(R, [x], {c: 1 for c in cc})], 1 << 16)[0])[0][0] for n, (x, cc) in src.items()}
S = (tuple(H['S'][0]), H['S'][1]); C = (tuple(H['C'][0]), H['C'][1])
random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 9); seq = [(random.randint(0, 1), random.randint(0, 1)) for _ in range(N)]
al = []; ce = {}; owner = []
for u, (a, b) in enumerate(seq):
    for n, on in (('B', b), ('A', a), ('K2', 1), ('K3', 1)):
        if not on: continue
        x, cc = src[n]; v = (-u * k * dd[n][0], -u * k * dd[n][1])
        al.append((x[0] + v[0], x[1] + v[1], x[2])); owner.append(u); [ce.__setitem__((c[0] + v[0], c[1] + v[1]), 1) for c in cc]
s = sit(R, al, ce)
t = tracks(lot([s], max(1 << 20, 4 * N * k * P))[0])
ok = 0
for u, (a, b) in enumerate(seq):
    mine = [t[i] for i in range(len(al)) if owner[i] == u]
    gS = sum(1 for x in mine if x == S); gC = sum(1 for x in mine if x == C)
    good = (gS, gC) == (a ^ b, a & b) and all(x is not None for x in mine); ok += good
    print(f"usage {u+1:2d} : a={a} b={b} → S={gS} C={gC} {'juste' if good else 'FAUX'}")
print(f"{ok}/{N} additions justes ; {len(al)} fourmis, {len(ce)} cases au départ (que des germes de vaisseaux)")
json.dump({'demi_additionneur': H, 'k': k, 'suite': seq, 'justes': ok, 'situation': s}, open(f'data/usages_add_{N}.json', 'w'))
