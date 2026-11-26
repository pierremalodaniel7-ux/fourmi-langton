#!/usr/bin/env python3
"""R-602 Portes « sélectives » en classe paire : un vaisseau Y (dir 2 ou 4) placé pour échanger avec la route décalée X' = X ⊕ σ
(σ = décalage d'un vaisseau dir 0 après un échange) est-il transparent pour la route non décalée X (et inversement) ?"""
import json, itertools
from swaps import issue, shift, sub
from s3lib import *
S = json.load(open('data/swaps.json'))
def neg(s): return (-s[0], -s[1])
sigmas = sorted({tuple(x['sB']) for x in S})          # décalages d'un vaisseau dir 0 (B) par un échange
print('décalages σ de dir 0 :', sigmas)
res = []
for x in S:
    wA, wB, o = tuple(x['A']), tuple(x['B']), x['ordre']
    if x['autre_ordre'] != 'échangé': continue      # on veut un échange valable dans les 2 ordres
    for s in sigmas:
        for sg, nm in ((s, 'Y échange X, test X⊕σ'), (neg(s), 'Y échange X⊕σ, test X')):
            # Y = A échange avec B ; on teste A contre B décalé de sg
            r2 = ''.join(issue(wA, shift(wB, sg), oo, 880) for oo in (0, 1))
            if r2 == 'TT': res.append(dict(r=x['r'], tau=x['tau'], v=x['v'], sigma=s, sens=nm)); print(x['r'], x['tau'], x['v'], 'σ', s, nm, r2)
print(len(res))
json.dump(res, open('data/selectifs.json', 'w'))
