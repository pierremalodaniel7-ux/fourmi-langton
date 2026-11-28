#!/usr/bin/env python3
"""R-624 DEUX PAS ENCHAÎNÉS, LES 8 BITS, EN UN GERME (greffe, 1 usage) : les 7 modules de R-619 (chain_params.json, translations de
chain_res.json) + le module h1'' (R-620, h1pp_param.json) translaté de (X, 0). Séparation : les vaisseaux vont à 1/8 de case par pas ;
avec X = 200 000, les deux groupes restent à plus de 2·T/8 l'un de l'autre pendant toute la simulation : aucune interaction possible.
Vérification : les 256 états, moteur C, par tranches (i/k) ; les 8 sorties doivent valoir F(F(e)) et l'état final être propre.
Usage : python3 germ2.py i/k [py]  -> ligne de résultat (ajoutée à data/germ2.log par le script de lancement)"""
import sys, json, itertools, time
from chain2 import root as croot, spec2, NAMES
from chain_h1 import R as R1
from modules import VARS
from nor import Layout
from s3lib import *
X = 200000
P = json.load(open('chain_params.json')); off = {k: tuple(v) for k, v in json.load(open('chain_res.json'))['translations'].items()}
Ls = {nm: Layout(croot(nm), Dmap=P[nm]['D'], Gmap=P[nm]['G']) for nm in NAMES}
p1 = json.load(open('h1pp_param.json')); Ls['h1'] = Layout(R1, Dmap=p1['D'], Gmap=p1['G']); off['h1'] = (X, 0)
names = NAMES + ['h1']
def present(e):
    W = []
    for nm in names: W += [transwl(w, off[nm]) for w in Ls[nm].present({v: e[v] for v in Ls[nm].vars})]
    return W
out = {nm: transwl(Ls[nm].out, off[nm]) for nm in names}
T = max(L.tmax for L in Ls.values()) + 1200
if __name__ == '__main__':
    i, k = map(int, sys.argv[1].split('/')); py = len(sys.argv) > 2
    envs = [dict(zip(VARS, b)) for b in itertools.product((0, 1), repeat=8)][i::k]
    sits = [sit_wls(present(e)) for e in envs]; t0 = time.time(); Rr = run_c(sits, T); good = clean = same = 0
    for e, s, (a, c) in zip(envs, sits, Rr):
        d = decode(a, c, T)
        if d is None: continue
        clean += 1; good += all(int(out[nm] in d) == spec2(nm, e) for nm in names)
        if py: pa, pc = run_py(s, T); same += sorted(pa) == sorted(a) and sorted(pc) == sorted(c)
    print(json.dumps(dict(tranche=sys.argv[1], cas=len(envs), propres=clean, justes=good, deux_moteurs=same if py else None,
                          vaisseaux_max=max(len(present(e)) for e in envs), T=T, secondes=round(time.time() - t0))), flush=True)
