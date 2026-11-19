#!/usr/bin/env python3
"""t7_theoreme.py : applique le théorème T7-loin (E2b_couplage.md §S11) aux classes de triplets.
(i) preuve (C) de la classe de c3 recoupée par `ant deux` (data/t7/audit_c_all.out) ;
(ii)+(iii) : transport7 ; (iii') : data/t7/kprime.txt (t7_kprime.py) (data/t7/transport7.txt : K:ok et M:ok). Sortie : bilan + data/t7/theoreme.txt. (S11)"""
import re
from collections import Counter
bases = [l.split() for l in open('resultats/relatif/t7_bases.txt')]
audit = {}
for l in open('data/t7/audit_c_all.out'):
    w = l.split()
    if len(w) > 3: audit[(w[0], w[1], w[2])] = 'COUPLAGE EXACT' in l
def rot(c, r):
    x, y = c
    for _ in range(r): x, y = -y, x
    return x, y
kp = {}
try:
    for l in open('data/t7/kprime.txt'):
        w = l.split(); kp[(w[0], w[6][3:])] = w[7] == 'KP:ok'
except FileNotFoundError: pass
cnt = Counter(); out = open('data/t7/theoreme.txt', 'w'); nb = set()
for l in open('data/t7/transport7.txt'):
    n, C, CE, dirs, vK, vM = l.split()
    r = 'HDBG'.index(bases[int(n)][2]); c3 = tuple(map(int, C.split(';')[2].split(',')))
    x, y = rot(c3, r); a = audit.get((n, str(x + y), str(y)))
    i_ = 'C:ok' if a else ('C:non-audité' if a is None else 'C:ECART')
    if vK != 'K:ok' and kp.get((n, C.split(';')[2])): vK = "K':ok"
    v = 'DEMONTRE' if (a and vK in ('K:ok', "K':ok") and vM == 'M:ok') else 'NON'
    cnt[(v, i_, vK, vM)] += 1; nb.add(n); out.write(f'{n} {C} {v} {i_} {vK} {vM}\n')
tot = sum(cnt.values()); d = sum(v for k, v in cnt.items() if k[0] == 'DEMONTRE')
print(f'bases {len(nb)} ; classes de triplets {tot} ; DÉMONTRÉES par T7-loin {d}')
for k, v in cnt.most_common(): print(' ', k, v)
