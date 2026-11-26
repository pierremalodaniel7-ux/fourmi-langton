#!/usr/bin/env python3
"""Piste 1 (R-344) : égaliser les horaires de S dans le demi-additionneur R-337 en retardant V (S quand a=0, b=1).
Étape 1 : un vaisseau constant Ka intercepte S-V en aval de la porte et le détourne PROPREMENT ; il ne doit rien abîmer dans les 3
autres cas (S-U intact dans (1,0), C intact dans (1,1), rien sur la voie 0 dans (0,0)).
Étape 2 : un 2e constant Kb ramène le vaisseau détourné sur une route commune avec S-U (même direction, voie, abscisse, phase).
Usage : python3 fa_retard.py etape1 | etape2"""
import sys, json, time
from fa_lib import *
T = 4000
CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
def base(ab):
    return [K3, K2] + ([B] if ab[1] else []) + ([A] if ab[0] else [])
def with_k(ab, Ks):
    """Ks : liste de (pièce, place) ; place 0 = jouée en premier, 9 = en dernier"""
    P = base(ab)
    for k, o in Ks: P.insert(min(o, len(P)), k)
    return sit(P)
REF = {ab: decode(*lotdump([sit(base(ab))], T)[0]) for ab in CASES}
def SVpos(t):
    n = (T - t) // 8; return (500 - n, -500 + n)       # S-V (voie 0, direction 0) : abscisse 1000 à T
if sys.argv[1] == 'etape1':
    t0 = time.time(); cand = []
    for tm in range(280, 1000, 16):
        Pm = SVpos(tm)
        for rK in (1, 2, 3, 4, 5):
            dK = ship_dir(rK)
            for i in range(-2, 3):
                for j in range(-2, 3):
                    st = (Pm[0] - tm // 8 * dK[0] + i, Pm[1] - tm // 8 * dK[1] + j)
                    if min(hd(st[0] - p[0], st[1] - p[1]) for p in [(0, 0), (30, -56), (62, -24), (-16, 16)]) < 12: continue
                    for tau in range(8):
                        K = kship(rK, st, tau)
                        for ko in (0, 9): cand.append((tm, rK, i, j, tau, ko, K))
    print('candidats Ka :', len(cand), flush=True)
    r01 = lotdump([with_k((0, 1), [(c[6], c[5])]) for c in cand], T)
    keep = []
    for c, r in zip(cand, r01):
        d = decode(*r)
        if d is None or (0, 0, 1000, 0) in d: continue
        if not all(x in d for x in REF[(0, 0)]): continue        # les déchets de K2, K3 inchangés
        keep.append(c)
    print('S-V détourné proprement :', len(keep), flush=True)
    res = {ab: lotdump([with_k(ab, [(c[6], c[5])]) for c in keep], T) for ab in [(0, 0), (1, 0), (1, 1)]}
    good = []
    for n, c in enumerate(keep):
        d = {ab: decode(*res[ab][n]) for ab in res}
        if any(v is None for v in d.values()): continue
        if (0, 0, 968, 0) not in d[(1, 0)] or (2, -28, 916, 0) not in d[(1, 1)]: continue
        if any(x[0] == 0 and x[1] == 0 for ab in [(0, 0), (1, 1)] for x in d[ab]): continue
        d01 = decode(*lotdump([with_k((0, 1), [(c[6], c[5])])], T)[0])
        new = [x for x in d01 if x not in d[(0, 0)]]
        good.append({'Ka': c[:6], 'K': c[6], 'nouveaux': new, 'sorties': {str(ab): d[ab] for ab in d} | {'(0, 1)': d01}})
    print('Ka acceptables (4 cas propres) :', len(good), ' temps', round(time.time() - t0), 's', flush=True)
    json.dump(good, open('data/fa_ka.json', 'w'))
if sys.argv[1] == 'tete':
    # Égaliseur « tête-bêche » : un constant Kb de direction 3 remonte la voie de S. S-V est 16 périodes devant S-U : Kb rencontre
    # S-V au point P1 ou S-U au point P2 (8 périodes plus tard, 8 cases plus près de la porte) ; si la rencontre est la même à une
    # translation près, Kb ressort sur la MÊME route dans les deux cas (S unique). Sans S, Kb reste sur sa route d'origine.
    t0 = time.time(); cand = []
    for tm in range(240, 1600, 8):
        Pm = SVpos(tm); dK = ship_dir(3)
        for i in range(-4, 5):
            for j in range(-4, 5):
                st = (Pm[0] - tm // 8 * dK[0] + i, Pm[1] - tm // 8 * dK[1] + j)
                for tau in range(8):
                    K = kship(3, st, tau)
                    if min(hd(K[0][0] - p[0], K[0][1] - p[1]) for p in [(0, 0), (30, -56), (62, -24), (-16, 16)]) < 12: continue
                    for ko in (0, 9): cand.append((tm, i, j, tau, ko, K))
    print('candidats Kb :', len(cand), flush=True)
    R = {ab: lotdump([with_k(ab, [(c[5], c[4])]) for c in cand], T) for ab in CASES}
    good = []
    for n, c in enumerate(cand):
        d = {ab: decode(*R[ab][n]) for ab in CASES}
        if any(v is None for v in d.values()): continue
        com = [x for x in d[(0, 1)] if x in d[(1, 0)] and x not in d[(0, 0)] and x not in d[(1, 1)]]
        if not com or (2, -28, 916, 0) not in d[(1, 1)]: continue
        good.append({'Kb': c[:5], 'K': c[5], 'S': com, 'sorties': {str(ab): d[ab] for ab in CASES}})
    print('égaliseurs trouvés :', len(good), ' temps', round(time.time() - t0), 's', flush=True)
    json.dump(good, open('data/fa_tete.json', 'w'))
    for g in good[:10]: print(g['Kb'], g['S'], g['sorties'])
if sys.argv[1] == 'un':
    # Un seul constant K, toute direction : il intercepte S-V en aval de la porte. Critère : 4 cas propres, S lisible sur UNE position
    # (même vaisseau, même route, même phase dans (1,0) et (0,1), absent de (0,0) et (1,1)), C sur UNE position (seulement dans (1,1)).
    from fa_complet import cover
    t0 = time.time(); cand = []
    dirs = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1, 2, 3, 4, 5]
    TM = range(248, 720, 8) if len(sys.argv) < 4 else range(int(sys.argv[3]), int(sys.argv[4]), 8)
    OF = range(-3, 4) if len(sys.argv) < 6 else range(-int(sys.argv[5]), int(sys.argv[5]) + 1)
    for tm in TM:
        Pm = SVpos(tm)
        for rK in dirs:
            dK = ship_dir(rK)
            for i in OF:
                for j in OF:
                    st = (Pm[0] - tm // 8 * dK[0] + i, Pm[1] - tm // 8 * dK[1] + j)
                    for tau in range(8):
                        K = kship(rK, st, tau)
                        if min(hd(K[0][0] - p[0], K[0][1] - p[1]) for p in [(0, 0), (30, -56), (62, -24), (-16, 16)]) < 12: continue
                        for ko in (0, 9): cand.append((tm, rK, i, j, tau, ko, K))
    print('candidats K :', len(cand), flush=True)
    R = {ab: lotdump([with_k(ab, [(c[6], c[5])]) for c in cand], T) for ab in CASES}
    good = []
    for n, c in enumerate(cand):
        d = {ab: decode(*R[ab][n]) for ab in CASES}
        if any(v is None for v in d.values()): continue
        O = {ab: [tuple(x) for x in d[ab]] for ab in CASES}
        PS = cover(O, lambda k: k[0] ^ k[1]); PC = cover(O, lambda k: k[0] & k[1])
        if PS is None or PC is None or PS == 'grand' or PC == 'grand': continue
        if len(PS) > 1: continue
        good.append({'K': c[6], 'c': c[:6], 'PS': PS, 'PC': PC, 'n': len(PS) + len(PC), 'sorties': {str(ab): O[ab] for ab in CASES}})
    good.sort(key=lambda g: g['n'])
    import collections
    print('lisibles :', len(good), collections.Counter(g['n'] for g in good), ' temps', round(time.time() - t0), 's', flush=True)
    json.dump(good, open('data/fa_un_%s_%s.json' % (''.join(map(str, dirs)), '_'.join(sys.argv[3:6])), 'w'))
    for g in good[:8]: print(g['c'], g['PS'], g['PC'])
