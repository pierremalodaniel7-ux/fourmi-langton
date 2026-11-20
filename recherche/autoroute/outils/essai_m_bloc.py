#!/usr/bin/env python3
"""essai_m_bloc.py TRIPLES : récurrence en m (2e distance) pour T7 : base W1 = blanc + c1 (pivotée comme dans resultats/relatif/bases9/13),
îlot {c2, c3} déplacé en bloc le long de la 2e bande ; `ant multi` (NS 0/1/2) puis `ant deux` pour chaque preuve. (S10)
Sortie : "n c1 J K CE offset verdict regle deux"."""
import sys, os, subprocess, re
here = os.path.dirname(os.path.abspath(__file__)); R = here + '/../../..'; A = R + '/recherche/autoroute/ant'
base = {}
for l in open(R + '/resultats/relatif/bases9.txt'): b, t = l.split(); base[b] = (b, t, 0)
for l in open(R + '/resultats/relatif/bases13.txt'): b, t, cap, o = l.split(); base[o] = (b, t, 'HDBG'.index(cap))
def rot(c, r):
    x, y = c
    for _ in range(r): x, y = -y, x
    return x, y
grid = [['0']] + [['1', str(p)] for p in (90, 70, 50, 110, 150, 190, 300, 600, 900, 1200)] + \
       [['2'] + p.split() for p in ('100 70', '100 40', '120 70', '100 120', '900 600', '1200 900')]
for l in open(sys.argv[1]):
    if l.startswith('#'): continue
    n, C, CE = l.split()[:3]; c = [tuple(map(int, p.split(','))) for p in C.split(';')]
    key = f'{c[0][0]},{c[0][1]}'
    if key not in base: print(n, key, 'PAS_DE_BASE'); continue
    B, T0, r = base[key]; c2, c3 = rot(c[1], r), rot(c[2], r)
    J, K = c2[0] + c2[1], c2[1]; off = [str(c3[0] - c2[0]), str(c3[1] - c2[1])]
    env = dict(os.environ, BASE=B, T0=T0, H0=str(r)); v = 'ECHEC'
    for P in grid:
        o = subprocess.run([A, 'multi', str(J), str(K), CE] + P + off, capture_output=True, text=True, env=env).stdout
        if 'TOUT OK' in o:
            S = re.findall(r's\d=(-?\d+)', o); rg = re.search(r'regle=\d+', o).group(0)
            d = subprocess.run([A, 'deux', str(J), str(K), CE, P[0]] + S + off, capture_output=True, text=True, env=env).stdout
            v = f"OK[{' '.join(P)}] {rg} deux:{'EXACT' if 'COUPLAGE EXACT' in d else 'ECART'}"; break
    print(n, key, J, K, CE, ' '.join(off), v, flush=True)
