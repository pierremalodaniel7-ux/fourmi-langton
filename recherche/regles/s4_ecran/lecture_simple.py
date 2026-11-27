#!/usr/bin/env python3
"""R-709 Lecture (destructive pour le 0) du pixel M/R' par UNE sonde (option 0 : direction 0, voie −3) — 2 moteurs.
Cas ON : mise à 1 puis sonde ; cas OFF : sonde seule. On lit le RETARD de la sonde à la sortie (temps de vol)."""
import sys
sys.argv = [sys.argv[0], '1', '0', '0']
from lecture_demo import *
for name, ops in (('ON', [('set', 415)]), ('OFF', [])):
    t = (ops[-1][1] if ops else 0) + GAP; st, tr, pr = ('M', 0, 0) if not ops else (K['set']['dst'], 415 + K['set']['T'], K['set']['fin'])
    if name == 'ON':
        p = (pr + t - tr) % 12; ops = ops + [(f'lire1_{p}', t)]; pn = f'lire1_{p}'
    else:
        while (t - tr) % 21 != K['lire0']['ph']: t += 1
        ops = ops + [('lire0', t)]; pn = 'lire0'
    s = sit(ops); T = t + 2400
    (a, c), = [lotdump([s], T)[0]]; pa, pc = pyrun(s, T)
    same2 = sorted(pa) == sorted(map(tuple, a)) and sorted(pc) == sorted(map(tuple, c))
    fa = [tuple(x) for x in a if hd(x[0], x[1]) > 6]; fc = [tuple(x) for x in c if hd(*x) > 6]
    got = sorted(of_label(lab_of(z, T)) for z in decode(fa, fc))
    out = norm(movT(K[pn]['out'], (0, 0), t)); retard = to_label(K[pn]['S'])[2] - to_label(K[pn]['out'])[2]
    print(name, ': sortie de la sonde attendue présente', out in got, '; retard de la sonde', retard, 'pas ; objet', K[pn]['dst'], '; 2 moteurs', same2)
