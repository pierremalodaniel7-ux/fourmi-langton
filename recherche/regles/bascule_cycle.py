#!/usr/bin/env python3
"""R-342 Cycle de bascule SANS MÉMOIRE DE L'HISTOIRE : « mise à 1 (ou pas) à l'instant es, puis remise à 0 à l'instant er ».
On cherche (bascule, es mod p, er) tels que :
 (A) mise à 1 puis remise à 0 → l'objet est EXACTEMENT celui qu'on aurait sans rien faire (M non dérangé, même phase) ;
 (B) remise à 0 seule (le bit valait 0) → idem, et le vaisseau ressort propre ;
 (C) lecture : le vaisseau de remise à 0 ne ressort pas au même endroit dans les deux cas (sinon le cycle n'apprend rien).
Alors un cycle se répète à l'identique quelle que soit la suite des bits (l'état de départ de chaque cycle ne dépend pas de l'histoire).
Usage : python3 bascule_cycle.py"""
import json, sys
from hx import step, PHASES
from exp_osc import setup, hd, parse
import ecran
F = json.load(open('data/bascules_RS.json'))
def kv(s): return dict(x.split('=') for x in s.split()[1:] if '=' in x)
def kit(osc, f):
    E = setup(osc, int(f['r']), int(f['l']), int(f['ph']), int(f['ord']))
    sh = E['ants'][-1] if int(f['ord']) == 0 else E['ants'][0]
    return ([list(sh)], {c: 1 for c in E['g'] if c not in E['states'][int(f['ph'])][1]}), int(f['ph']), E['T'], int(f['ord'])
def backx(Kt, e):
    m = (e + 7) // 8; a, g = ecran.back(Kt[0], Kt[1], 8 * m); A = [list(x) for x in a]; G_ = dict(g)
    for _ in range(8 * m - e): step(A, G_)
    return A, G_
def run(R, kits, T):
    a0, c0 = parse(R); A = [list(x) for x in a0]; g = {c: 1 for c in c0}
    for Kt, e in kits:
        a, gg = backx(Kt, e); A += a; g.update(gg)
    for _ in range(T): step(A, g)
    return A, g
def near(A, g, rad=10):
    return sorted(tuple(a) for a in A if hd(a[0], a[1]) <= rad), sorted(c for c in g if hd(*c) <= rad)
def far_ships(A, g, rad=10):
    out = []
    for a in A:
        if hd(a[0], a[1]) > rad:
            nb = frozenset((c[0] - a[0], c[1] - a[1]) for c in g if hd(c[0] - a[0], c[1] - a[1]) <= 2)
            out.append((tuple(a), PHASES.get((a[2], nb))))
    return sorted(out)
res = []
for idx, X in enumerate(F):
    pass
    f1, f2 = kv(X['s1']), kv(X['s2'])
    if int(f1['ord']) or int(f2['ord']): continue
    K1, ph1, T1, _ = kit(X['R'], f1); K2, ph2, T2, _ = kit(X['R2'], f2)
    p2 = int(f2['p'])
    # es ≡ ph1 (mod 21) : es = ph1 (+ 21 k pour laisser du temps) ; er : R' (créé en es + T1 à la phase 0 de son orbite) doit être en phase ph2
    p1 = int(f1['p']); es = ph1 + p1 * (840 // p1 + 1)
    OR2 = {(tuple(sorted(map(tuple, a))), tuple(sorted(c))) for a, c in [parse(X['R2'])]}
    for k in range(0, p1 * p2):
        er = es + T1 + k
        if k % p2 != ph2: continue
        T = er + T2 + 400
        A1, g1 = run(X['R'], [(K1, es), (K2, er)], T)       # bit 1
        A0, g0 = run(X['R'], [(K2, er)], T)                 # bit 0
        An, gn = run(X['R'], [], T)                         # rien
        okA = near(A1, g1) == near(An, gn); okB = near(A0, g0) == near(An, gn)
        if okA and okB:     # la mise à 1 a-t-elle VRAIMENT eu lieu ? (objet = R' juste après l'expérience de mise à 1)
            Am, gm = run(X['R'], [(K1, es)], es + T1)
            if (tuple(near(Am, gm)[0]), tuple(near(Am, gm)[1])) not in OR2: okA = False
        s1 = far_ships(A1, g1); s0 = far_ships(A0, g0)
        clean = all(s[1] for s in s1) and all(s[1] for s in s0)
        okC = s1 != s0
        if okA and okB and clean:
            res.append({'i': idx, 'es': es, 'er': er, 'lecture_differente': okC, 'sorties1': s1, 'sorties0': s0, 'X': X})
            print('cycle trouvé : bascule', idx, 'es', es, 'er', er, 'lecture', okC, s1, s0); sys.stdout.flush()
            break
print('cycles sans mémoire de l\'histoire :', len(res))
json.dump(res, open('data/bascule_cycles.json', 'w'))
