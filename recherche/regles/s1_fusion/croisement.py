#!/usr/bin/env python3
"""S1 / R-404 CROISEMENT : deux signaux dont les routes se coupent.
(a) Sans constant : parmi TOUS les chocs de 2 vaisseaux qui interagissent (fusion1.json : 1 688 chocs propres sur 1 880, R-333),
    lesquels rendent EXACTEMENT les deux trajectoires libres (même direction, voie, instant, phase) ? = croisement « par choc ».
(b) Bilan par angle : pour chaque angle (direction relative r = 1..5), quelles relations horaires (tau, v mod u) sont transparentes
    (jamais à moins de 6 : transparent exact, R-333) ou se comportent comme un croisement ; ce qui reste = horaires interdits.
Usage : python3 s1_fusion/croisement.py"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
from hx import ship, ship_dir, step
from chocs_exhaustif_lib import hd, DMAX
D = json.load(open(os.path.join(HERE, 'fusion1.json'))); res = D['res']; T = D['T']
from fusion1_lib import decodeg
KA, KG = D['K'][0], {tuple(c): 1 for c in D['K'][1]}
def free(a, g):
    A = [list(a)]; G = dict(g)
    for _ in range(T): step(A, G)
    return tuple(decodeg(A, sorted(G))[0])
Kf = free(KA, KG)
cnt = collections.Counter(); ex = []
for c in res:
    sA, cs = c['s']; f = free(sA, {tuple(x): 1 for x in cs})
    same = sorted(map(tuple, c['out'])) == sorted([f, Kf])
    cnt[(c['r'], same)] += 1
    if same: ex.append(c)
print('chocs propres qui rendent exactement les 2 trajectoires libres (croisement par choc) :', len(ex))
for r in range(1, 6): print('  r =', r, ':', cnt[(r, True)], '/', cnt[(r, True)] + cnt[(r, False)])
json.dump(ex, open(os.path.join(HERE, 'croisement_choc.json'), 'w'))
# (c) parmi les « croisements par choc », lesquels ont VRAIMENT interagi (trajectoires des fourmis différentes des trajectoires libres
#     à au moins un pas) ? — échange exact : les deux ressortent comme si de rien n'était, mais en se touchant.
def path(ants, g, n):
    A = [list(a) for a in ants]; G = dict(g); P = []
    for _ in range(n): step(A, G); P.append([tuple(a[:2]) for a in A])
    return P
real = []; per = collections.Counter(); mind = collections.Counter()
for c in ex:
    sA, cs = c['s']; gs = {tuple(x): 1 for x in cs}
    ants = [sA, KA] if c['order'] == 0 else [KA, sA]
    g = dict(gs); g.update(KG)
    Pj = path(ants, g, T)
    Ps = path([sA], gs, T); Pk = path([KA], KG, T)
    iS, iK = (0, 1) if c['order'] == 0 else (1, 0)
    touched = any(Pj[t][iS] != Ps[t][0] or Pj[t][iK] != Pk[t][0] for t in range(T))
    if touched:
        real.append(c); per[c['r']] += 1
        mind[min(hd(Ps[t][0][0] - Pk[t][0][0], Ps[t][0][1] - Pk[t][0][1]) for t in range(T))] += 1
print('dont VRAIS chocs (les fourmis se sont écartées de leur route puis l\'ont retrouvée exactement) :', len(real), dict(per))
print('distance minimale des trajectoires libres pour ces chocs :', sorted(mind.items()))
json.dump(real, open(os.path.join(HERE, 'croisement_echange.json'), 'w'))
# (d) bilan : géométries relatives (tau, v mod u, ordre) qui interagissent vraiment, par angle
# (d) TOUTES les géométries relatives proches (r, tau, v mod u, ordre ; dmin ≤ DMAX des trajectoires libres) : la paire se croise-t-elle
#     sans s'influencer (trajectoires des fourmis identiques aux trajectoires libres à chaque pas) ? Bilan selon dmin.
from hx import ship_dir as _sd
KP = 25; T0 = 8 * KP; dB = _sd(0)
def germ(r, pos, tau):
    a, c = ship(r, pos); ants = [list(a)]; g = {c: 1}
    for _ in range(tau): step(ants, g)
    return ants[0], g
tab = collections.defaultdict(collections.Counter); forb = collections.Counter()
for r in range(1, 6):
    dA = _sd(r); u = (dA[0] - dB[0], dA[1] - dB[1]); reps = {}
    for vx in range(-30, 31):
        for vy in range(-30, 31):
            best = None
            for kk in range(-60, 61):
                w = (vx + kk * u[0], vy + kk * u[1]); kq = (abs(w[0]) + abs(w[1]), w)
                if best is None or kq < best: best = kq
            reps[best[1]] = 1
    for tau in range(8):
        for v in reps:
            sA, gA = germ(r, (v[0] - KP * dA[0], v[1] - KP * dA[1]), tau)
            if hd(sA[0] - KA[0], sA[1] - KA[1]) <= DMAX + 4: continue
            Ps = path([sA], gA, 2 * T0); Pk = path([KA], KG, 2 * T0)
            dmin = min(hd(a[0][0] - b[0][0], a[0][1] - b[0][1]) for a, b in zip(Ps, Pk))
            if dmin > DMAX: continue
            for order in (0, 1):
                ants = [sA, KA] if order == 0 else [KA, sA]; g = dict(gA); g.update(KG)
                Pj = path(ants, g, 2 * T0); iS, iK = (0, 1) if order == 0 else (1, 0)
                same = all(Pj[t][iS] == Ps[t][0] and Pj[t][iK] == Pk[t][0] for t in range(2 * T0))
                tab[dmin][same] += 1
                if not same: forb[r] += 1
print('distance minimale des routes libres → (croisement exact, interaction) :')
for d in sorted(tab): print('  ', d, ':', tab[d][True], 'sans influence,', tab[d][False], 'avec')
print('géométries « interdites » (interaction) par angle r (sur 2 ordres) :', dict(forb), 'total', sum(forb.values()))
