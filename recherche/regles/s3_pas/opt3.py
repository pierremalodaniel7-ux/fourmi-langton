#!/usr/bin/env python3
"""R-610 Recherche des longueurs (D, G par nœud) pour un gros module, GRANDES échelles : objectif = nb de couples de segments de lignes
d'univers qui passent à < 7 l'un de l'autre hors des chocs voulus (diag.py, seuil 7 = sûr). Sans simulation ; la vérification
vient après (tous les cas, 2 moteurs). Descente aléatoire, écrit le meilleur au fur et à mesure.
Usage : python3 opt3.py module graine secondes [Dmax Gmax]"""
import sys, json, random, time
from modules import module, nodes
from nor import *
from diag import conflicts
nm, seed, secs = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
Dmax = int(sys.argv[4]) if len(sys.argv) > 4 else 300; Gmax = int(sys.argv[5]) if len(sys.argv) > 5 else 60
root = module(nm); names = [n.name for n in nodes(root)]
def evaluate(Dm, Gm):
    L = Layout(root, Dmap=Dm, Gmap=Gm); return len(conflicts(L, thr=7))
rnd = random.Random(seed)
Dm = {n: rnd.randint(8, Dmax) for n in names}; Gm = {n: rnd.randint(8, Gmax) for n in names}
s = evaluate(Dm, Gm); t0 = time.time(); it = 0
log = open(f'data/opt3_{nm}_{seed}.log', 'a'); print('départ', s, file=log, flush=True)
while time.time() - t0 < secs and s > 0:
    it += 1; D2, G2 = dict(Dm), dict(Gm)
    for _ in range(rnd.choice((1, 1, 2, 3))):
        n = rnd.choice(names); big = rnd.random() < 0.3
        if rnd.random() < 0.6: D2[n] = max(8, min(Dmax, D2[n] + (rnd.randint(-60, 60) if big else rnd.randint(-8, 8))))
        else: G2[n] = max(8, min(Gmax, G2[n] + (rnd.randint(-15, 15) if big else rnd.randint(-3, 3))))
    s2 = evaluate(D2, G2)
    if s2 <= s:
        if s2 < s: print(f'{it} {time.time()-t0:.0f}s conflits {s2}', file=log, flush=True)
        Dm, Gm, s = D2, G2, s2
        json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/opt3_{nm}_{seed}.json', 'w'))
print('fin', it, 'itérations', s, file=log, flush=True)
