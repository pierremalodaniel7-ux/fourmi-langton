#!/usr/bin/env python3
"""S1 / R-404 CROISEMENT : deux signaux dont les routes se coupent.
(a) Sans constant : parmi TOUS les chocs de 2 vaisseaux qui interagissent (fusion1.json : 1 688 chocs propres sur 1 880, R-333),
    lesquels rendent EXACTEMENT les deux trajectoires libres (même direction, voie, instant, phase) ? = croisement « par choc ».
(b) Bilan par angle : pour chaque angle (direction relative r = 1..5), quelles relations horaires (tau, v mod u) sont transparentes
    (jamais à moins de 6 : transparent exact, R-333) ou se comportent comme un croisement ; ce qui reste = horaires interdits.
Usage : python3 s1_fusion/croisement.py"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from hx import ship, ship_dir, step
from chocs_exhaustif_lib import hd, DMAX
D = json.load(open(os.path.join(HERE, 'fusion1.json'))); res = D['res']; T = D['T']
from fusion1_lib import decodeg
KA, KG = D['K'][0], {tuple(c): 1 for c in D['K'][1]}
def free(a, g):
    A = [list(a)]; G = dict(g)
    for _ in range(T): step(A, G)
    return tuple(decodeg(A, sorted(G))[0])
Kf = free(KA, KG)
cnt = collections.Counter(); ex = []
for c in res:
    sA, cs = c['s']; f = free(sA, {tuple(x): 1 for x in cs})
    same = sorted(map(tuple, c['out'])) == sorted([f, Kf])
    cnt[(c['r'], same)] += 1
    if same: ex.append(c)
print('chocs propres qui rendent exactement les 2 trajectoires libres (croisement par choc) :', len(ex))
for r in range(1, 6): print('  r =', r, ':', cnt[(r, True)], '/', cnt[(r, True)] + cnt[(r, False)])
json.dump(ex, open(os.path.join(HERE, 'croisement_choc.json'), 'w'))
