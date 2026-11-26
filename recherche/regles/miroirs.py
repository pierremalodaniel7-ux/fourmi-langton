#!/usr/bin/env python3
"""R-307 Miroirs réutilisables : obstacles de 1 à 3 cases (couleur 1) dans une fenêtre 5×5 centrée sur la voie de B
(K périodes devant). Pour chaque obstacle qui DÉVIE B proprement, on envoie 2 autoroutes sur la même voie (A devant de m
périodes, B derrière) : B sort-elle exactement comme A (même direction, même voie) ? Usage : python3 miroirs.py REGLE [W]"""
import sys, json, itertools, collections
from banc import launcher, sit, path, outcome, lane, K, TB
from outils_r import lot, parse
G = json.load(open('data/germes_regles.json'))
rule = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 2
g = G[rule]; P, D = g['P'], tuple(g['D'])
ant, cells = launcher(g)
t2 = K * P
X = path(rule, [ant], cells, t2, t2)[0][:2]
sol = outcome(rule, lot([sit(rule, [ant], cells)], TB)[0], 0, P, D)
win = [(X[0] + i, X[1] + j) for i in range(-W, W + 1) for j in range(-W, W + 1)]
confs = [s for k in (1, 2, 3) for s in itertools.combinations(win, k)]
lines = []
for s in confs:
    c = dict(cells); [c.__setitem__(v, 1) for v in s]; lines.append(sit(rule, [ant], c))
res = [outcome(rule, l, 0, P, D) for l in lot(lines, TB, ncpu=2)]
stat = collections.Counter((o[0], o[1] if o[0] == 'propre' else None, (o[1] == 0 and o[2] == sol[2]) if o[0] == 'propre' else None) for o in res)
defl = [(s, o) for s, o in zip(confs, res) if o[0] == 'propre' and not (o[1] == 0 and o[2] == sol[2])]
print(rule, 'obstacles', len(confs), 'issues', dict(stat))
# réutilisation
out = []
for m in (3, 10):
    a2, c2 = launcher(g, 0, (m * D[0], m * D[1]))
    L = []; meta = []
    for s, o in defl:
        c = dict(cells); c.update(c2)
        for v in s: c[(v[0] + m * D[0], v[1] + m * D[1])] = 1
        L.append(sit(rule, [ant, a2], c)); meta.append((s, o))
    R = lot(L, TB, ncpu=2) if L else []
    for l, (s, o) in zip(R, meta):
        ob, oa = outcome(rule, l, 0, P, D), outcome(rule, l, 1, P, D)
        out.append({'m': m, 'obst': s, 'seul': o, 'A': oa, 'B': ob, 'reutilisable': ob[0] == 'propre' and oa[0] == 'propre' and ob[1] == oa[1] and ob[2] == oa[2],
                    'meme_dir': ob[0] == 'propre' and oa[0] == 'propre' and ob[1] == oa[1], 'sit': l.split('|')[0:3]})
for m in (3, 10):
    sub = [x for x in out if x['m'] == m]
    print(f"  m={m} déviants {len(sub)} : B même direction que A {sum(x['meme_dir'] for x in sub)}, même voie (réutilisable) {sum(x['reutilisable'] for x in sub)}")
json.dump({'regle': rule, 'X': X, 'n': len(confs), 'issues': {str(k): v for k, v in stat.items()}, 'reuse': out},
          open('data/miroirs_' + rule.replace(':', '_') + '.json', 'w'), default=str)
