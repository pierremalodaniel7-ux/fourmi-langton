#!/usr/bin/env python3
"""R-608 (suite) Recherche des longueurs pour un gros module : objectif = 100·(cas faux) + 10·(cas sales) + conflits « logiques »
(segments d'arrivée ou sortie racine, diag.py, seuil 4) + 5·(routes opposées à < 4 voies). Descente aléatoire, écrit au fur et à mesure.
Usage : python3 opt2.py module graine iterations"""
import sys, json, random, time
from modules import module, nodes
from nor import *
from diag import conflicts
nm, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
root = module(nm); names = [n.name for n in nodes(root)]
def evaluate(Dm, Gm):
    L = Layout(root, Dmap=Dm, Gmap=Gm)
    c = [x for x in conflicts(L, thr=4) if 'in' in (x[1], x[3]) or root.name in (x[0], x[2])]
    w, bad = L.opposed(); opp = 0
    for o, i in bad:
        lo = [lane_of2(antpos(o, t), o[0]) for t in range(8)]; li = [lane_of2(antpos(i, t), o[0]) for t in range(8)]
        if min(abs(x - y) for x in lo for y in li) < 4: opp += 1
    r = L.check(); wrong = sum(1 for x in r if x[2] != x[3]); dirty = sum(1 for x in r if not x[1])
    return 100 * wrong + 10 * dirty + len(c) + 5 * opp, (wrong, dirty, len(c), opp)
rnd = random.Random(seed)
Dm = {n: rnd.randint(8, 50) for n in names}; Gm = {n: rnd.randint(8, 18) for n in names}
s, det = evaluate(Dm, Gm); t0 = time.time()
log = open(f'data/opt2_{nm}_{seed}.log', 'a')
for it in range(iters):
    D2, G2 = dict(Dm), dict(Gm)
    for _ in range(rnd.choice((1, 1, 2, 3))):
        n = rnd.choice(names)
        if rnd.random() < 0.6: D2[n] = max(8, min(80, D2[n] + rnd.randint(-8, 8)))
        else: G2[n] = max(8, min(24, G2[n] + rnd.randint(-3, 3)))
    s2, det2 = evaluate(D2, G2)
    if s2 <= s:
        if s2 < s: print(f'{it} {time.time()-t0:.0f}s score {s2} (faux, sales, conflits, opposées) = {det2}', file=log, flush=True)
        Dm, Gm, s, det = D2, G2, s2, det2
        json.dump(dict(D=Dm, G=Gm, score=s, detail=det), open(f'data/opt2_{nm}_{seed}.json', 'w'))
    if s == 0: break
print('fin', s, det, file=log, flush=True)
