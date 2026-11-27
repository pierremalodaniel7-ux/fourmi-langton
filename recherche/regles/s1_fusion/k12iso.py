#!/usr/bin/env python3
"""S1 / R-411 étape C : test isolé (cadre de k1side : temps 0 = 8 760 du circuit) de V0 + K1 + K2 et V7 + K1 + K2, K1 + K2 seuls (K2 = fusion
du catalogue posée exactement, k1match.json ; 3 ordres de jeu pour K2) : propres, sortie commune O absente du cas vide, O sans ombre
(aucune sortie parallèle du cas vide à ≤ 6 voies), pas de sortie de face sur l'axe de V. Écrit s1_fusion/k12iso.json.
Usage : python3 s1_fusion/k12iso.py TT"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from fa_lib import kship, decode, back, sit, lotdump
from hx import rot
TT = int(sys.argv[1]); NB = 30
def mk(r, L, A, ph): return kship(r, rot(((L + A) // 2, (L - A) // 2), r), ph)
V0b, V7b = back(mk(0, 19, 2187, 0), NB), back(mk(0, 19, 2187, 7), NB)
R1 = json.load(open(os.path.join(HERE, 'k1side.json'))); M = json.load(open(os.path.join(HERE, 'k1match.json')))
P = lambda p: (tuple(p[0]), [tuple(c) for c in p[1]])
lines = []; meta = []
for mi, m in enumerate(M):
    r = R1[m['i']]; K1 = P(r['K']); K2 = back(P(m['K']), -1095)
    for pos in range(3):          # rang de K2 : 0 = avant tout, 1 = entre, 2 = après tout
        def order(V):
            base = [V, K1] if r['order'] == 0 else [K1, V]
            return base[:pos] + [K2] + base[pos:] if pos < 2 else base + [K2]
        lines += [sit(order(V0b)), sit(order(V7b)), sit([K1, K2] if pos else [K2, K1])]; meta.append((mi, pos))
out = lotdump(lines, TT)
res = []; st = collections.Counter()
for n, (mi, pos) in enumerate(meta):
    d = [decode(*out[3 * n + j]) for j in range(3)]
    if None in d: st['sale'] += 1; continue
    s0, s7, sN = [set(map(tuple, x)) for x in d]
    com = (s0 & s7) - sN
    if not com: st['pas de sortie commune'] += 1; continue
    com = {o for o in com if not any(p[0] == o[0] and abs(p[1] - o[1]) <= 6 for p in sN)}
    if not com: st['ombre'] += 1; continue
    outs = s0 | s7 | sN
    if any((o[0] - 0) % 6 == 3 and abs(o[1] + 19) <= 6 for o in outs): st['face sur l’axe de c1'] += 1; continue
    st['OK'] += 1; res.append(dict(m=mi, pos=pos, O=sorted(com), s0=sorted(s0), s7=sorted(s7), seul=sorted(sN)))
json.dump(res, open(os.path.join(HERE, 'k12iso.json'), 'w'))
print(len(meta), 'montages :', dict(st))
