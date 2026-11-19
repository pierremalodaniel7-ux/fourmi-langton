#!/usr/bin/env python3
"""essai_m_c3fixe.py REC_M TRIPLES : pour les ECHEC de essai_m_bloc.py, récurrence en m avec c3 FIXE :
base = blanc + c1 + c3 (pivotée), îlot c2 seul ; multi puis deux. (S10)"""
import sys, os, subprocess, re
here = os.path.dirname(os.path.abspath(__file__)); R = here + '/../../..'; A = R + '/recherche/autoroute/ant'; F = R + '/src/fourmi'
base = {}
for l in open(R + '/resultats/relatif/bases9.txt'): b, t = l.split(); base[b] = (b, 0)
for l in open(R + '/resultats/relatif/bases13.txt'): b, t, cap, o = l.split(); base[o] = (b, 'HDBG'.index(cap))
def rot(c, r):
    x, y = c
    for _ in range(r): x, y = -y, x
    return x, y
ech = set()
for l in open(sys.argv[1]):
    w = l.split()
    if w[-1] == 'ECHEC': ech.add((w[0], w[4]))
grid = [['0']] + [['1', str(p)] for p in (90, 70, 50, 110, 150, 190, 300, 600, 900, 1200)] + \
       [['2'] + p.split() for p in ('100 70', '100 40', '120 70', '100 120', '900 600', '1200 900')]
for l in open(sys.argv[2]):
    n, C, CE = l.split()[:3]
    if (n, CE) not in ech: continue
    c = [tuple(map(int, p.split(','))) for p in C.split(';')]; B, r = base[f'{c[0][0]},{c[0][1]}']
    c2, c3 = rot(c[1], r), rot(c[2], r); B2 = f'{B};{c3[0]},{c3[1]}'
    o = subprocess.run([F, '-T', '400000000', '-cert', f'RL|0,0,{"HDBG"[r]}|{B2}'], capture_output=True, text=True).stdout
    m = re.search(r'CERT (\d+) .* 104,(-?\d+),(-?\d+),', o)
    if not m or (m.group(2), m.group(3)) != ('-2', '2'): print(n, C, 'BASE_PAS_DERIVE', m and m.groups()); continue
    T0 = m.group(1); env = dict(os.environ, BASE=B2, T0=T0, H0=str(r)); J, K = c2[0] + c2[1], c2[1]; v = 'ECHEC'
    for P in grid:
        out = subprocess.run([A, 'multi', str(J), str(K), CE] + P, capture_output=True, text=True, env=env).stdout
        if 'TOUT OK' in out:
            S = re.findall(r's\d=(-?\d+)', out); rg = re.search(r'regle=\d+', out).group(0)
            d = subprocess.run([A, 'deux', str(J), str(K), CE, P[0]] + S, capture_output=True, text=True, env=env).stdout
            v = f"OK[{' '.join(P)}] {rg} deux:{'EXACT' if 'COUPLAGE EXACT' in d else 'ECART'}"; break
    print(n, C, CE, 'T0=' + T0, v, flush=True)
