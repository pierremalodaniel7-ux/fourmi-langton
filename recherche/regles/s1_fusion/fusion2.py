#!/usr/bin/env python3
"""S1 / R-402 FUSION PROPRE à 2 constants : fusion « à ombre » réutilisable (R-401 : O = K décalé d'une voie, K seul sur la voie 0
dans le cas « aucun signal ») + un 2e constant K' qui SÉPARE O de son ombre K0 : on cherche K' (direction 1..5, passage près de la route
de O à l'instant t, décalage (i, j), phase tau, joué en premier ou en dernier) tel que
  - les 3 cas (aucun, x, y) soient propres (0 case) ;
  - une trajectoire O' soit présente dans les cas x et y, absente du cas « aucun », et ne soit PAS sur la direction 0 à ≤ 6 voies de
    la route de K (pas d'ombre) ;
  - aucune sortie sur l'axe d'une entrée (s1, s2, K, K') à contresens.
Puis 2 usages (9 suites, superposition exacte). Écrit au fur et à mesure dans s1_fusion/fusion2_<base>.json.
Usage : python3 s1_fusion/fusion2.py <indice de la fusion de base dans fusion_reuse2.json> [dirs]"""
import sys, os, json, itertools, time, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from fa_lib import decode, back, lotdump, sit, kship
from hx import ship_dir
from exp_osc import hd
from fusion_reuse import Excl, route, front
from circuit import check_multi
T = 4000
I = int(sys.argv[1]); dirs = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1, 2, 3, 4, 5]
F = json.load(open(os.path.join(HERE, 'fusion_reuse2.json')))[I]
pieces = [(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in F['pieces']]
O = tuple(F['O4000']); K0 = None
base = Excl(pieces)
d0 = [tuple(x) for x in decode(*lotdump([base.sit(base.cases()[0])], T)[0])]
K0 = [x for x in d0 if x[0] == 0][0]
ins = [route(p) for n, p, v in pieces]
def lane0(t, o):           # vaisseau direction 0 décodé (0, voie, abscisse, phase) au temps T → point de référence au temps t
    _, l, a, ph = o; a2 = a - 2 * ((T - t) // 8)
    # voie = X + Y, abscisse = X - Y (repère de la direction 0)
    return ((l + a2) // 2, (l - a2) // 2)
tk = 8 * (25 + 60)          # instant du choc de la fusion
cand = []
for n in range(3, 50, 3):
    t = tk + 8 * n; P = lane0(t, O)
    for rK in dirs:
        dK = ship_dir(rK)
        for i in range(-4, 5):
            for j in range(-4, 5):
                st = (P[0] - t // 8 * dK[0] + i, P[1] - t // 8 * dK[1] + j)
                for tau in range(8):
                    Kp = kship(rK, st, tau)
                    if min(hd(Kp[0][0] - p[0][0], Kp[0][1] - p[0][1]) for _, p, _ in pieces) < 12: continue
                    rk = route(Kp)
                    if any(front(rk, e) for e in ins): continue
                    for first in (0, 1): cand.append((n, rK, i, j, tau, first, Kp))
print('base', I, F['r1'], F['r2'], 'O', O, 'K0', K0, '; placements de K\' :', len(cand), flush=True)
def circ(c):
    P = list(pieces); kp = ('Kp', c[6], None)
    return Excl([kp] + P if c[5] else P + [kp])
t0 = time.time(); good = []; stats = collections.Counter()
CH = 6000
for s0 in range(0, len(cand), CH):
    part = cand[s0:s0 + CH]; Cs = [circ(c) for c in part]
    L = [C.sit(e) for C in Cs for e in C.cases()]
    R = lotdump(L, T)
    for n, (c, C) in enumerate(zip(part, Cs)):
        d = [decode(*R[3 * n + q]) for q in range(3)]
        if None in d: stats['sale'] += 1; continue
        d = [set(map(tuple, x)) for x in d]
        com = (d[1] & d[2]) - d[0]
        com = {o for o in com if not (o[0] == 0 and abs(o[1] - K0[1]) <= 6)}
        if not com: stats['pas de sortie commune sans ombre'] += 1; continue
        rk = route(c[6]); outs = {o[:2] for x in d for o in x}
        if any(front(s, e) for s in outs for e in ins + [rk]): stats['route de face'] += 1; continue
        Op = sorted(com)[0]; C.outputs = {'O': (lambda e: e['x'] | e['y'], [Op])}
        n2 = sum(1 for e1, e2 in itertools.product(C.cases(), repeat=2) if (lambda s: s[0] and s[1] == 2)(check_multi(C, [e1, e2], 200)))
        if n2 != 9: stats['2 usages < 9/9'] += 1; continue
        stats['OK'] += 1
        good.append(dict(base=I, c=c[:6], Kp=c[6], Op=Op, out=[sorted(x) for x in d], pieces=[(nn, p, v) for nn, p, v in C.pieces]))
        print('FUSION PROPRE', c[:6], 'O\' =', Op, flush=True)
    json.dump(good, open(os.path.join(HERE, 'fusion2_%d.json' % I), 'w'))
    print(f'  {s0 + len(part)}/{len(cand)}  {dict(stats)}  {round(time.time() - t0)} s', flush=True)
print('fin base', I, dict(stats))
