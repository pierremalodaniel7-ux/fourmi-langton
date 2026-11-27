#!/usr/bin/env python3
"""R-603 Couples de géométries (g, h) pour un circuit « NOR puis ET » en classe paire, logique de PRÉSENCE au niveau 1 et de VOIE au niveau 2 :
 g : puissance K (dir 0) × littéral L (dir 2) : échange dans les 2 ordres ; K décalé (K⊕σ_K) transparent pour un littéral placé pour K.
 h : K (dir 0) × puissance P (dir 4) : échange (K non décalé, P non décalé) ; transparents : (K⊕σ_K, P), (K, P⊕σ_P), (K⊕σ_K, P⊕σ_P)."""
import json
from swaps import issue, shift, sub
from s3lib import *
S = json.load(open('data/swaps.json'))
T = 880
def TT(wA, wB): return all(issue(wA, wB, o, T) == 'T' for o in (0, 1))
G = []
for x in S:
    if x['r'] != 2 or x['autre_ordre'] != 'échangé': continue
    wA, wB = tuple(x['A']), tuple(x['B']); sK = tuple(x['sB'])
    if TT(wA, shift(wB, sK)): G.append(x)
print('g possibles :', len(G), [(x['tau'], x['v'], x['ordre'], x['sB'], x['sA']) for x in G])
sKs = sorted({tuple(x['sB']) for x in G})
H = []
for y in S:
    if y['r'] != 4 or y['autre_ordre'] != 'échangé': continue
    wA, wB = tuple(y['A']), tuple(y['B']); sP = tuple(y['sA'])
    for sK in sKs:
        if TT(wA, shift(wB, sK)) and TT(shift(wA, sP), wB) and TT(shift(wA, sP), shift(wB, sK)):
            H.append(dict(h=y, sK=sK)); print('h', y['tau'], y['v'], y['ordre'], 'σP', sP, 'pour σK', sK)
json.dump(dict(G=G, H=H), open('data/combos.json', 'w'))
