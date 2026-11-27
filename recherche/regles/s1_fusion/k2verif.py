#!/usr/bin/env python3
"""S1 / R-411 : vérification d'un montage de k2full.json (indice i) avec les 2 moteurs (fourmi_r512 et hx.py), 16 cas, temps T3.
Usage : python3 s1_fusion/k2verif.py i T3"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import big; big.patch()
from circuit import Circuit
from fa_lib import decode, lotdump, pyrun
i, T3 = int(sys.argv[1]), int(sys.argv[2]); r = json.load(open(os.path.join(HERE, 'k2full.json')))[i]
C = Circuit([(n, (tuple(p[0]), [tuple(c) for c in p[1]]), v) for n, p, v in r['pieces']])
cs = C.cases(); L = [C.sit(e) for e in cs]; R = lotdump(L, T3); same = 0
for e, s, x in zip(cs, L, R):
    pa, pc = pyrun(s, T3); ok = sorted(pa) == sorted(map(tuple, x[0])) and sorted(pc) == sorted(map(tuple, x[1])); same += ok
    print(''.join(str(e[v]) for v in ('a0', 'b0', 'a1', 'b1')), 'O' if tuple(r['O'][0]) in set(map(tuple, decode(*x))) else '-', '2 moteurs identiques' if ok else 'DIFFÉRENTS')
print('pièces :', [(n, p[0]) for n, p, v in r['pieces'] if n in ('K1', 'K2')], '; 2 moteurs identiques :', same, '/16')
