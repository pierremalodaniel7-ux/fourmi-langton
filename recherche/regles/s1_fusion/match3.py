#!/usr/bin/env python3
"""S1 / R-409 Regrouper deux des 3 routes de c1 (R-405/R-407) avec une fusion du catalogue R-400 (1 constant), calcul EXACT :
pour chaque fusion z (1 529) et chaque paire ordonnée (X, Y) de routes de c1, on tourne le gadget pour que s1 suive EXACTEMENT X
(compose.attach) ; s2 suit alors Y à un glissement k près ssi gY − g(s2) = k (d1 − d2) (même direction, même phase). Écrit les
appariements dans s1_fusion/match3.json. Usage : python3 s1_fusion/match3.py"""
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from compose import attach, slide
from circuit import Circuit
from fa_lib import decode
from hx import rot, ship_dir
from fusion_reuse import make
T = 9000
D = json.load(open(os.path.join(HERE, 'fusion1.json'))); K = (tuple(D['K'][0]), [tuple(c) for c in D['K'][1]])
ok = json.load(open(os.path.join(HERE, 'fusion1_ok.json')))
V = {'V0': (0, 19, 2187, 0), 'V7': (0, 19, 2187, 7), 'V2': (2, -30, 2168, 1)}
def g(o):
    r, l, a, ph = o
    if (l + a) % 2: return None
    return rot(((l + a) // 2, (l - a) // 2), r)
def at(p, t):
    d = decode([p[0]], p[1])[0]; assert t % 8 == 0
    return (d[0], d[1], d[2] + 2 * (t // 8), d[3])
res = []
for zi, z in enumerate(ok):
    G = Circuit(make(z, K))
    for X, Y in itertools.permutations(V, 2):
        vx, vy = V[X], V[Y]
        rho = (vx[0] - z['r1'][0]) % 6
        if (z['r2'][0] + rho) % 6 != vy[0]: continue
        F = attach(G, 's1', rho, vx, T)
        if F is None: continue
        P = dict((n, p) for n, p, v in F.pieces)
        s2 = at(P['s2'], T)
        if s2[3] != vy[3]: continue
        a, b = g(s2), g(vy)
        if a is None or b is None: continue
        w = (b[0] - a[0], b[1] - a[1]); d1, d2 = ship_dir(vx[0]), ship_dir(vy[0]); dd = (d1[0] - d2[0], d1[1] - d2[1])
        # w = k dd ?
        k = None
        if dd[0]: k = w[0] // dd[0] if w[0] % dd[0] == 0 else None
        elif dd[1]: k = w[1] // dd[1] if w[1] % dd[1] == 0 else None
        if k is None or (k * dd[0], k * dd[1]) != w: continue
        F2 = slide(F, 's1', k)
        P2 = dict((n, p) for n, p, v in F2.pieces)
        assert at(P2['s1'], T) == vx and at(P2['s2'], T) == vy, (at(P2['s1'], T), at(P2['s2'], T))
        res.append(dict(z=zi, X=X, Y=Y, rho=rho, k=k, o=(z['o1'], z['o2']), typ=(z['r1'][0], z['r2'][0], z['O'][0]),
                        K=P2['K']))
        print(zi, X, Y, 'rho', rho, 'k', k, 'type', res[-1]['typ'], flush=True)
json.dump(res, open(os.path.join(HERE, 'match3.json'), 'w'))
print(len(res), 'appariements exacts')
