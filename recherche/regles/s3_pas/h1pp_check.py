#!/usr/bin/env python3
"""R-620 vérification d'un placement de l'arbre h1'' enchaîné (chain_h1.R) : simulation moteur C (et hx.py en option) de cas
choisis ; sortie lue = puissance racine tout droit ; attendu = h1 après 2 pas (spec2). Usage : python3 h1pp_check.py params.json [n_cas|all] [py]"""
import sys, json, itertools, random, time
from chain_h1 import R, spec2
from modules import VARS
from nor import Layout
from s3lib import *
p = json.load(open(sys.argv[1])); L = Layout(R, Dmap=p['D'], Gmap=p['G'])
full = [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)]
n = sys.argv[2] if len(sys.argv) > 2 else '8'
cases = full if n == 'all' else ([full[i] for i in range(int(n.split('/')[0]), 256, int(n.split('/')[1]))] if '/' in n else random.Random(0).sample(full, int(n)))
t0 = time.time(); T = L.tmax + 1200
r = L.check(envs=[{v: e[v] for v in L.vars} for e in cases], T=T, engine2=len(sys.argv) > 3)
bad = sum(1 for (e, c, got, val, same), ee in zip(r, cases) if got != spec2('h1', ee)); dirty = sum(1 for x in r if not x[1])
same = sum(1 for x in r if x[4])
print(f"h1'' [{n}] : {len(r)} cas, {dirty} sales, {bad} faux, 2 moteurs {same}/{len(r) if len(sys.argv) > 3 else 0}, tmax {L.tmax}, {len(L.ships)} vaisseaux — {time.time()-t0:.0f} s", flush=True)
