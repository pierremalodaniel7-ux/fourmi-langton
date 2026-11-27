#!/usr/bin/env python3
"""R-619 Longueurs (D, G) d'un module ENCHAÎNÉ (chain2.py) : descente sur les conflits exacts par cas (diag2, seuil 7), comme opt7 ;
dès que conflits ≤ SIM (défaut 6), simulation de tous les cas (moteur C) ; arrêt au 1er placement juste (spécification 2 pas) et propre.
Usage : python3 optc.py module graine secondes [départ.json]  -> data/optc_<module>_OK_<graine>.json"""
import sys, json, random, time, os
from modules import nodes, VARS
from chain2 import root as croot, spec2
from nor import Layout
from diag2 import conflicts2
nm, seed, secs = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]); SIM = int(os.environ.get('SIM', 6))
Dmax, Gmax = 300, 60
R = croot(nm); names = [n.name for n in nodes(R)]; rnd = random.Random(seed)
if len(sys.argv) > 4: p = json.load(open(sys.argv[4])); Dm, Gm = p['D'], p['G']
else: Dm = {n: rnd.randint(8, Dmax) for n in names}; Gm = {n: rnd.randint(8, Gmax) for n in names}
def evaluate(Dm, Gm): return len(conflicts2(Layout(R, Dmap=Dm, Gmap=Gm)))
def good(L):
    r = L.check(); z = {v: 0 for v in VARS}
    bad = sum(1 for e, cl, got, val, _ in r if got != spec2(nm, {**z, **e})); dirty = sum(1 for x in r if not x[1]); return bad, dirty, len(r)
s = evaluate(Dm, Gm); t0 = time.time(); it = 0; tested = set()
log = open(f'data/optc_{nm}_{seed}.log', 'a'); print('départ', s, file=log, flush=True)
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
        json.dump(dict(D=Dm, G=Gm, conflits=s), open(f'data/optc_{nm}_{seed}.json', 'w'))
        key = json.dumps([Dm, Gm], sort_keys=True)
        if s <= SIM and key not in tested:
            tested.add(key); L = Layout(R, Dmap=Dm, Gmap=Gm); bad, dirty, n = good(L)
            print(f'   simulation : {bad} faux, {dirty} sales / {n}', file=log, flush=True)
            if bad == 0 and dirty == 0:
                json.dump(dict(D=Dm, G=Gm, a=0, conflits=s, module=nm), open(f'data/optc_{nm}_OK_{seed}.json', 'w')); break
print('fin', it, 'itérations', s, f'{time.time()-t0:.0f}s', file=log, flush=True)
