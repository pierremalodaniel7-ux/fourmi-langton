#!/usr/bin/env python3
"""S1 / R-400 Vérification directe des fusions candidates de fusion1.py (simulation des 3 cas dans le repère absolu, 2 moteurs).
Cas 0 : K seul ; cas 1 : K + s1 ; cas 2 : K + s2. Fusion propre : 0 case restante dans chaque cas, O présent dans les cas 1 et 2
(même trajectoire exacte), absent du cas 0, et s1, s2 de routes différentes.
Usage : python3 s1_fusion/fusion1v.py"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from hx import ship_dir, step, rot
from fa_lib import decode, back, lotdump, sit, pyrun
D = json.load(open(os.path.join(HERE, 'fusion1.json')))
res, fus = D['res'], D['fus']; T = D['T']
KP = (tuple(D['K'][0]), [tuple(c) for c in D['K'][1]])
dB = ship_dir(0)
def w_of(r):
    d = ship_dir(r); return (dB[0] - d[0], dB[1] - d[1])
def piece(c, m=0):
    (x, y, h), cs = c['s']; w = w_of(c['r'])
    return ((x + m * w[0], y + m * w[1], h), [(a + m * w[0], b + m * w[1]) for a, b in cs])
def route(p):
    s = decode([tuple(p[0])], [tuple(c) for c in p[1]]); return s[0][:2]
BK = 60; TT = T + 8 * BK + 8 * 200
cands = []; seen = set()
for f in fus:
    (i1, j1, m1), (i2, j2, m2) = f['a'], f['b']
    c1, c2 = res[i1], res[i2]
    s1 = piece(c1, 0); s2 = piece(c2, m1 - m2)
    if route(s1) == route(s2): continue          # même route (au mieux deux horaires d'un même fil) : pas une fusion de deux routes
    k = (tuple(map(tuple, [s1[0], *s1[1]])), tuple(map(tuple, [s2[0], *s2[1]])), c1['order'], c2['order'])
    if k in seen: continue
    seen.add(k); cands.append((f, s1, s2, c1['order'], c2['order']))
print('candidats à routes distinctes :', len(cands), flush=True)
def lay(pcs):  # recule tout de BK périodes (même décalage de temps pour tous) puis situation
    return sit([back(p, BK) for p in pcs])
L = []
for f, s1, s2, o1, o2 in cands:
    L += [lay([KP]), lay([s1, KP] if o1 == 0 else [KP, s1]), lay([s2, KP] if o2 == 0 else [KP, s2])]
R = lotdump(L, TT)
ok = []; why = collections.Counter()
for n, (f, s1, s2, o1, o2) in enumerate(cands):
    d0, d1, d2 = [decode(*R[3 * n + q]) for q in range(3)]
    if None in (d0, d1, d2): why['sale'] += 1; continue
    com = set(map(tuple, d1)) & set(map(tuple, d2))
    com -= set(map(tuple, d0))
    if not com: why['pas de sortie commune'] += 1; continue
    O = sorted(com)[0]
    ok.append(dict(s1=s1, s2=s2, o1=o1, o2=o2, O=O, out0=d0, out1=d1, out2=d2, r1=route(s1), r2=route(s2)))
print('fusions VÉRIFIÉES (fourmi_r) :', len(ok), dict(why), flush=True)
# 2e moteur sur toutes
bad = 0
for n, z in enumerate(ok):
    for q, pcs in enumerate(([KP], [z['s1'], KP] if z['o1'] == 0 else [KP, z['s1']], [z['s2'], KP] if z['o2'] == 0 else [KP, z['s2']])):
        a, c = pyrun(lay(pcs), TT)
        if sorted(map(tuple, decode(a, c))) != sorted(map(tuple, z['out%d' % q])): bad += 1
print('2e moteur (hx.py) : désaccords', bad)
c = collections.Counter((z['r1'][0], z['r2'][0], z['O'][0]) for z in ok)
print('(dir s1, dir s2, dir O) :', c.most_common())
json.dump(ok, open(os.path.join(HERE, 'fusion1_ok.json'), 'w'))
