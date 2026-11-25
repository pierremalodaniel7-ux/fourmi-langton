#!/usr/bin/env python3
"""R-312 Objets fixes (cycles exacts) à 2 fourmis : fourmi 0 en (0,0), fourmi 1 dans [-3,3]², tous caps, 0 ou 1 case dans [-2,2]².
T = 2^17. Usage : python3 cycles2.py REGLE"""
import sys, collections
from outils_r import lot, parse, geo
rule = sys.argv[1]; _, M = geo(rule)
L = []
for d0 in range(M):
    for x in range(-3, 4):
        for y in range(-3, 4):
            if (x, y) == (0, 0): continue
            for d1 in range(M):
                base = f"{rule}|0,0,{d0};{x},{y},{d1}|"
                L.append(base)
                for cx in range(-2, 3):
                    for cy in range(-2, 3): L.append(base + f"{cx},{cy}")
out = lot(L, 1 << 17)
c = collections.Counter(); per = collections.Counter(); ex = {}
for s, l in zip(L, out):
    d = parse(l); c[d['issue']] += 1
    if d['issue'] == 'CYCLE': per[d['sig']] += 1; ex.setdefault(d['sig'], s)
print(rule, len(L), dict(c))
print('  périodes :', sorted(per.items(), key=lambda kv: int(kv[0][1:]))[:15])
for k in sorted(ex, key=lambda k: int(k[1:]))[:5]: print('  ex', k, ex[k])
