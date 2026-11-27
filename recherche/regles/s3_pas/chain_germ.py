#!/usr/bin/env python3
"""R-619 Deux pas enchaînés EN UN GERME : les 7 modules enchaînés h0'', x'', y'', c00''..c11'' (chain2.py, longueurs de optc.py)
(1) chaque module seul : tous ses cas, 2 moteurs, comparé à F∘F ; (2) les 7 côte à côte (translations de step.py, 1 usage) :
les 256 états, moteur C puis hx.py ; les 7 sorties doivent valoir F(F(e)).
Usage : NOLANES=1 BOX=3000 python3 chain_germ.py [graine]  -> chain_res.json (+ paramètres chain_params.json)"""
import sys, json, itertools, time, glob, os
from chain2 import root as croot, spec2, NAMES
from modules import VARS
from nor import Layout
from s3lib import *
from step import choose_offsets2
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
P = {}
for nm in NAMES:
    f = sorted(glob.glob(f'data/optc_{nm}_OK_*.json'))
    if f: P[nm] = json.load(open(f[0])); P[nm]['fichier'] = f[0]
names = [n for n in NAMES if n in P]; print('modules :', names, flush=True)
json.dump(P, open('chain_params.json', 'w'), indent=0)
Ls = {nm: Layout(croot(nm), Dmap=P[nm]['D'], Gmap=P[nm]['G']) for nm in names}
res = dict(modules={})
z = {v: 0 for v in VARS}
for nm in names:
    L = Ls[nm]; t0 = time.time(); r = L.check(engine2=True)
    ok = sum(1 for e, cl, got, val, same in r if cl and got == spec2(nm, {**z, **e})); n2 = sum(1 for x in r if x[4])
    nK = sum(1 for _, k, _ in L.ships if k == 'K'); nl = sum(1 for _, k, _ in L.ships if k == 'lit')
    res['modules'][nm] = dict(cas=len(r), justes=ok, deux_moteurs=n2, puissances=nK, litteraux=nl, tmax=L.tmax, vars=L.vars)
    print(f"{nm}'' seul : {len(r)} cas, {ok} justes et propres (= F∘F), 2 moteurs {n2}/{len(r)} ; {nK} puissances, {nl} littéraux ({time.time()-t0:.0f} s)", flush=True)
off = choose_offsets2(Ls, names, seed); print('translations :', off, flush=True)
def present(e):
    W = []
    for nm in names: W += [transwl(w, off[nm]) for w in Ls[nm].present(e)]
    return W
out = {nm: transwl(Ls[nm].out, off[nm]) for nm in names}
envs = [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)]
T = max(L.tmax for L in Ls.values()) + 1200
sits = [sit_wls(present(e)) for e in envs]; t0 = time.time(); R = run_c(sits, T); good = clean = 0; bad = []
for e, (a, c) in zip(envs, R):
    d = decode(a, c, T)
    if d is None: bad.append(('sale', e)); continue
    clean += 1
    if all(int(out[nm] in d) == spec2(nm, e) for nm in names): good += 1
    else: bad.append(('faux', e))
print(f'germe enchaîné, moteur C : {len(envs)} états, {clean} propres, {good} justes (les {len(names)} bits = F(F(e))) — {time.time()-t0:.0f} s', flush=True)
t0 = time.time(); same = 0
for s, (a, c) in zip(sits, R):
    pa, pc = run_py(s, T); same += sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
print(f'hx.py : {same}/{len(envs)} états finaux identiques — {time.time()-t0:.0f} s', flush=True)
nf = len(present({v: 1 for v in VARS}))
res.update(translations=off, T=T, etats=len(envs), propres=clean, justes=good, deux_moteurs=same, mauvais=bad[:5],
           vaisseaux_max=max(len(present(e)) for e in envs), sorties={nm: out[nm] for nm in names})
json.dump(res, open(sys.argv[2] if len(sys.argv) > 2 else 'chain_res.json', 'w'), ensure_ascii=False, indent=1)
