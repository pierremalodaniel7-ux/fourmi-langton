#!/usr/bin/env python3
"""transport7.py : hypothèses du transport (R-95, transport.py) aux deux étages de T7 (S10). Pour chaque triplet :
 - K : récurrence en k1 (bloc, NS0) à transporter le long de m (pas d2) et de m3 (pas d3) : chaque pas doit être d ou ⟂ d,
       et si ⟂ avec direction finale -d, les diagonales de la fenêtre finale doivent s'éloigner de D (critère de transport.py) ;
 - M : récurrence en m (bloc dans le repère pivoté de blanc + c1, NS0) à transporter le long de m3 : d3 = d2 ou ⟂ d2, même critère.
Sortie : bilan ; détails dans data/t7/transport7.txt. Lemme à deux étages : À ÉCRIRE ET RELIRE (E2b_couplage.md)."""
import subprocess, re, os
from collections import Counter
R = '.'; A = R + '/recherche/autoroute/ant'
T = [l.split() for l in open('data/t7/triples.txt') if not l.startswith('#')]
k1 = [l.split() for l in open('data/t7/rec_k1.txt')]; mm = [l.split() for l in open('data/t7/rec_m.txt')]
D = [l.split() for l in open('data/t7/directions.txt')]
base = {}
for l in open('resultats/relatif/bases9.txt'): b, t = l.split(); base[b] = (b, t, 0)
for l in open('resultats/relatif/bases13.txt'): b, t, cap, o = l.split(); base[o] = (b, t, 'HDBG'.index(cap))
def rot(c, r):
    x, y = c
    for _ in range(r): x, y = -y, x
    return x, y
def fin(args, env=None):
    o = subprocess.run([A, 'multi'] + args, capture_output=True, text=True, env=env).stdout
    return tuple(map(int, re.search(r'dir=\((-?\d+),(-?\d+)\) diagZ=\[(-?\d+),(-?\d+)\] diagD=\[(-?\d+),(-?\d+)\]', o).groups()))
def pas_ok(dref, step, f):           # dref : direction de la récurrence (y bas) ; step : direction du transport ; f : sortie multi
    if step == dref: return True
    if step[0]*dref[0] + step[1]*dref[1] != 0: return False      # -dref : non traité
    fx, fy, z0, z1, D0, D1 = f
    if (fx, fy) != (-dref[0], dref[1]): return True                # repère y haut : -d  <->  (−dx, dy) ... (cf. transport.py pour d=(-2,2))
    s = 4 if (step[0] + step[1]) > 0 else -4
    return (s > 0 and z0 > D1) or (s < 0 and z1 < D0)
cnt = Counter(); out = open('data/t7/transport7.txt', 'w')
for i, t in enumerate(T):
    ds = [(int(a), int(b)) for a, b in re.findall(r'\((-?\d+), (-?\d+)\)', ' '.join(D[i][3:]))]; d = (-2, 2); d2, d3 = ds[0], ds[1]
    vK = 'K:non-NS0'
    if k1[i][-1] == 'NS0':
        f = fin([k1[i][1], k1[i][2], k1[i][3], '0'] + k1[i][4:8])
        vK = 'K:ok' if (pas_ok(d, d2, f) and pas_ok(d, d3, f)) else 'K:dir'
    vM = 'M:non-NS0'
    if mm[i][-3] == 'OK[0]':
        c = [tuple(map(int, p.split(','))) for p in t[1].split(';')]; B, T0, r = base[f'{c[0][0]},{c[0][1]}']
        env = dict(os.environ, BASE=B, T0=T0, H0=str(r)); f = fin([mm[i][2], mm[i][3], mm[i][4], '0', mm[i][5], mm[i][6]], env)
        d3p = rot(d3, r)                                     # dans le repère pivoté, d2 devient (-2,2)
        vM = 'M:ok' if pas_ok((-2, 2), d3p, f) else 'M:dir'
    cnt[(vK, vM)] += 1; out.write(f'{t[0]} {t[1]} {t[2]} {D[i][2]} {vK} {vM}\n')
for k, v in cnt.most_common(): print(k, v)
