#!/usr/bin/env python3
"""R-308 Murs : lignes de L cases (pleines ou pointillées) le long de chaque axe du réseau, centrées près de la voie de B
(décalage 0..5 le long de D), L = 5, 9, 17, 33. Issues de B : direction de sortie, voie ; puis réutilisation (2e autoroute
10 périodes derrière). Usage : python3 murs.py REGLE"""
import sys, json, collections
from banc import launcher, sit, path, outcome, K, TB
from outils_r import lot
G = json.load(open('data/germes_regles.json'))
rule = sys.argv[1]; g = G[rule]; P, D = g['P'], tuple(g['D'])
ant, cells = launcher(g); t2 = K * P
X = path(rule, [ant], cells, t2, t2)[0][:2]
sol = outcome(rule, lot([sit(rule, [ant], cells)], TB)[0], 0, P, D)
axes = [(1,0),(0,1),(1,1),(1,-1)] if not rule.startswith(('H:','T:')) else [(1,0),(0,1),(1,-1)] if rule.startswith('H:') else [(1,0),(0,1)]
confs = []
for ax in axes:
    for L in (5, 9, 17, 33):
        for pas in (1, 2):
            for off in range(6):
                c0 = (X[0] + off * (1 if D[0] > 0 else -1 if D[0] < 0 else 0), X[1] + off * (1 if D[1] > 0 else -1 if D[1] < 0 else 0))
                w = [(c0[0] + k * ax[0], c0[1] + k * ax[1]) for k in range(-(L // 2), L // 2 + 1, pas)]
                confs.append(((ax, L, pas, off), w))
lines = []
for key, w in confs:
    c = dict(cells); [c.__setitem__(v, 1) for v in w]; lines.append(sit(rule, [ant], c))
res = [outcome(rule, l, 0, P, D) for l in lot(lines, TB)]
st = collections.Counter()
for (key, w), o in zip(confs, res):
    st[(o[0], o[1], (o[1] == 0 and o[2] == sol[2]) if o[0] == 'propre' else None)] += 1
print(rule, 'murs', len(confs), {str(k): v for k, v in st.most_common()})
# réutilisation des murs qui dévient (direction ≠ 0)
m = 10; a2, c2 = launcher(g, 0, (m * D[0], m * D[1]))
L2 = []; meta = []
for (key, w), o in zip(confs, res):
    if o[0] == 'propre' and o[1] not in (0, None):
        c = dict(cells); c.update(c2); [c.__setitem__((v[0] + m * D[0], v[1] + m * D[1]), 1) for v in w]
        L2.append(sit(rule, [ant, a2], c)); meta.append((key, o))
ok = 0; same = 0; ex = []
for l, (key, o) in zip(lot(L2, TB) if L2 else [], meta):
    ob, oa = outcome(rule, l, 0, P, D), outcome(rule, l, 1, P, D)
    if ob[0] == 'propre' and oa[0] == 'propre' and ob[1] == oa[1]:
        same += 1
        if ob[2] == oa[2]: ok += 1; ex.append(key)
print(f"  murs déviants {len(L2)} : 2e autoroute même direction {same}, même voie {ok}", ex[:5])
json.dump({'regle': rule, 'stat': {str(k): v for k, v in st.items()}, 'deviants': len(L2), 'meme_dir': same, 'reutilisables': ok, 'exemples': ex},
          open('data/murs_' + rule.replace(':', '_') + '.json', 'w'), default=str)
