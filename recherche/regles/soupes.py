#!/usr/bin/env python3
"""R-316 Soupes : 1 fourmi au centre d'un carré N×N rempli au hasard (densité 1/2, couleurs au hasard), 200 tirages, 2^20 pas.
Mesure la robustesse du FIL : part qui finit en autoroute, type, début médian. Usage : soupes.py N REGLE…"""
import sys, random, collections
from outils_r import lot, parse, ncol
N = int(sys.argv[1]); random.seed(11)
for rule in sys.argv[2:]:
    q = ncol(rule); L = []
    for e in range(200):
        cs = [f"{x},{y},{random.randint(1, q - 1)}" for x in range(-N // 2, N - N // 2) for y in range(-N // 2, N - N // 2) if random.random() < 0.5]
        L.append(f"{rule}|0,0,0|" + ';'.join(cs))
    c = collections.Counter(); s = collections.Counter(); debs = []
    for l in lot(L, 1 << 20, ncpu=1):
        d = parse(l); c[d['issue']] += 1
        if d['issue'] == 'AUTOROUTES': s[d['sig']] += 1; debs.append(d['ants'][0][3])
    debs.sort()
    print(f"{rule}\tN={N}\t{dict(c)}\tdébut médian {debs[len(debs)//2] if debs else '-'}\t{dict(s.most_common(3))}", flush=True)
