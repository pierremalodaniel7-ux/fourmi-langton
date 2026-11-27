#!/usr/bin/env python3
"""R-610 Recherche des longueurs (D, G) ET des côtés, mutations CIBLÉES sur les nœuds en conflit (et leurs ancêtres), recuit (accepte parfois pire) : descente sur le nombre de conflits EXACTS par cas (diag2.conflicts2, seuil 7),
grandes échelles ; dès que les conflits sont ≤ 3, simulation de tous les cas (moteur C) ; arrêt au 1er placement juste et propre partout.
Usage : python3 opt4.py module graine secondes [départ.json]"""
import sys, json, random, time
from modules import module, nodes
from nor import *
from diag2 import conflicts2
nm, seed, secs = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
Dmax, Gmax = 300, 60
root0 = module(nm); names = [n.name for n in nodes(root0)]
def build(F):
    import copy
    r = copy.deepcopy(root0)
    for n in nodes(r):
        if F.get(n.name): n.inputs = [('-' if sd == '+' else '+', it) for sd, it in n.inputs]
    return r
rnd = random.Random(seed)
if len(sys.argv) > 4:
    p = json.load(open(sys.argv[4])); Dm, Gm = p['D'], p['G']
    Fm = p.get('F', {n: 0 for n in names})
else:
    Dm = {n: rnd.randint(8, Dmax) for n in names}; Gm = {n: rnd.randint(8, Gmax) for n in names}; Fm = {n: rnd.randint(0, 1) for n in names}
import math
par = {}
for n in nodes(root0):
    for _, it in n.inputs:
        if not isinstance(it, str): par[it.name] = n.name
def owner(o): return o if o in par or o == root0.name else o.split('@')[1][:-1]
def evaluate(Dm, Gm, Fm):
    c = conflicts2(Layout(build(Fm), Dmap=Dm, Gmap=Gm)); hot = set()
    for x in c:
        for o in (x[0], x[2]):
            n = owner(o)
            while n is not None: hot.add(n); n = par.get(n)
    return len(c), sorted(hot)
(s, hot) = evaluate(Dm, Gm, Fm); best = s; t0 = time.time(); it = 0; tested = set()
log = open(f'data/opt6_{nm}_{seed}.log', 'a'); print('départ', s, file=log, flush=True)
while time.time() - t0 < secs:
    it += 1; D2, G2, F2 = dict(Dm), dict(Gm), dict(Fm)
    for _ in range(rnd.choice((1, 1, 2, 3))):
        n = rnd.choice(hot) if hot and rnd.random() < 0.7 else rnd.choice(names); big = rnd.random() < 0.3
        if rnd.random() < 0.15: F2[n] = 1 - F2[n]
        elif rnd.random() < 0.6: D2[n] = max(8, min(Dmax, D2[n] + (rnd.randint(-60, 60) if big else rnd.randint(-8, 8))))
        else: G2[n] = max(8, min(Gmax, G2[n] + (rnd.randint(-15, 15) if big else rnd.randint(-3, 3))))
    s2, hot2 = evaluate(D2, G2, F2); temp = max(0.05, 1.5 * (1 - (time.time() - t0) / secs))
    if s2 <= s or rnd.random() < math.exp(-(s2 - s) / temp):
        if s2 < best: best = s2; print(f'{it} {time.time()-t0:.0f}s conflits {s2}', file=log, flush=True)
        Dm, Gm, Fm, s, hot = D2, G2, F2, s2, hot2
        if s == best: json.dump(dict(D=Dm, G=Gm, F=Fm, conflits=s), open(f'data/opt6_{nm}_{seed}.json', 'w'))
        key = json.dumps([Dm, Gm, Fm], sort_keys=True)
        if s <= 3 and key not in tested:
            tested.add(key); L = Layout(build(Fm), Dmap=Dm, Gmap=Gm); r = L.check()
            bad = sum(1 for x in r if x[2] != x[3]); dirty = sum(1 for x in r if not x[1])
            print(f'   simulation : {bad} faux, {dirty} sales / {len(r)}', file=log, flush=True)
            if bad == 0 and dirty == 0:
                json.dump(dict(D=Dm, G=Gm, F=Fm, a=0, conflits=s), open(f'data/opt6_{nm}_OK_{seed}.json', 'w')); break
print('fin', it, 'itérations', s, file=log, flush=True)
