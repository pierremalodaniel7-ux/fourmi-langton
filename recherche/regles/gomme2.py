#!/usr/bin/env python3
"""R-300 (balayage) : gomme pour TOUTES les règles q = 2 (carré LRNU², hexa 6², triangle RLU²) et q = 3 (carré, hexa),
plusieurs T (pairs et impairs) et départs (blanc + 3 départs à cases au hasard). Sortie : data/gomme2.txt"""
import random, itertools, sys
from gomme import gomme, run, geo
random.seed(7)
HXL = {0:'N',1:'R1',2:'R2',3:'U',4:'L2',5:'L1'}
def rules(q):
    for w in itertools.product('LRNU', repeat=q): yield ''.join(w), [{'L':3,'R':1,'N':0,'U':2}[c] for c in w], 4
    for w in itertools.product(range(6), repeat=q): yield 'H:' + ''.join(HXL[k] for k in w), list(w), 6
    if q == 2:
        for w in itertools.product('RLU', repeat=q): yield 'T:' + ''.join(w), [{'R':1,'L':5,'U':3}[c] for c in w], 6
out = open('data/gomme2.txt', 'w')
stat = {}
for q in (2, 3):
    for rule, K, M in rules(q):
        res = []
        for essai in range(6):
            T = random.randint(500, 6000)
            init = {}
            if essai >= 2:
                for _ in range(5): init[(random.randint(-3, 3), random.randint(-3, 3))] = random.randint(1, q - 1)
            ok, *_ = gomme(rule, T, init)
            res.append(ok)
        cond = q == 2 and (K[0] + K[1]) % M == 0
        deg = len(set(K)) == 1
        tag = 'TOUJOURS' if all(res) else 'JAMAIS' if not any(res) else 'PARFOIS'
        stat.setdefault((q, cond, deg, tag), []).append(rule)
        print(rule, K, 'cond' if cond else '-', 'degen' if deg else '-', tag, ''.join('1' if r else '0' for r in res), file=out)
out.close()
for k, v in sorted(stat.items()): print(k, len(v), ' '.join(v[:12]) + (' …' if len(v) > 12 else ''))
