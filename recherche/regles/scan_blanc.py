#!/usr/bin/env python3
"""R-303 : départ blanc pour toutes les règles candidates (carré, hexa q=2 et q=3, triangle q=2 et q=3), T = 2^22."""
import itertools
from outils_r import lot, parse
HXL = {0:'N',1:'R1',2:'R2',3:'U',4:'L2',5:'L1'}
R = ['RL','LLR','LLLR','LLLLR','LLLLLR','LLLLLLR','LLRRRL','RLLR']
seen = set()
for q in (2, 3):
    for w in itertools.product(range(6), repeat=q):
        if len(set(w)) == 1 or w[0] == 0: continue          # mouvement indépendant de la couleur / ligne droite sur blanc
        m = tuple((6 - k) % 6 for k in w)
        if m in seen: continue
        seen.add(w); R.append('H:' + ''.join(HXL[k] for k in w))
for q in (2, 3):
    for w in itertools.product('RLU', repeat=q):
        if len(set(w)) == 1 or w[0] == 'L': continue          # miroir R<->L
        R.append('T:' + ''.join(w))
out = lot([f"{r}|0,0,0|" for r in R], 1 << 22)
with open('data/scan_blanc.txt', 'w') as f:
    for r, l in zip(R, out):
        d = parse(l); a = d['ants'][0] if d['ants'] else None
        f.write(f"{r}\t{d['issue']}\t{d['sig']}\t{a[3] if a else '-'}\t{d['boite']}\n")
print(len(R), 'règles')
