#!/usr/bin/env python3
"""R-610 Recherche des longueurs (D, G) d'un gros module : descente sur le nombre de conflits EXACTS par cas (diag2.conflicts2, seuil 7),
grandes échelles ; dès que les conflits sont ≤ 3, simulation de tous les cas (moteur C) ; arrêt au 1er placement juste et propre partout.
Usage : python3 opt4.py module graine secondes [départ.json]"""
import sys, json, random, time
from modules import module, nodes
from nor import *
from diag2 import conflicts2
nm, seed, secs = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
Dmax, Gmax = 300, 60
root = module(nm); names = [n.name for n in nodes(root)]
rnd = random.Random(seed)
if len(sys.argv) > 4:
    p = json.load(open(sys.argv[4])); Dm, Gm = p['D'], p['G']
else:
    Dm = {n: rnd.randint(8, Dmax) for n in names}; Gm = {n: rnd.randint(8, Gmax) for n in names}
def evaluate(Dm, Gm): return len(conflicts2(Layout(root, Dmap=Dm, Gmap=Gm)))
s = evaluate(Dm, Gm); t0 = time.time(); it = 0; tested = set()
log = open(f'data/opt4_{nm}_{seed}.log', 'a'); print('départ', s, file=log, flush=True)
while time.time() - t0 < secs:
    it += 1; D2, G2 = dict(Dm), dict(Gm)
    for _ in range(rnd.choice((1, 1, 2, 3))):
        n = rnd.choice(names); big = rnd.random() < 0.3
        if rnd.random() < 0.6: D2[n] = max(8, min(Dmax, D2[n] + (rnd.randint(-60, 60) if big else rnd.randint(-8, 8))))
        else: G2[n] = max(8, min(Gmax, G2[n] + (rnd.randint(-15, 15) if big else rnd.randint(-3, 3))))
    s2 = evaluate(D2, G2)
    if s2 <= s:
        if s2 < s: print(f'{it} {time.time()-t0:.0f}s conflits {s2}', file=log, flush=True)
        Dm, Gm, s = D2, G2, s2
        json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/opt4_{nm}_{seed}.json', 'w'))
        key = json.dumps([Dm, Gm], sort_keys=True)
        if s <= 3 and key not in tested:
            tested.add(key); L = Layout(root, Dmap=Dm, Gmap=Gm); r = L.check()
            bad = sum(1 for x in r if x[2] != x[3]); dirty = sum(1 for x in r if not x[1])
            print(f'   simulation : {bad} faux, {dirty} sales / {len(r)}', file=log, flush=True)
            if bad == 0 and dirty == 0:
                json.dump(dict(D=Dm, G=Gm, a=0, conflits=s), open(f'data/opt4_{nm}_OK_{seed}.json', 'w')); break
print('fin', it, 'itérations', s, file=log, flush=True)
