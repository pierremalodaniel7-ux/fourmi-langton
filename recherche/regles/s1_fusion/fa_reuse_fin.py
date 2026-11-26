#!/usr/bin/env python3
"""S1 / R-407 (copie de fa_reuse.py avec le critère FIN de croisement R-404 : deux routes à contresens ne se gênent que si la
somme de leurs voies est dans [−3, 1]). R-349bis Additionneur complet RÉUTILISABLE ? demi-additionneur R-337 (a, b) + retenue c = UN vaisseau, de direction quelconque,
qui croise la route de B, de K3 ou de S à un instant quelconque. Critères : 8 cas propres ; somme et retenue lisibles en « un vaisseau sur
l'une des positions » (≤ 3 positions) ; AUCUNE route de sortie sur un axe d'entrée à contresens (sinon l'usage suivant est percuté) et la
route de c n'est l'axe d'aucune sortie à contresens. Puis : 2 usages, 64 suites, superposition exacte.
Usage : python3 fa_reuse.py [directions] [graine de tranche]"""
import sys, os, json, time, itertools, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from fa_lib import *
from fa_complet import cover
from circuit import Circuit, check_multi
T = 4000
dirs = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [0, 1, 2, 4, 5]
AB = [(0, 0), (0, 1), (1, 0), (1, 1)]
def base(ab): return [K3, K2] + ([B] if ab[1] else []) + ([A] if ab[0] else [])
def route(p):
    s = decode([tuple(p[0])], [tuple(c) for c in p[1]]); return (s[0][0], s[0][1])
IN = [route(B), route(A), route(K2), route(K3)]
def front(s, rl): return (s[0] - rl[0]) % 6 == 3 and -3 <= s[1] + rl[1] <= 1
O0 = {ab + (0,): [tuple(x) for x in decode(*lotdump([sit(base(ab))], T)[0])] for ab in AB}
# points de passage : B (voie 0, avant et après la porte), K3, S-V / S-U
def lane0(t, along0):           # vaisseau direction 0, voie 0, abscisse along0 au temps 4000 → position au temps t (multiple de 8)
    a = along0 - 2 * ((T - t) // 8); return (a // 2, -a // 2)
pts = []
for t in range(80, 800, 16):
    for a0 in (1000, 968):       # route de B / S-V et de K3 / S-U
        pts.append((t, lane0(t, a0)))
t0 = time.time(); cand = []
for t, P in pts:
    for rK in dirs:
        dK = ship_dir(rK)
        for i in range(-4, 5):
            for j in range(-4, 5):
                st = (P[0] - t // 8 * dK[0] + i, P[1] - t // 8 * dK[1] + j)
                for tau in range(0, 8):
                    K = kship(rK, st, tau)
                    if min(hd(K[0][0] - p[0], K[0][1] - p[1]) for p in [(0, 0), (30, -56), (62, -24), (-16, 16)]) < 10: continue
                    rk = route(K)
                    if any(front((rk[0], rk[1]), rl) for rl in IN): continue        # c sur un axe d'entrée à contresens
                    for co in (0, 9): cand.append((t, rK, i, j, tau, co, K))
print('placements de c :', len(cand), flush=True)
R = {ab: lotdump([sit((lambda P: (P.insert(min(c[5], len(P)), c[6]), P)[1])(base(ab))) for c in cand], T) for ab in AB}
good = []
for n, c in enumerate(cand):
    O = dict(O0); bad = False
    for ab in AB:
        d = decode(*R[ab][n])
        if d is None: bad = True; break
        O[ab + (1,)] = [tuple(x) for x in d]
    if bad: continue
    rk = route(c[6]); outs = {x for v in O.values() for x in v}
    if any(front(s, rl) for s in outs for rl in IN + [rk]): continue
    PS = cover(O, lambda k: sum(k) % 2); PC = cover(O, lambda k: int(sum(k) >= 2))
    if PS in (None, 'grand') or PC in (None, 'grand'): continue
    good.append({'c': c[:6], 'K': c[6], 'PS': PS, 'PC': PC, 'n': len(PS) + 10 * len(PC)})
print('8/8 propres, lisibles, sans route de face :', len(good), ' temps', round(time.time() - t0), 's', flush=True)
good.sort(key=lambda g: g['n'])
json.dump(good, open('s1_fusion/data_fa_fin_%s.json' % ''.join(map(str, dirs)), 'w'))
print(collections.Counter(g['n'] for g in good).most_common(8))
# réutilisation : 2 usages, 64 suites (sur les 40 premiers)
ok = []
for g in [g for g in good if g['K'] is not None][:int(os.environ.get('NFA', '60'))]:
    K = (tuple(g['K'][0]), [tuple(x) for x in g['K'][1]]); pieces = [('K3', K3, None), ('K2', K2, None), ('B', B, 'b'), ('A', A, 'a')]
    pieces.insert(min(g['c'][5], 4), ('c', K, 'c'))
    C = Circuit(pieces, {'S': (lambda e: (e['a'] + e['b'] + e['c']) % 2, [tuple(p) for p in g['PS']]),
                         'C': (lambda e: int(e['a'] + e['b'] + e['c'] >= 2), [tuple(p) for p in g['PC']])})
    n2 = sum(1 for e1, e2 in itertools.product(C.cases(), repeat=2) if (lambda s: s[0] and s[1] == 2)(check_multi(C, [e1, e2], 200)))
    if n2 == 64: ok.append(g); print('RÉUTILISABLE (2 usages 64/64) :', g['c'], g['PS'], g['PC'], flush=True)
json.dump(ok, open('s1_fusion/fa_fin_ok_%s.json' % ''.join(map(str, dirs)), 'w'))
print('réutilisables :', len(ok))
