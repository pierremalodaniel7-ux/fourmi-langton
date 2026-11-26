#!/usr/bin/env python3
"""S1 / R-401 (complément exhaustif) Fusions à 1 constant où l'un des signaux NE TOUCHE PAS K (transparent exact : sa fourmi ne passe
jamais à ≤ DMAX de celle de K) : alors O = ce signal lui-même, et l'autre signal doit être dévié par K sur sa trajectoire exacte.
Pour chaque choc propre c (fusion1.json) et chaque sortie o ≠ route de K : o prolongé en arrière est-il transparent avec K ?
Si oui, (s1 = o, s2 = entrée de c) est une fusion ; on teste les routes de face. Complète fusion1.py (qui ne voyait que les signaux
qui interagissent) : la recherche à 1 constant est alors EXHAUSTIVE.
Usage : python3 s1_fusion/fusion1b.py"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from hx import ship_dir, step, rot
from chocs_exhaustif_lib import hd, DMAX
from demi_add_k import OFFS
from fusion1_lib import decodeg
D = json.load(open(os.path.join(HERE, 'fusion1.json'))); res = D['res']; T = D['T']
KA = D['K'][0]; KG = {tuple(c): 1 for c in D['K'][1]}
dB = ship_dir(0)
def lanes(o):          # (r, voie) d'une sortie (r, ph, gx, gy)
    r, ph, gx, gy = o; X, Y = rot((gx, gy), -r % 6); return (r, X + Y)
def front(s, e): return (s[0] - e[0]) % 6 == 3 and abs(s[1] + e[1]) <= 6
def kpos(t):           # fourmi de K au temps t (K libre : périodique)
    A = [list(KA)]; G = dict(KG); P = []
    for _ in range(t + 1): P.append((A[0][0], A[0][1])); step(A, G)
    return P
KP = kpos(T + 8 * 400)
def back_free(o, n):
    """trajectoire de la fourmi du vaisseau o (au temps T) prolongée en arrière jusqu'au temps 0 puis en avant : positions t = 0..T+8n"""
    r, ph, gx, gy = o; d = ship_dir(r)
    # point de référence au temps T - ph (début de période) ; au temps t = T - ph - 8m : g - m d
    # positions exactes de la fourmi dans la période : OFFS[(r, p)]
    P = []
    for t in range(T + 8 * n + 1):
        dt = t - (T - ph); m, p = dt // 8, dt % 8
        P.append((gx + m * d[0] + OFFS[(r, p)][0], gy + m * d[1] + OFFS[(r, p)][1]))
    return P
_A = [list(KA)]; _G = dict(KG)
for _ in range(T): step(_A, _G)
Klane = lanes(decodeg(_A, sorted(_G))[0])
cnt = collections.Counter(); found = []
for c in res:
    sA, cs = c['s']; sin = lanes(decodeg([list(sA)], [tuple(x) for x in cs])[0])
    for o in c['out']:
        if lanes(o) == Klane: continue
        P = back_free(o, 400)
        dmin = min(hd(p[0] - q[0], p[1] - q[1]) for p, q in zip(P, KP))
        if dmin <= DMAX: cnt['interagit (déjà couvert par fusion1)'] += 1; continue
        # fusion : s1 = o (transparent), s2 = entrée de c
        g = [x for x in c['out'] if x != o][0]
        ins = [lanes(o), sin, Klane]; outs = [lanes(o), Klane, lanes(o), lanes(g)]
        fr = any(front(s, e) for s in outs for e in ins)
        cnt['fusion, route de face' if fr else 'FUSION sans route de face'] += 1
        found.append(dict(c=c, o=o, face=fr, ombre=(lanes(o)[0] == 0 and abs(lanes(o)[1] - Klane[1]) <= 6)))
print(dict(cnt))
print('sans face :', [(f['o'], f['ombre']) for f in found if not f['face']][:20])
json.dump(found, open(os.path.join(HERE, 'fusion1b.json'), 'w'))
