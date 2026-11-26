#!/usr/bin/env python3
"""S1 / R-400 FUSION de deux signaux exclusifs avec UN vaisseau constant K (recherche exhaustive).
K = vaisseau direction 0 (canonique, comme B dans chocs_exhaustif). Un signal s (direction r = 1..5, avance tau, position v modulo u,
2 ordres de jeu) rencontre K : issue = liste de vaisseaux sortants (trajectoires exactes). Symétrie sigma : décaler s de 8 pas et de -d_K
redonne le même choc décalé (sigma laisse K invariant) ⇒ on travaille modulo sigma : une trajectoire de direction r et point de référence
g est rangée par g modulo w_r = d_K - d_r.
FUSION = deux signaux s1 ≠ s2 dont les chocs avec K émettent CHACUN un vaisseau sur la MÊME trajectoire O (même direction, voie, instant,
phase), O ≠ trajectoire de K seul (sinon le cas « aucun signal » donnerait 1), chocs propres (0 case).
On ajoute le cas « s1 = O prolongé en arrière » (s1 qui traverse K ou le percute et ressort sur sa propre route).
Usage (depuis recherche/regles) : python3 s1_fusion/fusion1.py"""
import sys, os, json, collections, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from hx import ship, ship_dir, step, PHASES, rot
from chocs_exhaustif_lib import hd, RAD, DMAX
from demi_add_k import OFFS
KP = 25; T0 = 8 * KP; T = 2 * T0 + 8 * 60
dB = ship_dir(0)
def germ(r, pos, tau):
    a, c = ship(r, pos); ants = [list(a)]; g = {c: 1}
    for _ in range(tau): step(ants, g)
    return ants[0], g
def decodeg(ants, cells):
    """vaisseaux (r, phase, gx, gy) ; None si une fourmi n'est pas un vaisseau propre ou s'il reste des cases"""
    out = []; used = set(); cs = set(cells)
    for x, y, h in ants:
        near = frozenset((p[0] - x, p[1] - y) for p in cs if hd(p[0] - x, p[1] - y) <= 2)
        k = PHASES.get((h, near))
        if not k: return None
        r, ph = k; out.append((r, ph, x - OFFS[(r, ph)][0], y - OFFS[(r, ph)][1])); used |= {(x + a, y + b) for a, b in near}
    if cs - used: return None
    return out
def w_of(r):
    d = ship_dir(r); return (dB[0] - d[0], dB[1] - d[1])
def key(o):
    """forme canonique modulo sigma (+ l'exposant m : o = sigma^m(clé))"""
    r, ph, gx, gy = o; w = w_of(r)
    if w == (0, 0): return (r, ph, gx, gy), 0
    f = lambda p: 7 * p[0] + 3 * p[1]          # fonctionnelle avec f(w) ≠ 0 pour les 5 vecteurs w
    fw = f(w); assert fw != 0
    m = f((gx, gy)) // fw                     # plancher : reste dans [0, fw) ou (fw, 0], unique
    return (r, ph, gx - m * w[0], gy - m * w[1]), m
def run(ants, g, n):
    for _ in range(n): step(ants, g)
    return ants, g
KA, KG = germ(0, (-KP * dB[0], -KP * dB[1]), 0)
Kout = decodeg(*run([list(KA)], dict(KG), T))[0]
Kkey = key(Kout)[0]
res = []; t0 = time.time()
for r in range(1, 6):
    dA = ship_dir(r); u = (dA[0] - dB[0], dA[1] - dB[1])
    reps = {}
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
            # transparence exacte ?
            a1, g1 = [list(sA)], dict(gA); a2, g2 = [list(KA)], dict(KG); dmin = 99
            for _ in range(2 * T0):
                step(a1, g1); step(a2, g2); dmin = min(dmin, hd(a1[0][0] - a2[0][0], a1[0][1] - a2[0][1]))
            if dmin > DMAX: continue
            sin = decodeg([list(sA)], list(gA))[0]
            for order in (0, 1):
                ants = [list(sA), list(KA)] if order == 0 else [list(KA), list(sA)]
                g = dict(gA); g.update(KG)
                run(ants, g, T)
                d = decodeg(ants, sorted(g))
                if d is None or len(d) != 2: continue
                if hd(ants[0][0] - ants[1][0], ants[0][1] - ants[1][1]) <= DMAX + 6: continue
                res.append(dict(r=r, tau=tau, v=v, order=order, s=(list(sA), sorted(gA)), sin=sin, out=d))
print('chocs propres (2 vaisseaux) :', len(res), round(time.time() - t0), 's', flush=True)
# index des sorties modulo sigma
idx = collections.defaultdict(list)
for i, c in enumerate(res):
    for j, o in enumerate(c['out']):
        kq, m = key(o)
        if kq == Kkey: continue                    # sortie = route de K seul : inutilisable
        idx[kq].append((i, j, m))
fus = []
for kq, L in idx.items():
    for a in range(len(L)):
        for b in range(a + 1, len(L)):
            i1, j1, m1 = L[a]; i2, j2, m2 = L[b]
            c1, c2 = res[i1], res[i2]
            # s1 = rep i1 (m = 0 → sortie sigma^m1 clé) ; s2 = sigma^(m1-m2) rep i2 ; même signal ? (même rep et m1 = m2 : même trajectoire)
            if (c1['r'], c1['tau'], tuple(c1['v'])) == (c2['r'], c2['tau'], tuple(c2['v'])) and m1 == m2: continue
            fus.append(dict(key=kq, a=(i1, j1, m1), b=(i2, j2, m2)))
print('paires de chocs à sortie commune (fusions candidates) :', len(fus), flush=True)
cnt = collections.Counter((res[f['a'][0]]['r'], res[f['b'][0]]['r'], f['key'][0]) for f in fus)
print('(r1, r2, r_sortie) :', cnt.most_common(30))
json.dump(dict(res=res, fus=fus, K=[list(KA), sorted(KG)], T=T), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fusion1.json'), 'w'))
