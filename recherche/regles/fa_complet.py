#!/usr/bin/env python3
"""R-344 Additionneur complet R2L2 : demi-additionneur R-337 (a, b) + retenue entrante c = UN vaisseau de direction 3 qui remonte la
voie de S « tête-bêche ». Pourquoi tête-bêche : S-V (b seul) est 16 périodes devant S-U (a seul) sur la même voie ; un vaisseau qui
remonte la voie rencontre l'un au point P1, l'autre au point P2 (8 périodes plus tard), et les deux rencontres sont la même à une
translation près ⇒ même issue, sans égaliser les horaires (R-344, argument de translation).
Critère : 8 cas (a, b, c) tous propres (0 case non expliquée) ; somme et retenue lisibles comme « un vaisseau sur l'une des positions
P_S (resp. P_C) » ; on classe par nombre de positions (1 = sortie unique, enchaînable).
Usage : python3 fa_complet.py cherche"""
import sys, json, time, itertools
from fa_lib import *
T = 4000
AB = [(0, 0), (0, 1), (1, 0), (1, 1)]
CASES = [(a, b, c) for c in (0, 1) for a, b in AB]
def base(ab): return [K3, K2] + ([B] if ab[1] else []) + ([A] if ab[0] else [])
def case_sit(abc, Cin, co):
    P = base(abc[:2])
    if abc[2]: P.insert(min(co, len(P)), Cin)
    return sit(P)
def SVpos(t):
    n = (T - t) // 8; return (500 - n, -500 + n)
def cover(O, f):
    """plus petit ensemble de positions P tel que f(cas) = 1 ⟺ O[cas] ∩ P ≠ ∅ ; None si impossible"""
    bad = set(x for k in O if not f(k) for x in O[k])
    good = {k: set(O[k]) - bad for k in O if f(k)}
    if any(not v for v in good.values()): return None
    allp = sorted(set().union(*good.values())) if good else []
    for n in range(1, 4):
        for P in itertools.combinations(allp, n):
            if all(set(P) & v for v in good.values()): return list(P)
    return 'grand'
if __name__ == '__main__' and sys.argv[1] == 'cherche':
    t0 = time.time()
    O0 = {abc: decode(*lotdump([case_sit(abc, None, 0)], T)[0]) for abc in CASES if abc[2] == 0}
    cand = []
    for tm in range(240, 1800, 8):
        Pm = SVpos(tm); dK = ship_dir(3)
        for i in range(-5, 6):
            for j in range(-5, 6):
                st = (Pm[0] - tm // 8 * dK[0] + i, Pm[1] - tm // 8 * dK[1] + j)
                if abs(lane(st[0], st[1], 3)) > 7: continue
                for tau in range(8):
                    K = kship(3, st, tau)
                    if min(hd(K[0][0] - p[0], K[0][1] - p[1]) for p in [(0, 0), (30, -56), (62, -24), (-16, 16)]) < 12: continue
                    for co in (0, 9): cand.append((tm, i, j, tau, co, K))
    print('placements de c :', len(cand), flush=True)
    R = {ab: lotdump([case_sit(ab + (1,), c[5], c[4]) for c in cand], T) for ab in AB}
    good = []
    for n, c in enumerate(cand):
        O = dict(O0)
        for ab in AB: O[ab + (1,)] = decode(*R[ab][n])
        if any(v is None for v in O.values()): continue
        O = {k: [tuple(x) for x in v] for k, v in O.items()}
        PS = cover(O, lambda k: sum(k) % 2); PC = cover(O, lambda k: sum(k) >= 2)
        if PS is None or PC is None: continue
        sc = (len(PC) if PC != 'grand' else 9) * 10 + (len(PS) if PS != 'grand' else 9)
        good.append({'c': c[:5], 'K': c[5], 'PS': PS, 'PC': PC, 'score': sc, 'sorties': {str(k): v for k, v in O.items()}})
    good.sort(key=lambda g: g['score'])
    print('additionneurs complets (8/8 propres, lisibles) :', len(good), ' temps', round(time.time() - t0), 's')
    import collections; print('scores :', collections.Counter(g['score'] for g in good).most_common(12))
    json.dump(good, open('data/fa_complet.json', 'w'))
    for g in good[:5]: print(g['c'], 'S sur', g['PS'], ' C sur', g['PC'])
