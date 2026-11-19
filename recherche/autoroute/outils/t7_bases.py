#!/usr/bin/env python3
"""t7_bases.py : les 484 bases W2 = blanc + c1 + c2 de T7 (une par paire de classes, écart k0 de recurrence_k1.txt),
pivotées (rotation de 90° k fois, cap tourné) pour que l'autoroute finale ait la dérive (-2,+2). Sortie : "BASE T0 CAP ORIG" (S9)."""
import subprocess, re, sys, os
here = os.path.dirname(os.path.abspath(__file__)); F = here + '/../../../src/fourmi'
R = here + '/../../../resultats/relatif/recurrence_k1.txt'
L = open(R).read().split('\n')[:-1][::2]            # 1 ligne sur 2 : écart k0
def rot(c): return (-c[1], c[0])                     # quart de tour (y vers le bas) : H -> D
out = []
lines = []
for l in L:
    J, K, CE, ex, ey = map(int, l.split()[:5]); c1 = (J - K, K); c2 = (c1[0] + ex, c1[1] + ey)
    for r in range(4):
        a, b = c1, c2
        for _ in range(r): a, b = rot(a), rot(b)
        lines.append((l, r, f'RL|0,0,{"HDBG"[r]}|{a[0]},{a[1]};{b[0]},{b[1]}\n'))
o = subprocess.run([F, '-T', '400000000', '-cert', '-lot'], input=''.join(x[2] for x in lines), capture_output=True, text=True).stdout.splitlines()
for (l, r, s), res in zip(lines, o):
    m = re.search(r'CERT (\d+) .* 104,(-?\d+),(-?\d+),', res)
    if m and (m.group(2), m.group(3)) == ('-2', '2'):
        J, K, CE, ex, ey = map(int, l.split()[:5])
        print(s.split('|')[2].strip(), m.group(1), "HDBG"[r], f'{J-K},{K};{J-K+ex},{K+ey}')
