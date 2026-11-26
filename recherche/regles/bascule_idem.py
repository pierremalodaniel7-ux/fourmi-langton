#!/usr/bin/env python3
"""R-341 (suite) Écritures idempotentes ? « mise à 1 » sur l'état 1 (toutes ses phases) et « mise à 0 » sur l'état 0 laissent-elles l'objet
dans son orbite, sans débris, vaisseau ressorti ? (920 bascules RS de data/bascules_RS.json)"""
import json, sys
import bascule_demo as bd   # (exécute la démo de l'indice 0 au chargement : sans effet sur ce test)
from hx import step, PHASES
from exp_osc import setup, hd, parse
def kv(s): return dict(x.split('=') for x in s.split()[1:] if '=' in x)
def test(X):
    f1, f2 = kv(X['s1']), kv(X['s2'])
    OR, OR2 = bd.orbit_states(X['R']), bd.orbit_states(X['R2'])
    K1 = bd.kit(X['R'], f1); K2 = bd.kit(X['R2'], f2)
    res = []
    for (Kt, orb) in ((K1, OR2), (K2, OR)):
        ok = 0
        for st in orb:
            ants = [list(a) for a in st[0]]; g = {c: 1 for c in st[1]}
            ants += [list(a) for a in Kt[0][0]] if Kt[4] == 0 else []; g.update(Kt[0][1])
            for _ in range(Kt[2] + 200): step(ants, g)
            na = sorted(tuple(a) for a in ants if hd(a[0], a[1]) <= 10); nc = sorted(c for c in g if hd(*c) <= 10)
            far = [a for a in ants if hd(a[0], a[1]) > 10]
            clean = len(far) == 1 and all(hd(c[0] - far[0][0], c[1] - far[0][1]) <= 2 for c in g if hd(*c) > 10)
            ok += ((na, nc) in orb) and clean
        res.append(ok == len(orb))
    return res
F = json.load(open('data/bascules_RS.json'))
n = 0; good = []
for i, X in enumerate(F):
    r = test(X)
    if all(r): good.append(i)
print('bascules RS idempotentes (écrire 1 sur 1 et 0 sur 0 sans effet, toutes phases) :', len(good), '/', len(F), good[:20])
json.dump(good, open('data/bascules_idem.json', 'w'))
