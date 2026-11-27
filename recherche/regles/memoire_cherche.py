#!/usr/bin/env python3
"""R-346 Choisir une bascule (R → R' par 1 vaisseau, R' → R par 1 autre, bascule_hexa.py) que la sortie C = a∧b du demi-additionneur
R-337 (réutilisable, certifié) peut écrire : la bascule est tournée/posée sur la route de C (temps tstar) ; on exige pour les 4 cas
(a, b) : R' si a∧b, R sinon (les déchets des autres cas ne doivent pas l'abîmer) et tout propre hors de l'objet.
Usage : python3 memoire_cherche.py [tstar]"""
import sys, json, collections
from memoire_calc import *
tstar = int(sys.argv[1]) if len(sys.argv) > 1 else 1600
HA = Circuit([('K3', K3, None), ('K2', K2, None), ('B', B, 'b'), ('A', A, 'a')])
CS = (2, -28, 916, 0)
X = json.load(open('data/bascules_osc2.json'))
seen = {}
for x in X:
    f1 = kv(x['s1']); k = (x['R'], f1['r'], f1['l'], f1['ph'], f1['ord'])
    if k not in seen: seen[k] = x
print('mises à 1 distinctes :', len(seen), flush=True)
jobs = []; meta = []
for k, x in seen.items():
    f1 = kv(x['s1'])
    try: pieces, o, cen, rho, orb = place_gen(x['R'], f1, CS, 4000, tstar)
    except Exception as ex: continue
    for inp in HA.cases():
        P = (HA.parts(inp) + pieces) if o == 'avant' else (pieces + HA.parts(inp))
        jobs.append(sit(P)); meta.append((k, tuple(inp.values()), cen, rho))
T = tstar + 8 * 150
print('simulations :', len(jobs), flush=True)
R = lotdump(jobs, T)
res = collections.defaultdict(dict)
for m, r in zip(meta, R):
    k, ab, cen, rho = m; x = seen[k]
    if 'orbs' not in res[k]:
        res[k]['orbs'] = [(0, orbit_abs(x['R'], 0, (0, 0))), (1, orbit_abs(x['R2'], 0, (0, 0)))]
    # on compare dans le repère de la bascule : on ramène l'état (rotation −rho, translation)
    obj_a = [a for a in r[0] if hd(a[0] - cen[0], a[1] - cen[1]) <= 10]; obj_c = [q for q in r[1] if hd(q[0] - cen[0], q[1] - cen[1]) <= 10]
    far_a = [a for a in r[0] if a not in obj_a]; far_c = [q for q in r[1] if q not in obj_c]
    clean = decode(far_a, far_c) is not None
    res[k][ab] = (clean, obj_a, obj_c)
good = []
for k, v in res.items():
    x = seen[k]; f1 = kv(x['s1'])
    pieces, o, cen, rho, orb = place_gen(x['R'], f1, CS, 4000, tstar)
    # orbites absolues de R et R' : R et R' sont dans le repère de l'expérience → même rotation/translation que l'objet
    E = setup(x['R'], int(f1['r']), int(f1['l']), int(f1['ph']), int(f1['ord']))
    cshift = (cen[0] - rot(E['center'], rho)[0], cen[1] - rot(E['center'], rho)[1])
    orbs = [(0, orbit_abs(x['R'], rho, cshift)), (1, orbit_abs(x['R2'], rho, cshift))]
    st = {ab: (v[ab][0], which_state(v[ab][1], v[ab][2], cen, orbs)) for ab in [(0, 0), (0, 1), (1, 0), (1, 1)] if ab in v}
    if len(st) == 4 and all(c for c, s in st.values()) and [st[ab][1] for ab in [(0, 0), (0, 1), (1, 0), (1, 1)]] == [0, 0, 0, 1]:
        good.append({'R': x['R'], 'R2': x['R2'], 's1': x['s1'], 's2': x['s2'], 'centre': cen, 'rho': rho})
print('bascules écrites correctement par C (4/4) :', len(good))
json.dump(good, open('data/memoire_ok_%d.json' % tstar, 'w'))
for g in good[:5]: print(g['R'], '|', g['s1'][:90])
