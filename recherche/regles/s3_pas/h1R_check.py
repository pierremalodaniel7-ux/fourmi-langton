#!/usr/bin/env python3
"""R-616 Vérification complète du module h1' réutilisable (htree.h1_tree2) : 256 cas (2 moteurs), certificat (cert2), 20 usages ×3.
Usage : python3 h1R_check.py h1R_param_3.json"""
import sys, json, random, time
from htree import build, h1_tree2
from nor import Layout
from modules import spec, VARS
from cert2 import certificate2
from reuse import check_multi
p = json.load(open(sys.argv[1])); L = Layout(build(h1_tree2()), Dmap=p['D'], Gmap=p['G']); t0 = time.time()
r = L.check(engine2=True)
ok = sum(1 for x in r if x[1] and x[2] == x[3] == spec('h1', {**{v: 0 for v in VARS}, **x[0]})); n2 = sum(1 for x in r if x[4])
print(f'{sys.argv[1]} : {len(r)} cas, {ok} justes et propres, 2 moteurs {n2}/{len(r)}, tmax {L.tmax} ({time.time()-t0:.0f} s)', flush=True)
try: okc, delta, info = certificate2(L, log=lambda s: print(s, flush=True))
except AssertionError as ex: print('certificat : échec', str(ex)[:300], flush=True); sys.exit()
res = dict(fichier=sys.argv[1], cas=len(r), justes=ok, deux_moteurs=n2, certificat=okc, delta=delta, fenetre=info['span'], rayon=info['R'], voies_opposees=info['opposees'])
if okc:
    D = delta + (-delta) % 8; res['usages20'] = []
    for seed in range(3):
        rnd = random.Random(seed); seq = [rnd.choice(L.cases()) for _ in range(20)]
        sup, good, same, nf = check_multi(L, seq, D, engine2=False)
        res['usages20'].append(dict(graine=seed, superposition=sup, justes=good, deux_moteurs=same, fourmis=nf))
        print(f'20 usages (graine {seed}, Δ = {D}) : superposition {sup}, {good}/20 justes, 2 moteurs {same}, {nf} fourmis', flush=True)
    sup, good, same, nf = check_multi(L, seq[:3], D, engine2=True)
    res['usages3_deux_moteurs'] = dict(superposition=sup, justes=good, deux_moteurs=same, fourmis=nf)
    print(f'3 usages, 2 moteurs : superposition {sup}, {good}/3 justes, 2 moteurs {same}', flush=True)
json.dump(res, open(sys.argv[1].replace('param', 'verif'), 'w'), ensure_ascii=False, indent=1)
