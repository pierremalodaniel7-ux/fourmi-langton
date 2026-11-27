#!/usr/bin/env python3
"""R-350 Tourner la retenue c0 du demi-additionneur R-337 avec UN vaisseau constant Kt (pour enchaîner l'additionneur complet
réutilisable R-349 loin de la porte) : 4 cas propres, a∧b lu sur UNE position nouvelle (direction ≠ 2), rien sur une route d'entrée
à contresens ; puis essai d'enchaînement (16 cas) et de réutilisation (20 usages).
Usage : python3 virage_c.py"""
import sys, json, time, itertools, collections, random
from compose import *
from fa_complet import cover
import fa_reutilisable as F
T = 4000
AB = [(0, 0), (0, 1), (1, 0), (1, 1)]
def base(ab): return [K3, K2] + ([B] if ab[1] else []) + ([A] if ab[0] else [])
def route(p):
    s = decode([tuple(p[0])], [tuple(c) for c in p[1]]); return (s[0][0], s[0][1])
IN = [route(B), route(A), route(K2), route(K3)]
def front(s, rl): return (s[0] - rl[0]) % 6 == 3 and abs(s[1] + rl[1]) <= 6
def c0pos(t):                     # c0 = (2, −28, 916, 0) au temps 4000 → position de référence au temps t (multiple de 8)
    from memoire_calc import ship_pos
    p = ship_pos((2, -28, 916, 0)); d = ship_dir(2); n = (T - t) // 8; return (p[0] - n * d[0], p[1] - n * d[1])
cand = []
for t in range(320, 1200, 16):
    P = c0pos(t)
    for rK in (0, 1, 3, 4, 5):
        dK = ship_dir(rK)
        for i in range(-3, 4):
            for j in range(-3, 4):
                st = (P[0] - t // 8 * dK[0] + i, P[1] - t // 8 * dK[1] + j)
                for tau in range(8):
                    K = kship(rK, st, tau)
                    if any(front(route(K), rl) for rl in IN): continue
                    for co in (0, 9): cand.append((t, rK, i, j, tau, co, K))
print('placements de Kt :', len(cand), flush=True)
R = {ab: lotdump([sit((lambda P_: (P_.insert(min(c[5], len(P_)), c[6]), P_)[1])(base(ab))) for c in cand], T) for ab in AB}
good = []
for n, c in enumerate(cand):
    O = {}
    for ab in AB:
        d = decode(*R[ab][n])
        if d is None: break
        O[ab] = [tuple(x) for x in d]
    if len(O) < 4: continue
    outs = {x for v in O.values() for x in v}
    if any(front(s, rl) for s in outs for rl in IN + [route(c[6])]): continue
    PC = cover(O, lambda k: k[0] & k[1])
    if PC in (None, 'grand') or len(PC) != 1 or PC[0][0] == 2: continue
    PS = cover(O, lambda k: k[0] ^ k[1])
    good.append({'c': c[:6], 'K': c[6], 'C': PC[0], 'PS': PS})
print('virages propres de c0 :', len(good), collections.Counter(g['C'][0] for g in good), flush=True)
json.dump(good, open('data/virage_c.json', 'w'))
