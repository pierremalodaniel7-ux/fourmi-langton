#!/usr/bin/env python3
"""relatif.py "BASE" T0 K2 [CAP] (CAP = cap initial H D B G de la fourmi en (0,0)) : partie (C) de « BASE + une case loin dans sa bande ».
BASE = cases (y vers le bas) ; T0 = certificat de la base (dérive (-2,+2)). Repère la bande (diagonales touchées à k = K2),
calcule les classes (k = K2..K2+5), puis prouve chaque classe avec `ant multi` (NS = pente/52 - 1, seuils cherchés)."""
import sys, re, subprocess, os
from collections import defaultdict
B, T0, K2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); CAP = sys.argv[4] if len(sys.argv) > 4 else "H"; H0 = "HDBG".index(CAP)
here = os.path.dirname(os.path.abspath(__file__)); F = here + '/../../../src/fourmi'; A = here + '/../ant'
def lot(lines):
    o = subprocess.run([F, '-T', '200000000', '-cert', '-lot'], input=''.join(lines), capture_output=True, text=True).stdout
    return o.splitlines()
# position de la fourmi à T0 -> diagonale centrale
o = subprocess.run([F, '-cert', '-c0', str(T0), f'RL|0,0,{CAP}|{B}'], capture_output=True, text=True).stdout
m = re.search(r'fin (-?\d+),(-?\d+)', o)
lines = []; keys = []
# balayage large des diagonales : on prend j sur [-400, 400] mais seulement celles « touchées » (pas certifié != celui de la base)
base_cert = int(re.search(r'CERT (\d+)', o).group(1))
jc = int(m.group(1)) + int(m.group(2))   # S9 : bande centrée sur la fourmi à T0 (bases pivotées de T7) ; contient l'ancien [-450,450]
JR = range(min(-450, jc - 450), max(450, jc + 450) + 1)
cand = []
for j in JR:
    cand.append(f'RL|0,0,{CAP}|{B};{j-K2},{K2}\n')
res = lot(cand); hit = [j for j, l in zip(JR, res) if int(re.search(r'CERT (\d+)', l).group(1)) != base_cert]
hit2 = []
for j in JR:
    cand2 = f'RL|0,0,{CAP}|{B};{j-K2-1},{K2+1}\n'; hit2.append(cand2)
res2 = lot(hit2); hit += [j for j, l in zip(JR, res2) if int(re.search(r'CERT (\d+)', l).group(1)) != base_cert]
js = sorted(set(hit)); print('# base cert', base_cert, 'diagonales touchées', js[:3], '...', js[-3:], len(js), file=sys.stderr)
cl = defaultdict(list)
L = [f'RL|0,0,{CAP}|{B};{j-k},{k}\n' for j in js for k in range(K2, K2 + 6)]
for l in lot(L):
    x, y = map(int, l.split('|')[2].split(';')[-1].split(','))
    c = int(re.search(r'CERT (\d+)', l).group(1)); cl[(x + y, y % 2)].append((y, c))
env = dict(os.environ, BASE=B, T0=str(T0), H0=str(H0)); ok = ko = 0; stat = defaultdict(int)
for (j, par), V in sorted(cl.items()):
    V.sort(); S = {(c - V[0][1]) / (k - V[0][0]) for k, c in V[1:]}
    if len(S) != 1: print('IRREGULIER', j, par, V); ko += 1; continue
    s = S.pop(); stat[s] += 1
    if s == 0: continue
    NS = int(s // 52) - 1; k0, c0 = V[0]; good = False
    grids = {0: [[]], 1: [[90], [70], [50], [110], [130], [150], [190], [300], [400], [500], [600], [900], [1200], [1500]], 2: [[100, 70], [100, 40], [120, 70], [100, 120], [400, 300], [500, 350], [600, 400]], 3: [[100, 70, 100], [100, 120, 100], [500, 350, 500]]}.get(NS, [])  # seuils hauts : bases dont D monte haut
    for P in grids:
        r = subprocess.run([A, 'multi', str(j), str(k0), str(c0), str(NS)] + [str(p) for p in P], capture_output=True, text=True, env=env).stdout
        if 'TOUT OK' in r: good = True; print('OK', j, k0, c0, NS, *P); break
    if good: ok += 1
    else: ko += 1; print('ECHEC', j, k0, c0, NS, 'pente', s)
print('# classes', dict(stat), 'preuves OK', ok, 'ECHEC', ko, file=sys.stderr)
