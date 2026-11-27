#!/usr/bin/env python3
"""R-349 (suite) Horloges à 2 générateurs : 4 vaisseaux (symétrie d'ordre 2) ou 6 vaisseaux (symétrie d'ordre 3), tirés au hasard
dans un disque de rayon R ; on garde les CYCLES exacts (fourmi_r) et on mesure la taille de l'orbite.
Usage : python3 horloge2.py [nombre] [rayon] [T] [graine]"""
import sys, json, random, collections
from fa_lib import kship
from hx import rot
from demi_add_k import fmt
from outils_r import lot
from exp_osc import hd
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000; Rr = int(sys.argv[2]) if len(sys.argv) > 2 else 8
T = int(sys.argv[3]) if len(sys.argv) > 3 else 8000; random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
jobs = []; meta = []
while len(jobs) < N:
    m, sr = random.choice([(2, 3), (3, 2)])
    gens = []
    for _ in range(2):
        while True:
            x, y = random.randint(-Rr, Rr), random.randint(-Rr, Rr)
            if hd(x, y) <= Rr and (x, y) != (0, 0): break
        gens.append(kship(random.randrange(6), (x, y), random.randrange(8)))
    ants = []; cells = []
    for g in gens:
        for k in range(m):
            a, cs = g; rr = k * sr; X, Y = rot(a[:2], rr); ants.append((X, Y, (a[2] + rr) % 6)); cells += [rot(c, rr) for c in cs]
    if len(set(cells)) < len(cells) or len({a[:2] for a in ants}) < len(ants): continue
    if min(hd(a[0] - b[0], a[1] - b[1]) for i, a in enumerate(ants) for b in ants[i + 1:]) < 3: continue
    jobs.append(fmt(ants, cells)); meta.append(m)
out = lot(jobs, T)
cnt = collections.Counter(); res = []
for m, s, l in zip(meta, jobs, out):
    f = l.split('|'); issue = f[3]; cnt[(m, issue)] += 1
    if issue == 'CYCLE': res.append({'m': m, 'sit': s, 'P': int(f[5]), 'boite': f[-1]})
print(sorted(cnt.items()))
print('cycles :', len(res))
json.dump(res, open('data/horloges2_R%d_s%s.json' % (Rr, sys.argv[4] if len(sys.argv) > 4 else '1'), 'w'))
for z in sorted(res, key=lambda z: -z['P'])[:10]: print(z['m'], z['P'], z['boite'], z['sit'][:120])
