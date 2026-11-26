#!/usr/bin/env python3
"""R-339 Certificat : la mémoire R-335 marche pour TOUT nombre d'usages et TOUTE suite de bits (même méthode que R-338).
Un usage = (écrire b si b = 1) puis lire ; il part du pixel VIDE et y revient. Les usages sont des copies décalées de 2G = 3 200 pas
(l'écart écriture → lecture ne dépend que de t0 mod 8 = 0). Si deux usages ne passent jamais à ≤ 6 l'un de l'autre, N usages = superposition.
Usage : python3 memoire_certif.py [J]"""
import sys, itertools, json
import ecran
from hx import step, rot
from exp_osc import hd
import memoire_finale as mf          # fixe l'oscillateur et la paire (Da, Db)
pair = mf.pair; G = 1600; P = (0, 0)
J = int(sys.argv[1]) if len(sys.argv) > 1 else 20
def usage(b):
    plan = []
    if b: plan.append(('écrit', P, 0))
    plan.append(('efface', P, pair.t_erase(0, G) if b else (G + 7) // 8 * 8))
    return ecran.build(pair, plan)
W = 2 * G + 2400
def traj(ants, cells):
    A = [list(a) for a in ants]; Gd = {c: 1 for c in cells}; Pp = [[tuple(a[:2]) for a in A]]
    for t in range(W + 8): step(A, Gd); Pp.append([tuple(a[:2]) for a in A])
    vin = [(Pp[8][i][0] - Pp[0][i][0], Pp[8][i][1] - Pp[0][i][1]) for i in range(len(A))]
    vout = [(Pp[W + 8][i][0] - Pp[W][i][0], Pp[W + 8][i][1] - Pp[W][i][1]) for i in range(len(A))]
    for i in range(len(A)):
        assert all(Pp[t + 8][i] == (Pp[t][i][0] + vout[i][0], Pp[t][i][1] + vout[i][1]) for t in range(W - 64, W)), ('sortie', i)
        assert all(Pp[t + 8][i] == (Pp[t][i][0] + vin[i][0], Pp[t][i][1] + vin[i][1]) for t in range(0, 64)), ('entrée', i)
    assert not [c for c in Gd if all(hd(c[0] - a[0], c[1] - a[1]) > 2 for a in A)], 'case laissée'
    return Pp, vin, vout
def pos(T, t, i):
    Pp, vin, vout = T
    if t < 0:
        m = (-t + 7) // 8; tt = t + 8 * m; return (Pp[tt][i][0] - m * vin[i][0], Pp[tt][i][1] - m * vin[i][1])
    if t > W + 8:
        m = (t - W) // 8; tt = t - 8 * m
        if tt > W + 8: tt -= 8; m += 1
        return (Pp[tt][i][0] + m * vout[i][0], Pp[tt][i][1] + m * vout[i][1])
    return Pp[t][i]
def mind(T1, T2, shift):
    best = 10 ** 9; n1, n2 = len(T1[0][0]), len(T2[0][0]); lo = min(0, shift) - 8; hi = max(W, W + shift) + 16
    for t in range(lo, hi):
        for i in range(n1):
            p = pos(T1, t, i)
            for j in range(n2):
                q = pos(T2, t - shift, j); best = min(best, hd(p[0] - q[0], p[1] - q[1]))
    for side in (-1, 1):
        for i in range(n1):
            for j in range(n2):
                t0 = lo if side < 0 else hi
                v1 = (T1[2] if side > 0 else T1[1])[i]; v2 = (T2[2] if t0 - shift > W else T2[1] if t0 - shift < 0 else (0, 0))[j]
                if v1 == v2 and (t0 - shift > W + 8 or t0 - shift < 0): continue
                t = t0
                for _ in range(20000):
                    p, q = pos(T1, t, i), pos(T2, t - shift, j); d = hd(p[0] - q[0], p[1] - q[1]); best = min(best, d)
                    p2, q2 = pos(T1, t + side * 800, i), pos(T2, t + side * 800 - shift, j)
                    if hd(p2[0] - q2[0], p2[1] - q2[1]) > d: break
                    t += side * 8
                else: return -1
    return best
TR = {b: traj(*usage(b)) for b in (0, 1)}
worst = 10 ** 9
for jj in range(1, J + 1):
    d = min(mind(TR[b1], TR[b2], jj * 2 * G) for b1, b2 in itertools.product((0, 1), (0, 1))); worst = min(worst, d)
    if jj <= 3 or jj == J: print(f'écart de {jj} usage(s) : distance minimale = {d}')
print('distance minimale sur les écarts 1 …', J, ':', worst, '→', 'CERTIFIÉ (> 6)' if worst > 6 else 'à examiner')
json.dump({'J': J, 'distance_min': worst}, open('resumes/memoire_certif.json', 'w'))
def droite(T, i, out):
    Pp, vin, vout = T; v = vout[i] if out else vin[i]; p = Pp[W][i] if out else Pp[0][i]
    r = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)].index(v); X, Y = rot(p, -r % 6); return r, X + Y
S_ = {droite(TR[b], i, True) for b in (0, 1) for i in range(len(TR[b][0][0]))}
E_ = {droite(TR[b], i, False) for b in (0, 1) for i in range(len(TR[b][0][0]))}
print('routes de face (même axe, sens opposés, ≤ 6 voies) :', [(s, e) for s in S_ for e in E_ if (s[0] - e[0]) % 6 == 3 and abs(s[1] + e[1]) <= 6])
