#!/usr/bin/env python3
"""T4 : toutes les routes de vaisseaux du pas complet (R-617), pour placer les pixels loin de tout.
Entrées : réunion des lignes d'univers posées (256 états) -> segments de t = 0 jusqu'au germe (on prend toute la droite jusqu'à
l'abscisse du germe + marge, prudent). Sorties : décodage exact (moteur C) des 256 états à TDEC -> rayons, prolongés en arrière de
TDEC/8 cases (un vaisseau vu à TDEC n'a pas pu parcourir plus). Sortie : t4/rayons.json = liste [r, lat, a_min, a_max] (a_max None = ∞)"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t4lib import *
t0 = time.time(); envs = STEP.cases()
seg = {}
def add(r, l, a0, a1):
    k = (r, l); o = seg.get(k)
    seg[k] = [min(a0, o[0]), None if (a1 is None or (o and o[1] is None)) else max(a1, o[1])] if o else [a0, a1]
for e in envs:
    for w in STEP.present(e):
        r = w[0]; p0 = S3L.antpos(w, 0); p1 = S3L.antpos(w, TDEC)
        l, a0 = lat_ab(p0, r); _, a1 = lat_ab(p1, r); add(r, l, a0, a1)
R = run_c([STEP.sit(e) for e in envs], TDEC); bad = 0
for (a, c) in R:
    d = decode3(a, c, TDEC)
    if d is None: bad += 1; continue
    for w in d:
        r = w[0]; p = S3L.antpos(w, TDEC); l, ab = lat_ab(p, r); add(r, l, ab - 2 * (TDEC // 8) - 4, None)
out = [[k[0], k[1], v[0], v[1]] for k, v in seg.items()]
json.dump(out, open(os.path.join(T4, 'rayons.json'), 'w'))
print(len(out), 'segments ;', bad, 'états non décodés ;', f'{time.time()-t0:.0f} s')
